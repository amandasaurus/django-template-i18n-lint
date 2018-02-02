#! /usr/bin/env python
"""
Prints out all
"""

import html
import os
import re
from optparse import OptionParser


def location(string, pos):
    """
    Given a string str and an integer pos, find the line number and character
    in that line that correspond to pos
    """
    lineno, charpos = 1, 1
    counter = 0
    for char in string:
        if counter == pos:
            return lineno, charpos
        elif char == '\n':
            lineno += 1
            charpos = 1
            counter += 1
        else:
            charpos += 1
            counter += 1
    return lineno, charpos


# Things that are OK:
GOOD_STRINGS = re.compile(
    r"""
          # django comment
       ( {%\ comment\ %}.*?{%\ endcomment\ %}

         # already translated text
        |{%\ ?blocktrans.*?{%\ ?endblocktrans\ ?%}

         # any django template function (catches {% trans ..) aswell
        |{%.*?%}

         # CSS
        |<style.*?</style>

         # JS
        |<script.*?</script>

         # A html title or value attribute that's been translated
        |(?:value|title|summary|alt)="{%\ ?trans.*?%}"

         # A html title or value attribute that's just a template var
        |(?:value|title|summary|alt)="{{.*?}}"

         # An <option> value tag
        |<option[^<>]+?value="[^"]*?"

         # Any html attribute that's not value or title (single quote, double quote and html5 quoteless)
         # NB at the start we want to grab any trailing quote from the previous attribute
         # FIXME This will fail for some quoteless attr values.
        |(?:['"]\W+)?[a-z:-]+?(?<!alt)(?<!value)(?<!title)(?<!summary)=(?:'(?:{{.*?}}|{%.*?%}|[^']*)'|"(?:{{.*?}}|{%.*?%}|[^"]*)+"|[a-zA-Z\.]+)

         # The actual alt/value/title tag itself cannot be translated, but the value should be
         # Treat data-title/data-original-title etc as equivalanets. Think this is some bootstrap thing & HTML5
        |(?:['"]\W+)?(?:data-|data-original-)?(?:alt|value|title|summary)=['"]?

         # Boolean attributes
        |<[^<>]+?(?:checked|selected|disabled|readonly|multiple|ismap|defer|async|declare|noresize|nowrap|noshade|compact|hidden|itemscope|autofocus|autoplay|controls|download)[^<>]*?>

         # HTML opening tag
        |<[\w:]+

         # End of a html opening tag
         # NB: catching end of quote from last attribute
        |(?:['"]\W*)?/?>

         # closing html tag
        |</.*?>

         # any django template variable
        |{{.*?}}

         # any django template tag
        |{%.*?%}

         # any angular.js template
        |\[\[.*?\]\]

         # HTML doctype
        |<!DOCTYPE.*?>

         # IE specific HTML
        |<!--\[if.*?<!\[endif\]-->

         # HTML comment
        |<!--.*?-->

         # HTML entities
        |&[a-z]{1,10};

        # HTML entities
        |&\#x[0-9]{1,10};

         # CSS style
        |<style.*?</style>

         # another common template comment
        |{\#.*?\#}
        )""",

    # MULTILINE to match across lines and DOTALL to make . include the newline
    re.MULTILINE | re.DOTALL | re.VERBOSE | re.IGNORECASE)

# Stops us matching non-letter parts, e.g. just hypens, full stops etc.
LETTERS = re.compile(r"[^\W\d_]")

LEADING_TRAILING_WHITESPACE = re.compile("(^\W+|\W+$)")

HTML_ENTITIES = re.compile(r"\&[a-zA-Z]{2,25}\;")


def split_into_good_and_bad(template):
    for index, match in enumerate(GOOD_STRINGS.split(template)):
        yield (index, match)


def split_trailing_space(string):
    """
    Given a string, returns a tuple of 3 string:
    the leading whitespace, middle, and trailing whitespace
    """
    results = LEADING_TRAILING_WHITESPACE.split(string)
    if len(results) == 1:
        # no spaces
        return ('', string, '')
    elif len(results) == 3:
        if not results[0] and results[2]:
            # only leading whitespace
            return (results[1], results[2], '')
        elif results[0] and not results[2]:
            # only trailing
            return ('', results[0], results[1])
        else:
            raise NotImplementedError("Unknown case: %r %r" % (string, results))
    elif len(results) == 5:
        # leading and trailing whitespace
        return (results[1], results[2], results[3])
    else:
        raise NotImplementedError("Unknown case: %r %r" % (string, results))


def wrap_message(message):
    if '\n' in message:
        return '{% blocktrans %}' + message.replace('"', '\\"') + '{% endblocktrans %}'
    else:
        return '{% trans "' + message.replace('"', '\\"') + '" %}'


