import requests
from semantic_version import Version

from nodebin.blueprints.api10.exceptions import ApiException


CNPM_TIMEOUT = 10
NODE_INDEX = 'https://npm.taobao.org/mirrors/node/index.json'
NODE_ADDR = 'https://npm.taobao.org/mirrors/node/v{0}/node-v{0}-{1}.tar.xz'


def parse_node(platform, ext):
    # Get node version and bin from CNPM
    rv = requests.get(NODE_INDEX, timeout=CNPM_TIMEOUT)
    if rv.status_code != 200:
        raise ApiException(
            'CNPM service returns {} status code'.format(rv.status_code)
        )

    # Process response
    response, result = rv.json(), []
    for package in response:
        _ = dict()
        _['number'] = _process_version(package['version'])
        _['url'] = _process_url(package['files'], _['number'], platform)
        result.append(_)
    return result


def _process_version(version):
    # Remove additional v in versions
    if version.startswith('v'):
        version = version[1:]

    # Check sementic verison validness
    version = str(Version(version))

    return version


def _process_url(files, version, platform):
    """
    :param files is a list
    """
    # Convert platform to appropriate key
    if platform == 'linux-x64':
        target = 'linux-x64'
    elif platform == 'darwin-x64':
        # osx-x64-tar is in tar.gz or tar.xz format
        # osx-x64-pkg is in pkg format
        target = 'osx-x64-tar'

    if target in files:
        return NODE_ADDR.format(version, platform)
    return ''
