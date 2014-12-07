"""
Unittests for django-template-i18n-lint.
"""
import unittest
import django_template_i18n_lint


def _known_good_output(input_string, expected_output):
    def test(self):
        actual_output = list(django_template_i18n_lint.non_translated_text(input_string))
        self.assertEqual(actual_output, expected_output)
    test.__doc__ = "Input string {0} should give output of {1}".format(
        repr(input_string[:30]), repr(expected_output)[:30])
    return test


class DjangoTemplateI18nLintTestCase(unittest.TestCase):
    """
    Unittests.
    """

    testSimple = _known_good_output("<h1>Foo</h1>", [(1, 5, 'Foo')])
    testMultiWord = _known_good_output("<h1>Foo</h1><p>Bar</p>", [(1, 5, 'Foo'), (1, 16, 'Bar')])
    testMultiWordMultiLine = _known_good_output("<h1>Foo</h1>\n<p>Bar</p>", [(1, 5, 'Foo'), (2, 4, 'Bar')])

    # Test things that shouldn't be included
    testTransOK = _known_good_output("<b>{% trans 'Foo' %}</b>", [])
    testBlocktransOK1 = _known_good_output("<b>{% blocktrans %}Foo{% endblocktrans %}</b>", [])
    testBlocktransOK2 = _known_good_output("<b>{% blocktrans with var=bar %}Foo{% endblocktrans %}</b>", [])
    testBlocktransOK3 = _known_good_output("<b>{% blocktrans with var as bar %}Foo{% endblocktrans %}</b>", [])
    testDjangoCustomTag = _known_good_output("{% load foo %}", [])
    testJS = _known_good_output("Foo<script>alert('Foo');</script>Bar", [(1, 1, 'Foo'), (1, 34, 'Bar')])
    testDjangoVar = _known_good_output("Foo{{ bar }}Baz", [(1, 1, 'Foo'), (1, 13, 'Baz')])
    testBooleanValuesOK1 = _known_good_output("<option selected>Option</option>",[(1, 18, 'Option')])
    testBooleanValuesOK2 = _known_good_output("<img src='my.jpg' ismap />",[])

    testNoHTMLAttrSingleQuote = _known_good_output("<form method='POST'>FOO</form>", [(1, 21, 'FOO')])
    testNoHTMLAttrDoubleQuote = _known_good_output("<form method=\"POST\">FOO</form>", [(1, 21, 'FOO')])
    testNoHTMLAttrNoQuote1 = _known_good_output("<form method=POST>FOO</form>", [(1, 19, 'FOO')])
    testNoHTMLAttrNoQuote2 = _known_good_output("<form method=post>FOO</form>", [(1, 19, 'FOO')])

    testNumbers = _known_good_output("<b>123.456,789</b>", [])
    
    testIssue17a = _known_good_output("<input type=\"submit\" value=\"Confirm\" class=\"btn btn-danger\" />", [(1, 29, 'Confirm')])
    testIssue17b = _known_good_output('<li><a href="https://twitter.com/localunews" class="icon-twitter" rel="tooltip" title="" data-placement="top" data-original-title="Twitter"><i class="fa fa-twitter"></i></a></li>', [(1, 132, 'Twitter')])


if __name__ == '__main__':
    unittest.main()