def replace_strings(filename, overwrite=False, force=False, accept=None):
    if accept is None:
        accept = []

    full_text_lines = []
    with open(filename) as fp:
        content = fp.read()

    offset = 0
    ignore_lines = find_ignored_lines(content)

    for index, string in split_into_good_and_bad(content):
        if index % 2 == 1:
            full_text_lines.append(string)
            offset += len(string)
            continue

        # Ignore it if it doesn't have letters
        m = LETTERS.search(string)
        if not m:
            full_text_lines.append(string)
            offset += len(string)
            continue

        # split out the leading whitespace and trailing
        leading_whitespace, message, trailing_whitespace = split_trailing_space(string)
        full_text_lines.append(leading_whitespace)

        # Find location of first letter
        lineno, charpos = location(string, offset+m.span()[0])

        if any(r.match(message) for r in accept):
            full_text_lines.append(message)
        elif lineno in ignore_lines:
            full_text_lines.append(message)
        elif force:
            full_text_lines.append(wrap_message(message))
        else:
            change = input("Make %r translatable? [Y/n] " % message).lower()
            if change in ('y', 'yes', ''):
                full_text_lines.append(wrap_message(message))
            else:
                full_text_lines.append(message)

        full_text_lines.append(trailing_whitespace)
        offset += len(string)

    full_text = "".join(full_text_lines)
    if overwrite:
        save_filename = filename
    else:
        save_filename = filename.split(".")[0] + "_translated.html"
    open(save_filename, 'w').write(full_text)
    print("Fully translated! Saved as: %s" % save_filename)


def find_ignored_lines(template):
    lines = set()
    for m in re.finditer(r'{#\s*notrans\s*#}', template):
        offset = m.span()[0]
        lineno, charpos = location(template, offset)
        lines.add(lineno)
    return lines


def non_translated_text(template):
    offset = 0
    ignore_lines = find_ignored_lines(template)

    # Find the parts of the template that don't match this regex
    # taken from http://www.technomancy.org/python/strings-that-dont-match-regex/
    for index, match in split_into_good_and_bad(template):
        if index % 2 == 0:

            # Ignore it if it doesn't have letters
            m = LETTERS.search(match)
            if m:
                # Get location of first letter
                lineno, charpos = location(template, offset+m.span()[0])
                if lineno in ignore_lines:
                    offset += len(match)
                    continue
                yield (lineno, charpos, match.strip().replace("\n", "").replace("\r", "")[:120])

        offset += len(match)


def print_strings(filename, accept=None):
    if accept is None:
        accept = []

    with open(filename) as fp:
        file_contents = fp.read()

    for lineno, charpos, message in non_translated_text(file_contents):
        if any(r.match(message) for r in accept):
            continue
        print("%s:%s:%s:%s" % (filename, lineno, charpos, message))


def filenames_to_work_on(directory, exclude_filenames):
    """Return list of files in directory that we should look at"""
    files = []
    for dirpath, dirs, filenames in os.walk(directory):
        for fname in filenames:
            if fname.endswith('.html') or fname.endswith('.txt'):
                if fname not in exclude_filenames:
                    files.append(os.path.join(dirpath, fname))
    return files


def replace_html_entities(filename):
    with open(filename) as fp:
        content = fp.read()
    for entity in set(HTML_ENTITIES.findall(content)):
        # exclude &nbsp;. It's doesn't readable :)
        if entity == '&nbsp;':
            continue
        replacement = html.unescape(entity)
        # replace only 1 char
        if len(replacement) != 1:
            continue
        content = content.replace(entity, replacement)
    with open(filename, 'w') as fp:
        fp.write(content)


def parse_argv():
    parser = OptionParser(usage="usage: %prog [options] <filenames>")
    parser.add_option(
        "-r", "--replace",
        action="store_true",
        dest="replace",
        help="Ask to replace the strings in the file.",
        default=False)
    parser.add_option(
        "-o", "--overwrite",
        action="store_true",
        dest="overwrite",
        help=(
            "When replacing the strings, overwrite the original file."
            "If not specified, the file will be saved in a seperate file named X_translated.html"
        ),
        default=False)
    parser.add_option(
        "-f", "--force",
        action="store_true",
        dest="force",
        help="Force to replace string with no questions",
        default=False)
    parser.add_option(
        "-e", "--exclude",
        action="append",
        dest="exclude_filename",
        help="Exclude these filenames from being linted",
        default=[]
    )
    parser.add_option(
        "-x", "--accept",
        action="append",
        dest="accept",
        help="Exclude these regexes from results",
        default=[])
    parser.add_option(
        "-s", "--specialchars",
        action="store_true",
        dest="specialchars",
        help="Replace all HTML entities to UTF-8.",
        default=False)
    return parser.parse_args()


def main(options, args):
    # Create a list of files to check
    if len(args) == 0:
        args = [os.getcwd()]
    files = []
    for arg in args:
        if os.path.isdir(arg):
            files = filenames_to_work_on(arg, options.exclude_filename)
        elif arg not in options.exclude_filename:
            files.append(arg)

    accept_regexes = [re.compile(r) for r in options.accept]

    for filename in files:
        if options.specialchars:
            replace_html_entities(filename)
        if options.replace:
            replace_strings(filename, overwrite=True, force=options.force, accept=accept_regexes)
        else:
            print_strings(filename, accept=accept_regexes)


if __name__ == '__main__':
    options, args = parse_argv()
    main(options, args)
