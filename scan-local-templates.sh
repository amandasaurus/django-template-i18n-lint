#! /usr/bin/env bash
# Scan for i18n strings everywhere in the current directory tree.

if [[ ${#} > 0 ]] && [[ `ls "$1"` = "" ]]; then
    # Bail out now if first arg is an invalid or empty directory
    echo ""
    echo "  usage:  $0 [root-dir [filename-pattern]]"
    echo ""
    echo "First arg should be a non-empty directory, or omitted entirely. Optional second arg is a "
    echo "filename pattern for your Django templates (if omitted, the default pattern is *.html)"
    echo ""
    echo "  examples:"
    echo "    $0                            # scans the current working directory"
    echo "    $0 ~/myproject/src/           # scans the specified directory"
    echo "    $0 ~/myproject/src/ *.tmpl    # scans the specified directory for .tmpl files"
    echo "    $0 . *.tmpl                   # scans the current working directory for .tmpl files"
    echo ""
    exit
fi

# search for templates using any pattern submitted (or *.html by default)
for f in `find "${1:-.}" -iname ${2:-*.html}`
do
    python django-template-i18n-lint.py $f
done
