
"""
.. module:: lex
.. moduleauthor:: Mario Vidov <mvidov@yahoo.com>


"""

import re


class LexerError(Exception):
    def __init__(self, text: str, line_num: int):
        self.text = text
        self.line_num = line_num

    def __str__(self):
        ln = 'Line %i:' % self.line_num
        return ln + self.text.splitlines()[self.line_num]


class Lexer:
    def __init__(self):
        tdasm_keywords = ['sizeof', 'struct', 'end', 'global']

        self.definitions = [
            ('new_line', r'\r\n|\n'),
            ('string', r'"[\s\w]*"'),
            ('directive', '#[_A-Za-z][_A-Za-z0-9]*'),
            ('equal', '='),
            ('comment', r';.*$'),
            ('lbracket', r'\['),
            ('rbracket', r']'),
            ('lcurly', r'\{'),
            ('rcurly', r'}'),
            ('comma', r','),
            ('minus', '-'),
            ('plus', '\+'),
            ('mul', '\*'),
            ('label', r'[_A-Za-z][_A-Za-z0-9]*:'),
            ('keyword', r'\b(%s)\b' % '|'.join(tdasm_keywords)),
            ('hex_num', r'0x[0-9A-Fa-f]+'),
            ('bin_num', r'[01]+[bB]'),
            ('float', r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'),
            ('num', r'[0-9]+'),
            ('period', '\.'),
            ('iden', r'[_A-Za-z][_A-Za-z0-9]*(\.[_A-Za-z][_A-Za-z0-9]*)*'),
            ('space', r' |\t')
        ]

        parts = []
        for name, part in self.definitions:
            parts.append('(?P<%s>%s)' % (name, part))
        self.regexp_string = "|".join(parts)
        self.regexp = re.compile(self.regexp_string, re.MULTILINE)

    def tokenize(self, text: str) -> list:
        """Function return list of lines, and every
        line consist of list of tokkens.
        token, token, token, ...
        token, token, token, ...
        ...
        token = (tok_type, tok_value, line_number)"""

        line_number = 0
        tokkens = []
        lines = []
        len_text = len(text)
        position = 0
        while True:
            match = self.regexp.match(text, position)
            if match is not None:
                position = match.end()
                for name, rexp in self.definitions:
                    m = match.group(name)
                    if m is not None:
                        if name == 'hex_num':
                            name = "num"
                            m = str(int(m, 16))
                        elif name == 'bin_num':
                            name = "num"
                            m = int(m[:len(m)-1], 2)
                            m = str(m)
                        elif name == 'string':
                            m = str(m[1:len(m)-1])
                        if m == '\n' or m == "\r\n":
                            line_number += 1
                            if len(tokkens) == 0:
                                continue
                            lines.append(tokkens)
                            tokkens = []
                            continue
                        tokkens.append((name, m, line_number))
                        break
            else:
                if position != len_text:
                    raise LexerError(text, line_number)
                if len(tokkens) > 0:
                    lines.append(tokkens)
                return lines
