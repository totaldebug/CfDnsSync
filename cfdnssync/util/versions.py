def py_version():
    from platform import python_version

    return python_version()


def py_platform():
    from platform import platform

    return platform(terse=True, aliased=True)


def cfu_version():
    from cfdnssync import __version__

    return __version__
