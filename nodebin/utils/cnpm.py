import requests
from semantic_version import Version


CNPM_TIMEOUT = 10
NODE_INDEX = 'https://npm.taobao.org/mirrors/node/index.json'
NODE_ADDR = 'https://npm.taobao.org/mirrors/node/v{0}/node-v{0}-{1}.tar.gz'


# TODO: Exception is handled in application
def cnpm2dict(platform, txt, latest, range_):
    # Get node version and bin from CNPM
    rv = requests.get(NODE_INDEX, timeout=CNPM_TIMEOUT)
    if rv.status_code != 200:
        raise Exception(
            'CNPM service returns {} status code'.format(rv.status_code)
        )

    # Process response
    response, results = rv.json(), []
    for package in response:
        _ = dict()
        _['number'] = _process_version(package['version'])
        _['url'] = _process_url(
            files=package['files'], version=_['number'], platform=platform
        )

        # Only output if url is valid
        if _['url']:
            results.append(_)

    # Filter by range
    #if range_:
    #    results = filter(lambda result: Version(result))

    # Filter by latest
    if latest:
        results = sorted(
            results, key=lambda result: Version(result['number']), reverse=True
        )[0]

    # Output diffent format
    if txt:
        # Convert to list for postprocess since latest only returns one
        if type(results) is dict:
            results = [results]

        results = '\n'.join(
            ['{} {}'.format(package['number'], package['url']) for package in results]
        )
    return results


def _process_version(version):
    # Remove additional v in versions
    if version.startswith('v'):
        version = version[1:]

    # Check semantic verison validness
    version = str(Version(version))

    return version


def _process_url(files, version, platform):
    """
    :param files should be list
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
