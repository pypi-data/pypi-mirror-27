from django.test import TestCase

from server.models import TestDiff


class ModelDiffTestCase(TestCase):
    def setUp(self):
        self.obj = TestDiff(name='Foo')
        self.obj.save()

    def _no_change(self):
        self.assertEqual(self.obj.has_changed, False)
        self.assertEqual(list(self.obj.changed_fields), [])

    def test_no_change(self):
        self.assertEqual(self.obj.name, 'Foo')
        self._no_change()

    def test_name_change(self):
        self.obj.name = 'Bar'
        self.assertEqual(self.obj.name, 'Bar')
        self.assertEqual(self.obj.has_changed, True)
        self.assertTrue('name' in self.obj.changed_fields)

        self.assertFalse(self.obj.recorded_name_change)
        self.obj.save()
        self.assertTrue(self.obj.recorded_name_change)
        self._no_change()

    def test_number_change(self):
        self.obj.number = 100
        self.assertEqual(self.obj.number, 100)
        self.assertEqual(self.obj.has_changed, True)
        self.assertTrue('number' in self.obj.changed_fields)

        self.obj.save()
        self._no_change()
