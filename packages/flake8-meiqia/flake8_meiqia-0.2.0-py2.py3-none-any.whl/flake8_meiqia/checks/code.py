import re

from flake8_meiqia import core

MUTABLE_DEFAULT_ARGS_RE = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")


@core.flake8ext
def meiqia_no_mutable_default_args(logical_line):
    """Checks for common mutable default args.

    MQ301: def f(a, b={}, c=[])
    """

    m = MUTABLE_DEFAULT_ARGS_RE.search(logical_line)
    if not m:
        return

    msg = "MQ301: Use of mutable type in function definition is not allowed"
    yield (0, msg)
