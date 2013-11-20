import unittest
import django_template_i18n_lint

class DjangoTemplateI18nLintTestCase(unittest.TestCase):
    def test_simple(self):
        output = list(django_template_i18n_lint.non_translated_text("<h1>Foo</h1>"))
        self.assertEqual(output, [(1, 5, 'Foo')])

if __name__ == '__main__':
    unittest.main()
