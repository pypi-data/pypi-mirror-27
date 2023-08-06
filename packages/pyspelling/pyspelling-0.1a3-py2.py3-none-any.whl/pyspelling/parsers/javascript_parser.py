"""JavaScript parser."""
import re
import codecs
from pyspelling import parsers
import textwrap

RE_LINE_PRESERVE = re.compile(r"\r?\n", re.MULTILINE)
RE_JSDOC = re.compile(r"(?s)^/\*\*$(.*?)[ \t]*\*/", re.MULTILINE)
RE_COMMENT = re.compile(
    r'''(?x)
        (?P<comments>
            (?P<block>/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)                        # multi-line comments
          | (?P<start>^)?(?P<leading_space>[ \t]*)?(?P<line>//(?:[^\r\n])*)  # single line comments
        )
      | (?P<code>
            "(?:\\.|[^"\\])*"                                                # double quotes
            '(?:\\.|[^'\\])*'                                                # single quotes
          | .[^/"']*?                                                        # everything else
        )
    ''',
    re.DOTALL | re.MULTILINE
)


class JavaScriptParser(parsers.Parser):
    """JavaScript parser."""

    FILE_PATTERNS = ('*.js',)

    def __init__(self, options, default_encoding='ascii'):
        """Initialization."""

        self.blocks = options.get('block_comments', True) is True
        self.lines = options.get('line_comments', True) is True
        # self.strings = options.get('strings', False) is True
        self.group_comments = options.get('group_comments', False) is True
        self.jsdocs = options.get('jsdocs', False) is True
        super(JavaScriptParser, self).__init__(options, default_encoding)

    def _evaluate(self, m):
        """Search for comments."""

        g = m.groupdict()
        if g["code"]:
            text = g["code"]
            self.line_num += text.count('\n')
        else:
            if g['block']:
                if self.jsdocs:
                    m1 = RE_JSDOC.match(g['comments'])
                    if m1:
                        lines = []
                        for line in m1.group(1).splitlines(True):
                            l = line.lstrip()
                            lines.append(l[1:] if l.startswith('*') else l)
                        self.jsdoc_comments.append([''.join(lines), self.line_num])
                    elif self.blocks:
                        self.block_comments.append([g['block'][2:-2], self.line_num])
                elif self.blocks:
                    self.block_comments.append([g['block'][2:-2], self.line_num])
                self.line_num += g['comments'].count('\n')
            elif self.lines:
                if g['start'] is None:
                    self.line_comments.append([g['line'][2:], self.line_num])
                    self.line_num += g['comments'].count('\n')
                else:
                    # Cosecutive lines with only comments with same leading whitespace
                    # will be captured as a single block.
                    if (
                        self.group_comments and
                        self.line_num == self.prev_line + 1 and
                        g['leading_space'] == self.leading
                    ):
                        self.line_comments[-1][0] += '\n' + g['line'][2:]
                    else:
                        self.line_comments.append([g['line'][2:], self.line_num])
                    self.leading = g['leading_space']
                    self.line_num += g['comments'].count('\n')
                    self.prev_line = self.line_num
            else:
                self.line_num += g['comments'].count('\n')
            text = ''.join([x[0] for x in RE_LINE_PRESERVE.findall(g["comments"])])
        return text

    def find_comments(self, text):
        """Find comments."""

        return ''.join(map(lambda m: self._evaluate(m), RE_COMMENT.finditer(text)))

    def parse_file(self, source_file, encoding):
        """Parse HTML file."""

        content = []
        self.line_num = 1
        self.prev_line = -1
        self.leading = ''
        self.jsdoc_comments = []
        self.block_comments = []
        self.line_comments = []

        with codecs.open(source_file, 'r', encoding=encoding) as f:
            self.find_comments(f.read())
            for comment, line in self.jsdoc_comments:
                content.append(
                    parsers.SourceText(
                        textwrap.dedent(comment),
                        "%s (%d)" % (source_file, line),
                        encoding,
                        'jsdocs'
                    )
                )
            for comment, line in self.block_comments:
                content.append(
                    parsers.SourceText(
                        textwrap.dedent(comment),
                        "%s (%d)" % (source_file, line),
                        encoding,
                        'block-comment'
                    )
                )
            for comment, line in self.line_comments:
                content.append(
                    parsers.SourceText(
                        textwrap.dedent(comment),
                        "%s (%d)" % (source_file, line),
                        encoding,
                        'line-comment'
                    )
                )

        return content


def get_parser():
    """Get parser."""

    return JavaScriptParser
