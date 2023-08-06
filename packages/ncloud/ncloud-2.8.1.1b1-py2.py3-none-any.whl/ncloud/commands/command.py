# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Command line interface for Nervana's deep learning cloud.
"""
from builtins import object
from collections import namedtuple
from datetime import datetime
import inspect
import logging
import os
import tarfile
import sys
import zipfile
import io
import requests
import json
import time

from nauth.errors import PasswordExpirationError
from ncloud.completers import DirectoriesCompleter
from ncloud.formatting.output import print_table
from ncloud.formatting.time_zone import utc_to_local
from ncloud.vendor.python.argparse import ArgumentTypeError
from ncloud.util.request_processor import NcloudRequest
from ncloud.util.file_transfer import download_compressed, download_objects
from ncloud.util.url_processor import url_processor

logger = logging.getLogger()

# command constants
Cmd = namedtuple('Cmd', ['name', 'aliases'])
LS = Cmd('ls', ('list', 'l'))
SHOW = Cmd('show', ('s',))
UL = Cmd('ul', ('upload', 'u'))
LN = Cmd('ln', ('link', 'k'))
RM = Cmd('rm', ('remove',))
ADD = Cmd('add', ('a',))
MODIFY = Cmd('modify', ('m',))
TRAIN = Cmd('train', ('t',))
START = Cmd('start', ())
STOP = Cmd('stop', ())
RESULTS = Cmd('results', ('res', 'r'))
IMPORT = Cmd('import', ('i',))
DEPLOY = Cmd('deploy', ('d',))
PREDICT = Cmd('predict', ('p',))
UNDEPLOY = Cmd('undeploy', ('ud', 'u'))
ADDGRP = Cmd('addgrp', ('addgroup', 'ag'))
RMGRP = Cmd('rmgrp', ('removegroup', 'rmg', 'rg'))
PWRST = Cmd('pwrst', ('pwreset', 'pr'))
HIST = Cmd('history', ('hist', 'h'))
REVOKE = Cmd('revoke', ('r',))
DEFAULT = Cmd('default', ('d',))


def string_argument(string):
    if len(string) > 255:
        raise ArgumentTypeError('"%s" must be less than 255 characters.' %
                                string)
    return string


def collection_argument(string):
    split = string.split(':')
    if len(split) is not 2:
        raise ArgumentTypeError('"%s" must contain one colon.' % string)
    if not split[1].isdigit():
        raise ArgumentTypeError('"s" must be an integer.' % split[1])
    split[1] = int(split[1])
    return tuple(split)


def iso_8601_argument(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: {}. Need YYYY-MM-DD format.".format(date)
        raise ArgumentTypeError(msg)


class Choices(object):
    """class used to specify what choices for a
       command arg should be allowed
    """

    def __init__(self, choices):
        self.choices = choices

    def __iter__(self):
        yield self

    def __contains__(self, key):
        return key in self.choices

    def __repr__(self):
        # can't have brackets with argparse in add_argument
        # see https://bugs.python.org/issue14046
        # return str(self.choices)
        return ', '.join([str(x) for x in self.choices])


class Command(object):
    # used in multiple inheritance, like List --> BaseList --> Command
    BASE_ARGS = {}

    @classmethod
    def parser(cls, subparser):
        raise NotImplementedError("provide a subparser for your command")

    @classmethod
    def arg_names(cls, startidx=1):
        return inspect.getargspec(cls.call).args[startidx:]

    @staticmethod
    def call():
        raise NotImplementedError("provide an implementation for your command")

    @staticmethod
    def api_call(*args, **kwargs):
        if not hasattr(Command, 'request_handler'):
            Command.request_handler = NcloudRequest()
        return Command.request_handler.make_call(*args, **kwargs)

    @staticmethod
    def display_before(config, args):
        pass

    @staticmethod
    def display_after(config, args, res):
        if res is not None:
            print_table(res)

    @classmethod
    def arg_call(cls, config, args):
        arg_dict = vars(args)
        arg_vals = []
        for name in cls.arg_names():
            # check if parameter got excluded based on auth_type
            if name in arg_dict.keys():
                arg_vals.append(arg_dict[name])
            else:
                arg_vals.append(None)
        # used with multiple inheritance args in the .call() funcs
        cls.BASE_ARGS = {name: arg_dict[name] for name in cls.BASE_ARGS}
        cls.display_before(config, args)
        try:
            res = cls.call(config, *arg_vals)
            cls.display_after(config, args, res)
        except PasswordExpirationError:
            url = url_processor(arg_dict["host"])
            msg = "Your password has expired. Please go to {} in order" \
                  "to change your password and try again".format(url)
            Command.display_after(config, args, {'error': msg})

        # reset the base args, if any
        cls.BASE_ARGS = {}


class ShowLogs(Command):
    """
    Provides a base class for displaying logs
    """

    @classmethod
    def parser(cls, subparser, aliases, help_text, desc):
        show_logs = subparser.add_parser(
            SHOW.name, aliases=aliases,
            help=help_text, description=desc
        )

        show_logs.add_argument(
            "-l", "--log", action="store_true",
            help="Show console log from runtime."
        )
        show_logs.add_argument(
            "-L", "--log-follow", action="store_true",
            help="Show console log from runtime as the data grows." +
                 "Similar to how tail -f works on a UNIX-based machine."
        )

        return show_logs

    @staticmethod
    def read_log(config, path, params):
        # if we aren't streaming, then the data returned as zipfile bytes
        # has to be done here because of pytest shenanigans
        # pytest replaces sys.stdout specifically
        write = getattr(sys.stdout, 'buffer', sys.stdout).write
        res = ShowLogs.api_call(config, path, params=params)
        try:
            write(
                zipfile.ZipFile(io.BytesIO(res)).read(params.get('log_file')))
        except KeyError:
            logger.warning("attempting to view non-existent {}".format(
                           params.get('log_file')))

    @staticmethod
    def default_stream_parser(log_data):
        """
        Parse the data returned from the server and dsiplay it.
        """
        # get the data from each request
        # write the results out and use the offset to fetch more
        # data from that point
        results = log_data['results']
        offset = log_data['offset']
        if results:
            print(results)

        return offset

    @staticmethod
    def read_log_tail(config, show_path, params, stream_parser=None):
        """
        Read and tail a log. Uses the custom stream_parser if provided.
        The stream_parser should accept the arguments log_data and status_code.
        """
        sess = requests.session()
        # Get logs from helium
        result, status_code = ShowLogs.api_call(
            config, show_path, stream=True,
            session=sess, params=params,
            return_status_code=True,
            console_log_follow=True
        )
        log_data = json.loads(result)

        while True:
            try:
                # if we are logging immediately, then keep
                # trying to fetch the tailing logs
                # even though they might not be here yet
                # only applies to console_log_follow (-L)
                # TODO: why does custom code return 404...
                if status_code in (400, 404):
                    # put dummy data here, we'll retry again at
                    # the bottom of this loop
                    # If the log files not exist yet continue, else exit.
                    if 'No files available for' not in log_data['status']:
                        print_table(log_data)
                        sys.exit(0)
                    log_data = {'results': '', 'offset': 0}

                if stream_parser is None:
                    offset = ShowLogs.default_stream_parser(log_data)
                else:
                    offset = stream_parser(log_data, status_code)

                # wait 2.5 sec before fetching more data again
                # if 200 status code, else break if 202
                time.sleep(2.5)
                if status_code == 202:
                    return

                params['offset'] = offset
                result, status_code = ShowLogs.api_call(
                    config, show_path,
                    stream=True,
                    session=sess,
                    params=params,
                    return_status_code=True,
                    console_log_follow=True
                )
                log_data = json.loads(result)
            except KeyboardInterrupt:
                # graceful exit on keyboard interrupt
                sys.exit(0)


class BaseList(Command):
    """Provides universal functionality to listing various objects
    """
    BASE_ARGS = {'count': 10, 'offset': None, 'asc': None}

    @classmethod
    def parser(cls, subparser, help_text, desc):
        list_objects = subparser.add_parser(LS.name, aliases=LS.aliases,
                                            help=help_text, description=desc)
        list_objects.add_argument("-n", "--count", type=int, default=10,
                                  help="Show up to n objects. Without the "
                                       "--asc flag, returns most recent "
                                       "objects. For unlimited set n=0. Can "
                                       "be used alongside the offset arg to "
                                       "implement pagination of objects "
                                       "returned. Ex: `ncloud m ls -o 25 "
                                       "-n 10` would return objects 16-25, "
                                       "and `ncloud m ls -o 25 -n 10 --asc` "
                                       "would return objects 25-34.")
        list_objects.add_argument("-o", "--offset", type=int,
                                  help="Where in the object pagination to "
                                       "start next. Represents an object id "
                                       "to return the next newest X results, "
                                       "where X = count. Used as a way to "
                                       "paginate object listings.")
        list_objects.add_argument("--asc", action="store_true",
                                  help="Displays objects in ascending "
                                       "order instead of the default "
                                       "descending order.")
        return list_objects


class Results(Command):
    """
    Model results: Retrieve results files -- model weights, callback outputs
    and neon log.
    Dataset results: Retrieve the original dataset in various formats.
    Batch prediction results: Retrieve metadata and output files.
    Interactive session results: Retrieve log files.
    Stream results: Retrieve stream result files.
    """

    def __init__(self, object_name, object_id_completer, url_path):
        """
            object_name: used to say what kind of results we are fetching
            url_path: used to determine what endpoint to hit
            object_id_completer: used to autocomplete object ids when hitting
                                 tab to see what you can get results for
        """
        self.object_name = object_name
        self.url_path = url_path
        self.object_id_completer = object_id_completer

    def parser(self, subparser):
        results_parser = subparser.add_parser(RESULTS.name,
                                              aliases=RESULTS.aliases,
                                              help=Results.__doc__,
                                              description=Results.__doc__)
        results_parser.add_argument(
            "object_id", type=int,
            help="ID of {} to retrieve results of.".format(self.object_name)
        ).completer = self.object_id_completer
        results_parser.add_argument(
            "-d", "--directory",
            help="Location to download files {directory}/results_files. "
                 "Defaults to current directory."
        ).completer = DirectoriesCompleter
        results_parser_mode = results_parser.add_mutually_exclusive_group()
        results_parser_mode.add_argument(
            "-u", "--url", action="store_true",
            help="Obtain URLs to directly download individual results."
        )
        results_parser_mode.add_argument(
            "-o", "--objects", action="store_true",
            help="Download objects directly to specified directory."
        )
        results_parser_mode.add_argument(
            "-z", "--zip", action="store_true",
            help="Retrieve a zip file of results."
        )
        results_parser_mode.add_argument(
            "-t", "--tar", action="store_true",
            help="Retrieve a tar file of results."
        )
        results_parser.add_argument(
            "-f", "--filter", action='append',
            help="Only retrieve files with names matching <filter>.  Note - "
                 "uses glob style syntax. Multiple --filter arguments will "
                 "be combined with logical or."
        )

        results_parser.set_defaults(
            func=self.arg_call, url_path=self.url_path)

    @staticmethod
    def list_results(config, results_path, vals):
        # default to listing results
        vals["format"] = "list"
        results = Results.api_call(
            config, results_path, params=vals, return_json=True)
        if results and 'result_list' in results:
            result_list = results['result_list']
            for result in result_list:
                result['last_modified'] = \
                    utc_to_local(result["last_modified"])
        return results

    @staticmethod
    def get_compressed_download(config, results_path, vals, stream, results,
                                directory, object_id, ext):
        results = Results.api_call(
            config, results_path, params=vals, stream=stream)
        filename = download_compressed(
            results, directory, object_id, ext, stream)
        return filename

    @staticmethod
    def call(config, object_id, filter=None, zip=None, tar=None,
             url=None, objects=None, directory=None, url_path=None):
        vals = {}
        results_path = os.path.join(url_path, str(object_id), "outputs")
        if filter:
            vals["filter"] = filter

        results = None
        if any((url, objects, zip, tar)):
            directory = directory or '.'
            if url or objects:
                vals["format"] = "url"
                results = Results.api_call(
                    config, results_path, params=vals, return_json=True)
                if objects:
                    download_objects(results, directory)
            elif zip or tar:
                ext = "zip" if zip else "tar"
                vals["format"] = ext
                stream = not zip
                filename = Results.get_compressed_download(
                    config, results_path, vals, stream, results, directory,
                    object_id, ext)
                valid = False
                # special retry handler here because we want to test retry
                # based on tarfile success
                # TODO: some way to combine with main request retrier?
                attempts = 0
                if ext == 'tar':
                    while not valid and attempts < 2:
                        # make sure valid tar, just in case tar
                        # stream got interrupted
                        try:
                            tarfile.open(filename).getnames()
                        except IOError:
                            # try again and see if helium has recovered
                            filename = Results.get_compressed_download(
                                config, results_path, vals, stream, results,
                                directory, object_id, ext)
                            attempts += 1
                            continue
                        break
                if attempts == 2:
                    print("Unable to retrieve tar file. Server "
                          "under maintenance.")
            if not url:
                return
        else:
            results = Results.list_results(config, results_path, vals)

        return results

    @staticmethod
    def display_after(config, args, res):
        if res and 'result_list' in res:
            if args.url:
                print("Public URLs will expire 1 hour from now.")
            print_table(res['result_list'])


class NoRespCommand(Command):
    @staticmethod
    def display_after(config, args, res):
        if not res:
            print_table({"error": "Error: no response from Helium"})
        else:
            print_table(res)


def build_subparser(name, aliases, hlp, classes, subparser):
    parser = subparser.add_parser(name, aliases=aliases, help=hlp,
                                  description=hlp)
    subsubparser = parser.add_subparsers(title=name + ' operations')
    for cls in classes:
        cls.parser(subsubparser)
