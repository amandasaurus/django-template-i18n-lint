"""
Prints out all
"""

import re
import sys
from optparse import make_option
import os.path

from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module


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

         # Any html attribute that's not value or title
        |[a-z:-]+?(?<!alt)(?<!value)(?<!title)(?<!summary)='[^']*?'

         # Any html attribute that's not value or title
        |[a-z:-]+?(?<!alt)(?<!value)(?<!title)(?<!summary)="[^"]*?"

         # HTML opening tag
        |<[\w:]+

         # End of a html opening tag
        |>
        |/>

         # closing html tag
        |</.*?>

         # any django template variable
        |{{.*?}}

         # HTML doctype
        |<!DOCTYPE.*?>

         # IE specific HTML
        |<!--\[if.*?<!\[endif\]-->

         # HTML comment
        |<!--.*?-->

         # HTML entities
        |&[a-z]{1,10};

         # CSS style
        |<style.*?</style>

         # another common template comment
        |{\#.*?\#}
        )""",

    # MULTILINE to match across lines and DOTALL to make . include the newline
    re.MULTILINE | re.DOTALL | re.VERBOSE)

# Stops us matching non-letter parts, e.g. just hypens, full stops etc.
LETTERS = re.compile("\w")


def location(str, pos):
    """Given a string str and an integer pos, find the line number and character in that line that correspond to pos"""
    lineno, charpos = 1, 1
    counter = 0
    for char in str:
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


def replace_strings(filename):
    full_text_lines = []
    for index, message in enumerate(GOOD_STRINGS.split(open(filename).read())):
        if index % 2 == 0 and re.search("\w", message):
            before, message, after = re.match("^(\s*)(.*?)(\s*)$", message, re.DOTALL).groups()
            message = message.strip().replace("\n", "").replace("\r", "")
            change = raw_input("Make '%s' translatable? [Y/n] " % message)
            if change == 'y' or change == "":
                message = '%s{%% trans "%s" %%}%s' % (before, message, after)
        full_text_lines.append(message)

    full_text = "".join(full_text_lines)
    save_filename = filename.split(".")[0] + "_translated.html"
    open(save_filename, 'w').write(full_text)
    print "Fully translated! Saved as: %s" % save_filename


def non_translated_text(filename):
    template = open(filename).read()
    offset = 0

    # Find the parts of the template that don't match this regex
    # taken from http://www.technomancy.org/python/strings-that-dont-match-regex/
    for index, match in enumerate(GOOD_STRINGS.split(template)):
        if index % 2 == 0:

            # Ignore it if it doesn't have letters
            if LETTERS.search(match):
                lineno, charpos = location(template, offset)
                yield (lineno, charpos, match.strip().replace("\n", "").replace("\r", "")[:120])

        offset += len(match)


def print_strings(filename, stdout=sys.stdout):
    for lineno, charpos, message in non_translated_text(filename):
        stdout.write("%s:%s:%s:%s" % (filename, lineno, charpos, message))


class Command(BaseCommand):
    args = '<filename>'
    help = 'A simple script to find non-i18n text in a Django template'
    option_list = BaseCommand.option_list + (
        make_option('-e', '--exclude', dest='exclude',action='append', default=[],
            help='App to exclude (use multiple --exclude to exclude multiple apps).'),
        make_option(
            "-r",
            "--replace",
            action="store_true",
            dest="replace",
            help="Ask to replace the strings in the file.",
            default=False),
    )

    def handle(self, *app_labels, **options):
        #if len(args) != 1:
        #    raise CommandError("Please specify a template file.")
        #if options['replace']:
        #    replace_strings(args[0])
        #else:
        #    print_strings(args[0])
        exclude = options.get('exclude',[])

        apps = self._get_apps(app_labels, exclude)

        templates_dirs = []

        for app in apps:
            module = import_module(app)
            module_dir = os.path.dirname(module.__file__)
            templates_dirs.append(os.path.join(module_dir, 'templates'))

        for templates_dir in templates_dirs:
            templates = self._find_files(templates_dir)

            #print templates_dir, ':'

            for template_name in templates:
                #print '    ', template_name
                print_strings(os.path.join(templates_dir, template_name), self.stdout)


    def _get_apps(self, app_labels, exclude=[]):
        from django.conf import settings

        apps = dict([(app.split('.')[-1], app) for app in settings.INSTALLED_APPS])

        try:
            [apps.pop(app_label) for app_label in exclude]
        except KeyError, key:
            raise CommandError("Unknown application: %s in excluded apps" % key)

        if len(app_labels) > 0:
            try:
                apps = [apps.pop(app_label) for app_label in app_labels]
            except KeyError, key:
                raise CommandError("Unknown application: %s" % key)
        else:
            apps = apps.values()

        return apps

    def _find_files(self, location):
        """Recursively finds files at location. Returns list of relative to
        filename files"""
        files = []
        for dirpath, dirnames, filenames in os.walk(location):
            for filename in filenames:
                file_name = os.path.join(dirpath, filename) \
                                   .replace(location, '') \
                                   .strip('/\\')
                files.append(file_name)
        return files
