from __future__ import print_function, unicode_literals, division

import difflib
import re

__all__ = ['MarkdownProcessor', 'BBCodeRemover', 'LtagCleaner', 'BBCodeRemover2']


class Converter(object):
    def __init__(self, pattern, repl, flags=0):
        self.re = re.compile(pattern=pattern, flags=flags)
        self.repl = repl
        self.flags = flags

    def __call__(self, text):
        return self.re.sub(repl=self.repl, string=text)


class MarkdownProcessor(object):
    modifiers = []
    ready_for_production = False
    comment = NotImplemented

    def __call__(self, markdown, field, locale, wiki_object):
        result = self.modify(markdown)

        d = difflib.Differ()
        diff = d.compare(markdown.replace("\r", "").split("\n"),
                         result.replace("\r", "").split("\n"))
        for dd in diff:
            if dd[0] != " ":
                print(dd)

        return result

    def modify(self, markdown):
        result = "\n" + markdown

        for modifier in self.modifiers:
            result = modifier(result)

        result = result[1:]
        return result


class BBCodeRemover2(MarkdownProcessor):
    def __init__(self):

        self.modifiers = [
            Converter(pattern=r'\n?\[hr\]\n?',
                      repl=r"\n----\n",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[(/?)sub\]',
                      repl=r"<\1sub>",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[(/?)sup\]',
                      repl=r"<\1sup>",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[(/?)s\]',
                      repl=r"<\1s>",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[p]',
                      repl=r"<p></p>",
                      flags=re.IGNORECASE),
        ]


