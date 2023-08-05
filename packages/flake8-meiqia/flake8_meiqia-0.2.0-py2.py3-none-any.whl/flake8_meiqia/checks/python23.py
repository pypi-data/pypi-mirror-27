from flake8_meiqia import core


@core.skip_on_py3
@core.flake8ext
def meiqia_python3x_except_compatible(logical_line, noqa):
    """Check for except statements to be Python 3.x compatible

    As of Python 3.x, the construct 'except x,y:' has been removed.
    Use 'except x as y:' instead.

    Okay: try:\n    pass\nexcept Exception:\n    pass
    Okay: try:\n    pass\nexcept (Exception, AttributeError):\n    pass
    MQ231: try:\n    pass\nexcept AttributeError, e:\n    pass
    Okay: try:\n    pass\nexcept AttributeError, e:  # noqa\n    pass
    """
    if noqa:
        return

    def is_old_style_except(logical_line):
        return (',' in logical_line and
                ')' not in logical_line.rpartition(',')[2])

    if (logical_line.startswith("except ") and
            logical_line.endswith(':') and
            is_old_style_except(logical_line)):
        yield 0, "MQ231: Python 3.x incompatible 'except x,y:' construct"
