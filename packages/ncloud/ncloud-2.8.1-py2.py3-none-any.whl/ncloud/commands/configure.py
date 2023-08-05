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
Configure subcommand.
"""
from backports.configparser import NoSectionError
from builtins import input
import getpass
import logging
from ncloud.commands.command import Command
from ncloud.config import (CFG_FILE, CFG_SEC_DEF, CFG_DEF_AUTH0_ID,
                           CFG_DEF_LEGACY_AUTH_HOST, CFG_SEC_USER,
                           DEF_NUM_THREADS, DEF_REQUEST_RETRIES,
                           DEF_UPLOAD_QUEUE_SIZE)
from ncloud.formatting.output import print_table

logger = logging.getLogger()


class Configure(Command):
    """
    Update stored configuration options like email, password, and tenant.
    One config option is allowed at a time.
    """
    @classmethod
    def parser(cls, subparser):
        config = subparser.add_parser("configure",
                                      help=Configure.__doc__,
                                      description=Configure.__doc__)
        config_options = config.add_mutually_exclusive_group()
        config_options.add_argument(
            '-l', "--list-hosts", action="store_true",
            help="List all Nervana cloud hosts known.")
        config_options.add_argument(
            '-c', "--change", action="store_true", help="Change the currently "
            "selected Nervana cloud config.")
        config_options.add_argument(
            '-a', "--add", nargs=1, help="Name of another Nervana cloud "
            "configuration. Useful for multiple tenant connections.")
        config_options.add_argument(
            '-s', "--select-host", nargs=1, help="Select configuration "
            "to use.")
        config_options.add_argument(
            '-p', "--print-config", action="store_true", help="Helper to "
            "output config file.")
        config_options.add_argument(
            '-r', "--rename", nargs=2, help="Old and new names for a "
            "config grouping.")
        config_options.add_argument(
            '-e', "--edit-host", help="Flag for selecting a host to edit. "
            "Ignored unless also passing in -t, -q, or -u")
        config_options.add_argument(
            '-t', "--num-threads", help="Set the number of threads to use "
            "for a host. If the --edit-host (-e) flag is not set, changes "
            "currently selected host. Defaults to {}.".format(
                DEF_NUM_THREADS), default=DEF_NUM_THREADS, type=int)
        config_options.add_argument(
            '-q', "--num-request-retries", help="Set the number of retries "
            "to use when making an api call. If the --edit-host (-e) flag is "
            "not set, changes currently selected host. Defaults to {}."
            .format(DEF_REQUEST_RETRIES), default=DEF_REQUEST_RETRIES,
            type=int)
        config_options.add_argument(
            '-u', "--upload-queue-size", help="Set the max size of the upload "
            "queue when uploading volume data (comparative to max open number "
            "of files). If the --edit-host (-e) flag is not set, changes "
            "currently selected host. Defaults to {}.".format(
                DEF_UPLOAD_QUEUE_SIZE),
            default=DEF_UPLOAD_QUEUE_SIZE, type=int)
        config.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, host, auth_host, tenant, api_ver, list_hosts,
             change, add, select_host, print_config,
             rename, edit_host, num_threads, num_request_retries,
             upload_queue_size):
        """
        Create/update stored configuration credentials.
        Prompts the user for info
        """
        if list_hosts:
            Configure.conf_list_hosts(config)
        elif select_host:
            Configure.conf_select_host(config, select_host[0], write_conf=True)
        elif print_config:
            Configure.print_config()
        elif rename:
            Configure.rename_section(
                config, rename[0], rename[1], write_conf=True)
        # want to reconfigure if user has no ncloudrc yet
        elif any((add, change)) or not config.get_tenant():
            Configure.configure(config, host, auth_host, tenant, api_ver,
                                change, add[0] if add else add)
        else:
            Configure.edit_defaults(
                config, edit_host, num_threads, num_request_retries,
                upload_queue_size)

    @classmethod
    def print_config(cls):
        with open(CFG_FILE, 'r') as f:
            print(f.read())

    @classmethod
    def rename_section(cls, config, old_section, new_section,
                       write_conf=False):
        conf = config.conf
        try:
            items = conf.items(old_section)
        except NoSectionError as e:
            print("Section: {} not in {}. Select from the following:".format(
                e.section, CFG_FILE))
            Configure.conf_list_hosts(config)
            exit(1)
        conf.add_section(new_section)
        for item in items:
            conf.set(new_section, item[0], item[1])
        conf.remove_section(old_section)
        if write_conf:
            config._write_config(conf)

    @classmethod
    def conf_select_host(cls, config, config_to_select, write_conf=False):
        conf = config.conf
        for section in conf.sections():
            if conf.get(section, "selected", fallback=None):
                conf.set(section, "selected", "False")
        try:
            conf.set(config_to_select, "selected", "True")
        except NoSectionError as e:
            print("Section: {} not in {}. Select from the following:".format(
                e.section, CFG_FILE))
            Configure.conf_list_hosts(config)
            exit(1)
        if write_conf:
            config._write_config(conf)

    @classmethod
    def edit_defaults(cls, config, edit_different_host, num_threads,
                      num_request_retries, upload_queue_size):
        conf = config.conf
        settings = old_settings = config.get_selected_section()
        if edit_different_host:
            # leverage select host logic to verify if actually a host to edit
            Configure.conf_select_host(config, edit_different_host)
            settings = config.get_selected_section()

        # cast here rather than above so we make sure user passes
        # in valid integers
        conf.set(settings, "num_threads", str(num_threads))
        conf.set(settings, "request_retries", str(num_request_retries))
        conf.set(settings, "upload_queue_size", str(upload_queue_size))
        Configure.conf_select_host(config, old_settings)
        config._write_config(conf)

    @classmethod
    def configure(cls, config, host, auth_host, tenant, api_ver,
                  change=False, add_new_config=None):
        conf = config.conf
        # silentmigration, also get rid of old auth link section name
        if not add_new_config and conf.has_section(CFG_DEF_LEGACY_AUTH_HOST):
            Configure.rename_section(
                config, CFG_DEF_LEGACY_AUTH_HOST, CFG_SEC_USER)
        current_settings = config.get_selected_section()
        current_config = add_new_config or config.get_selected_section()
        change = change or add_new_config
        if not conf.has_section(current_config):
            conf.add_section(current_config)
        defaults = {key: val for (key, val) in conf.items(current_settings)}
        if "client_id" in defaults:
            idfield = "username"
            data = {"client_id": defaults["client_id"]}
        else:
            # legacy`
            idfield = "email"
            data = {"client_id": CFG_DEF_AUTH0_ID}

        logger.info("Updating {0} configuration.  Defaults are in "
                    "'[]'".format(CFG_FILE))

        fields = [idfield, "password", "tenant"] + (["host"] if change else [])
        for item in fields:
            default = defaults.get(item, "")
            if item == "tenant" and default == "" and tenant is not None:
                default = tenant
            if item == "password":
                res = getpass.getpass("{0}: ".format(item))
            else:
                res = input("{0} [{1}]: ".format(item, default))
            if len(res.strip()) == 0 and len(default.strip()) > 0:
                res = default
            conf.set(current_config, item, res)
            data[item] = res
            if item == "tenant" and default == "":
                # no prior tenant default set, use the one just provided
                conf.set(CFG_SEC_DEF, "tenant", res)
        if idfield == "email":
            data["username"] = data["email"]
        Configure.conf_select_host(config, current_config)

        config.get_token(refresh=True, data=data)

    @classmethod
    def conf_list_hosts(cls, config):
        conf = config.conf
        print_table({'Hosts': ", ".join([val for val in conf.sections()])})