class BBCodeRemover(MarkdownProcessor):
    ready_for_production = True
    comment = "Replace BBcode by Markdown"

    _tests = [
        {
            "source": "un texte en [b]gras [/b]et un en [i]italique[/i] [i][/i] ",
            "expected": "un texte en **gras** et un en *italique*  ",
        },
        {
            "source": "un texte en [b][i]gras et italique[/i][/b]",
            "expected": "un texte en ***gras et italique***",
        },
        {
            "source": "[center][b]outside![/b][/center]",
            "expected": "**[center]outside![/center]**",
        },
        {
            "source": "[url=http:google.fr][i]outside![/i][/url]",
            "expected": "*[outside!](http:google.fr)*",
        },
        {
            "source": "[b]\r\ngrep!\r\n[/b]",
            "expected": "\r\n**grep!**\r\n",
        },
        {
            "source": "#c coucou ##c s",
            "expected": "# coucou ##c s",
        },
        {
            "source": "line\n####c coucou ##c s",
            "expected": "line\n#### coucou ##c s",
        },
        {
            "source": "###coucou",
            "expected": "###coucou",
        },
        {
            "source": "###C bien",
            "expected": "###C bien",
        },

        {
            "source": "[url=]http://www.zone-di-tranquillita.ch/[/url]",
            "expected": "http://www.zone-di-tranquillita.ch/ "
        },
        {
            "source": "[url]http://www.google.com[/url]",
            "expected": "http://www.google.com "
        },
        {
            "source": "[url]http://www.google.com[/url] x [url]http://www.google2.com[/url]",
            "expected": "http://www.google.com  x http://www.google2.com "
        },
        {
            "source": "[url=http://www.google.com]google[/url]",
            "expected": "[google](http://www.google.com)",
        },
        {
            "source": "[url=http://www.google.com]google[/url] et [url=http://www.google2.com]google2[/url]",
            "expected": "[google](http://www.google.com) et [google2](http://www.google2.com)"
        },
        {
            "source": "[url]http://www.google.com?a=b&c=d[/url] and [url=http://www.google.com?a=b!c]pas touche[/url]",
            "expected": "[url]http://www.google.com?a=b&c=d[/url] and [url=http://www.google.com?a=b!c]pas touche[/url]"
        },
        {
            "source": "[url]http://www.google.com?a=b;d[/url] et [url]pas.touche.fr[/url]",
            "expected": "[url]http://www.google.com?a=b;d[/url] et [url]pas.touche.fr[/url]"
        },
        {
            "source": "[url]http://www.google.com?a=b&c=d[/url] x [url]http://www.google2.com?a=b&c=d[/url]",
            "expected": "[url]http://www.google.com?a=b&c=d[/url] x [url]http://www.google2.com?a=b&c=d[/url]"
        },
        {
            "source": "[url=http://www.google.com?a=b&c=d]google[/url]",
            "expected": "[url=http://www.google.com?a=b&c=d]google[/url]",
        },
        {
            "source": "[url=http://www.google.com?a=b&c=d]go[/url] et [url=http://www.google2.com?a=b&c=d]o[/url]",
            "expected": "[url=http://www.google.com?a=b&c=d]go[/url] et [url=http://www.google2.com?a=b&c=d]o[/url]"
        },
        {
            "source": "[email]dev@camptocamp.org[/email]",
            "expected": "[dev@camptocamp.org](mailto:dev@camptocamp.org)"
        },
        {
            "source": "[email=dev@camptocamp.org]email[/email]",
            "expected": "[email](mailto:dev@camptocamp.org)"
        }
    ]

    def do_tests(self):
        def do_test(source, expected):
            result = self.modify(source)
            if result != expected:
                print("Source   ", repr(source))
                print("Expected ", repr(expected))
                print("Result   ", repr(result))
                print()

        for test in self._tests:
            do_test(**test)

    def __init__(self):
        def get_typo_cleaner(bbcode_tag, markdown_tag):
            converters = [

                Converter(
                    pattern=r'\[' + bbcode_tag + r'\]\[/' + bbcode_tag + '\]',
                    repl=r"",
                    flags=re.IGNORECASE),

                Converter(pattern=r'\n *\[' + bbcode_tag + r'\] *',
                          repl=r"\n[" + bbcode_tag + r"]",
                          flags=re.IGNORECASE),

                Converter(pattern=r'\[' + bbcode_tag + r'\] +',
                          repl=r" [" + bbcode_tag + r"]",
                          flags=re.IGNORECASE),

                Converter(pattern=r' +\[/' + bbcode_tag + r'\]',
                          repl=r"[/" + bbcode_tag + r"] ",
                          flags=re.IGNORECASE),

                Converter(pattern=r'\r\n\[/' + bbcode_tag + r'\]',
                          repl=r"[/" + bbcode_tag + r"]\r\n",
                          flags=re.IGNORECASE),

                Converter(pattern=r'\[' + bbcode_tag + r'\] *\r\n([^\*\#]?)',
                          repl=r"\r\n[" + bbcode_tag + r"]\1",
                          flags=re.IGNORECASE),

                Converter(
                    pattern=r'\[center] *\[' + bbcode_tag + r'\]([^\n\r\*\`]*?)\[/' + bbcode_tag + '\] *\[/center]',
                    repl=markdown_tag + r"[center]\1[/center]" + markdown_tag,
                    flags=re.IGNORECASE),

                Converter(
                    pattern=r'\[url=(.*?)] *\[' + bbcode_tag + r'\]([^\n\r\*\`]*?)\[/' + bbcode_tag + '\] *\[/url]',
                    repl=markdown_tag + r"[url=\1]\2[/url]" + markdown_tag,
                    flags=re.IGNORECASE),

                Converter(
                    pattern=r'\[' + bbcode_tag + r'\]([^\n\r\*\`]*?)\[/' + bbcode_tag + '\]',
                    repl=markdown_tag + r"\1" + markdown_tag,
                    flags=re.IGNORECASE),

                Converter(
                    pattern=r'\[' + bbcode_tag + r'\]([^\n\r\*\`]+?)\r?\n([^\n\r\*\`]+?)\[/' + bbcode_tag + '\]',
                    repl=markdown_tag + r"\1\n\2" + markdown_tag,
                    flags=re.IGNORECASE),

                Converter(
                    pattern=r'\[' + bbcode_tag + r'\]' +
                            r'([^\n\r\*\`]+?)\r?\n' +
                            r'([^\n\r\*\`]+?)\r?\n' +
                            r'([^\n\r\*\`]+?)\[/' + bbcode_tag + '\]',
                    repl=markdown_tag + r"\1\n\2\n\3" + markdown_tag,
                    flags=re.IGNORECASE),
            ]

            def result(markdown):
                for converter in converters:
                    markdown = converter(markdown)

                return markdown

            return result

        self.modifiers = [
            get_typo_cleaner("b", "**"),
            get_typo_cleaner("i", "*"),

            Converter(pattern=r'\[i\]\*\*([^\n\r\*\`]*?)\*\*\[/i\]',
                      repl=r"***\1***",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[(/?)imp\]',
                      repl=r"[\1important]",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[(/?)warn\]',
                      repl=r"[\1warning]",
                      flags=re.IGNORECASE),

            Converter(pattern=r'(^|\n)(#+)c +',
                      repl=r"\1\2 "),

            Converter(pattern=r'\[url=?\](http|www)([^\n\&\;\!]*?)\[/url\]',
                      # r'\[url\](.*?)\[/url\]' for all urls
                      repl=r"\1\2 ",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[url\=([^\n\&\;\!]*?)\](.*?)\[\/url\]',
                      # r'\[url\=(.*?)\](.*?)\[\/url\]' for all urls
                      repl=r"[\2](\1)",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[email\](.*?)\[/email\]',
                      repl=r"[\1](mailto:\1)",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\[email\=(.*?)\](.*?)\[\/email\]',
                      repl=r"[\2](mailto:\1)",
                      flags=re.IGNORECASE),

        ]


