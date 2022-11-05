from urllib.parse import urlencode


URL_TEMPLATE = 'https://github.com/totaldebug/CfDnsSync/issues/new?template=bug_report.yml&{}'


def bug_url():
    from cfdnssync.util.versions import (cfu_version, py_platform,
                                             py_version)

    q = urlencode({
        'os': py_platform(),
        'python': py_version(),
        'version': cfu_version(),
    })

    return URL_TEMPLATE.format(q)


def bug_report():
    url = bug_url()

    print("Click the below link to log a bug report:")
    print('')
    print(url)
