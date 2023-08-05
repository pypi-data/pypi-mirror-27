import re
import tokenize

from flake8_meiqia import core


_EMPTY_LINE_RE = re.compile("^\s*(#.*|$)")


@core.flake8ext
def meiqia_has_only_comments(physical_line, filename, lines, line_number):
    """Check for empty files with only comments

    MQ104: empty file with only comments
    """
    if line_number == 1 and all(map(_EMPTY_LINE_RE.match, lines)):
        return 0, "MQ104: File contains nothing but comments"


_TODO_RE = re.compile(r'''
    (?P<leading>[@\W])?
    (?P<todo>TODO|ToDo|todo|FIXME|FixMe|fixme|XXX|xxx)
    (?P<trailing>\()?''', re.VERBOSE)


@core.flake8ext
def meiqia_todo_format(physical_line, tokens):
    """Checks for 'TODO()' in comments.

    Okay: # TODO(timonwong)
    MQ101: # TODO
    MQ101: # TODO xxx
    MQ101: # TODO (timonwong)
    MQ101: # @ToDo
    """

    for token_type, text, start_index, _, _ in tokens:
        if token_type == tokenize.COMMENT:
            m = _TODO_RE.search(text)
            if not m:
                continue

            groups = m.groupdict()
            todo_name = groups['todo'].upper()
            if (groups['leading'] == '@' or groups['todo'] != todo_name or
                    groups['trailing'] != '('):
                if groups['leading'] == '@':
                    err_pos = m.start('leading') + start_index[1]
                else:
                    err_pos = m.start('todo') + start_index[1]

                return err_pos, "MQ101: Use %s(NAME)" % todo_name


_AUTHOR_TAG_RE = (re.compile("^\s*#\s*@?(a|A)uthors?:"),
                  re.compile("^\.\.\s+moduleauthor::"))


@core.flake8ext
def no_author_tags(physical_line):
    """Checks that no author tags are used.

    MQ105: Don't use author tags
    """
    for regex in _AUTHOR_TAG_RE:
        if regex.match(physical_line):
            physical_line = physical_line.lower()
            pos = physical_line.find('moduleauthor')
            if pos < 0:
                pos = physical_line.find('author')
            return pos, "MQ105: Don't use author tags"