class LtagCleaner(MarkdownProcessor):
    ready_for_production = False
    comment = "Simplify L# syntax"

    _tests = [
        {
            "source": "L#{} | 1 | 2\nL# | 1 | 2\n\nautre texte",
            "result": "L#{} | 1 | 2\nL# | 1 | 2\n\nautre texte"
        },
        {
            "source": "L#{} | 1 | 2\n\nL# | 1 | 2\n",
            "result": "L#{} | 1 | 2\nL# | 1 | 2\n"
        },
        {
            "source": "L#{} | 1\n2 | 2\nL# | 1 | 2\n\n\nautre texte",
            "result": "L#{} | 1<br>2 | 2\nL# | 1 | 2\n\n\nautre texte",
        },
        {
            "source": "L#{} |\n 12 | 2\nL#{} | 1 \n| 2\n",
            "result": "L#{} | 12 | 2\nL#{} | 1 | 2\n"
        },
        {
            "source": "L#{} | 1 L# 2 | 2\nL#{} | 1 | 2\n3\n",
            "result": "L#{} | 1 L# 2 | 2\nL#{} | 1 | 2<br>3\n"
        },
        {
            "source": "L#{} | 12 | 2\nL#{} | 1 | 2\n3\n\n4",
            "result": "L#{} | 12 | 2\nL#{} | 1 | 2<br>3\n\n4"
        },
        {
            "source": "L#{}:1::2\n##Titre",
            "result": "L#{}|1|2\n##Titre"
        },
        {
            "source": "L#{} |1::2",
            "result": "L#{} |1|2"
        },
        {
            "source": "L#{}:1::2",
            "result": "L#{}|1|2"
        },
        {
            "source": "L#{}|1:2::3||R#4||||5::::6",
            "result": "L#{}|1:2|3|R#4|5|6"
        },
        {
            "source": "L#{} 1:2",
            "result": "L#{} |1:2"
        },
        {
            "source": "L#{}|1::2",
            "result": "L#{}|1|2"
        },
        {
            "source": "L#{}::1::2||3:: ::5|6| |7::8:aussi 8|9",
            "result": "L#{}|1|2|3| |5|6| |7|8:aussi 8|9"
        },
        {
            "source": "L#~ plein ligne !:: \n| fds : \n\n| {} a la fin",
            "result": "L#~ plein ligne !:: <br>| fds : \n\n| {} a la fin",
        },
        {
            "source": "L#{} || [[touche/pas|au lien]] : stp::merci ",
            "result": "L#{} | [[touche/pas|au lien]] : stp|merci "
        },
    ]

    _numbering_postfixs = ["", "12", "+3", "+", "-25", "-+2", "+2-+1", "bis",
                           "bis2", "*5bis", "+5bis", "_", "+bis",
                           "''", "+''", "!", "2!", "+2!", "="]

    def do_tests(self):
        def do_test(source, expected):
            result = self.modify(source)
            if result != expected:
                print("source   ", repr(source))
                print("expected ", repr(expected))
                print("result   ", repr(result))
                print()

        for postfix in self._numbering_postfixs:
            for test in self._tests:
                source = test["source"].format(postfix, postfix)
                expected = test["result"].format(postfix, postfix)
                do_test(source, expected)

    def __init__(self):
        self.modifiers = []

        newline_converters = [
            Converter(pattern=r'\nL#(.*)\n\nL#',
                      repl=r"\nL#\1\nL#",
                      flags=re.IGNORECASE),

            Converter(pattern=r'\nR#(.*)\n\nR#',
                      repl=r"\nR#\1\nR#",
                      flags=re.IGNORECASE),
        ]

        # replace leading `:` by `|`
        leading_converter = Converter(pattern=r'^([LR]#)([^\n \|\:]*)( *)\:+',
                                      repl=r"\1\2\3|",
                                      flags=re.IGNORECASE)

        # replace no first sep by `|`
        no_leading_converter = Converter(
            pattern=r'^([LR]#)([^\n \|\:]*)( +)([^\:\|\ ])',
            repl=r"\1\2\3|\4",
            flags=re.IGNORECASE)

        # replace multiple consecutives  `:` or  `|` by `|`
        multiple_converter = Converter(
            pattern=r'( *)(<br>)?( *)([\:\|]{2,}|\|)( *)(<br>)?( *)',
            repl=r"\1\3|\5\7",
            flags=re.IGNORECASE)

        def modifier(markdown):
            markdown = markdown.replace("\r\n", "\n")
            markdown = markdown.replace("\r", "\n")

            for converter in newline_converters:
                markdown = converter(markdown)

            lines = markdown.split("\n")
            result = []

            last_line_is_ltag = False
            for line in lines:
                if line.startswith("L#") or line.startswith("R#"):
                    result.append(line)
                    last_line_is_ltag = True

                elif line.startswith("#") or line == "":
                    result.append(line)
                    last_line_is_ltag = False

                elif not last_line_is_ltag:
                    last_line_is_ltag = False
                    result.append(line)

                else:  # last_line_is_ltag is true here
                    result[len(result) - 1] += "<br>" + line

            markdown = "\n".join(result)

            lines = markdown.split("\n")
            result = []

            for line in lines:
                if (line.startswith("L#") or line.startswith("R#")) and line[
                    2] != "~":
                    line = leading_converter(line)
                    line = no_leading_converter(line)
                    line = multiple_converter(line)

                result.append(line)

            return "\n".join(result)

        self.modifiers.append(modifier)


class ColorAndUnderlineRemover(MarkdownProcessor):
    ready_for_production = True
    comment = "Remove color and u tags"

    _tests = [
        {
            "source": "test [u]underlines[/u] and [color=#FFdd1E]color[/color] et [color=red]color[/color]",
            "expected": "test underlines and color et color"
        },
    ]

    def do_tests(self):
        def do_test(source, expected):
            result = self.modify(source)
            if result != expected:
                print("source   ", repr(source))
                print("expected ", repr(expected))
                print("result   ", repr(result))
                print()

        for test in self._tests:
            do_test(**test)

    def __init__(self):
        self.modifiers = []
        self.modifiers.append(
            Converter(pattern=r'\[/?(color|u)(=#?[a-zA-Z0-9]{3,10})?\]',
                      repl=r"",
                      flags=re.IGNORECASE), )
