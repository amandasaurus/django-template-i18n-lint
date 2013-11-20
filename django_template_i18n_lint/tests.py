import unittest
import django_template_i18n_lint

class DjangoTemplateI18nLintTestCase(unittest.TestCase):
    def _known_good_output(input_string, expected_output):
        def test(self):
            actual_output = list(django_template_i18n_lint.non_translated_text(input_string))
            self.assertEqual(actual_output, expected_output)
        test.__doc__ = "Input string {0} should give output of {1}".format(repr(input_string[:30]), repr(expected_output)[:30])
        return test

    testSimple = _known_good_output("<h1>Foo</h1>", [(1, 5, 'Foo')])
    testMultiWord = _known_good_output("<h1>Foo</h1><p>Bar</p>", [(1, 5, 'Foo'), (1, 16, 'Bar')])
    testMultiWordMultiLine = _known_good_output("<h1>Foo</h1>\n<p>Bar</p>", [(1, 5, 'Foo'), (2, 4, 'Bar')])


if __name__ == '__main__':
    unittest.main()
