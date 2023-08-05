__version__ = '0.2.0'


def flake8ext(f):
    f.name = 'flake8_meiqia'
    f.version = __version__
    f.skip_on_py3 = False
    if not hasattr(f, 'off_by_default'):
        f.off_by_default = False
    return f


def off_by_default(f):
    """Decorator to turn check off by default.

    To enable the check use the flake8 select setting in
    tox.ini.

    flake8 documentation:
    http://flake8.readthedocs.org/en/latest/extensions.html.
    """
    f.off_by_default = True
    return f


def skip_on_py3(f):
    f.skip_on_py3 = True
    return f
