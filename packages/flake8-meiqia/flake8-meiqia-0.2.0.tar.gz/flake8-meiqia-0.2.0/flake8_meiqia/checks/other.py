import re

from flake8_meiqia import core


@core.flake8ext
def meiqia_no_cr(physical_line):
    """Checks there is no windows style line endings."""

    pos = physical_line.find('\r')
    if pos >= 0 and pos == len(physical_line) - 2:
        return pos, "MQ903: Windows style line endings not allowed"


_LOG_STRING_INTERPOLATION = re.compile(
    r".*(LOG|logger)\.(?:error|warn|warning|info|critical|exception|debug)"
    r"\([^,]*%[^,]*[,)]")


@core.flake8ext
@core.off_by_default
def hacking_delayed_string_interpolation(logical_line, noqa):
    """String interpolation should be delayed at logging calls.

    H904: LOG.debug('Example: %s' % 'bad')
    Okay: LOG.debug('Example: %s', 'good')
    """
    msg = ("MQ904: String interpolation should be delayed to be "
           "handled by the logging code, rather than being done "
           "at the point of the logging call. "
           "Use ',' instead of '%'.")

    if noqa:
        return

    if _LOG_STRING_INTERPOLATION.match(logical_line):
        yield 0, msg
