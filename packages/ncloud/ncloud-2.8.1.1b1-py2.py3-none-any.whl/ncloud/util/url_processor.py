from six.moves.urllib.parse import urlparse


def url_processor(url):
    domain = urlparse(url).hostname.split('.')[0]
    result_url = url.replace(domain, 'dlstudio')
    return result_url
