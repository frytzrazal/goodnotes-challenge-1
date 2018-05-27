import unittest
from lww_element_set import LwwElementSet


class TestLwwElementSet(unittest.TestCase):
    """Unit test for LwwElementSet class"""

    def setUp(self):
        self.s1 = LwwElementSet()
        self.s2 = LwwElementSet()

    def test_add(self):
        self.s1.add('Starlord')

        # 'Starlord' should be in add_set
        self.assertTrue(any('Starlord' in elem for elem in self.s1.add_set))
        self.assertEqual(self.s1.get_final_set(), {'Starlord'})

    def test_add_ts(self):
        self.s1.add_ts('Starlord', 100)
        
        self.assertIn(('Starlord', 100), self.s1.add_set)

    def test_remove(self):
        self.s1.add('Starlord')
        self.s1.remove('Starlord')

        self.assertTrue(any('Starlord' in elem for elem in self.s1.remove_set))
        self.assertEqual(self.s1.get_final_set(), set())

    def test_remove_ts(self):
        self.s1.add('Starlord')
        self.s1.remove_ts('Starlord', 100)

        self.assertIn(('Starlord', 100), self.s1.remove_set)

    def test_merge(self):
        self.s1.add('Starlord')
        self.s2.add('Drax')
        self.s2.remove('Drax')

        self.s1.merge(self.s2)
        self.assertTrue(self.s2.add_set.issubset(self.s1.add_set))
        self.assertTrue(self.s2.remove_set.issubset(self.s1.remove_set))

    def test_resolve_add(self):
        self.s1.add_ts('Starlord', 500)
        self.s1.add_ts('Starlord', 501)
        self.s1.resolve_add()

        self.assertEqual(self.s1.add_set, {('Starlord', 501)})

    def test_resolve_remove(self):
        self.s1.remove_ts('Drax', 800)
        self.s1.remove_ts('Drax', 801)
        self.s1.resolve_remove()

        self.assertEqual(self.s1.remove_set, {('Drax', 801)})

    def test_get_final_set(self):
        self.s1.add('Starlord')
        self.s1.add('Gamora')
        self.s1.add('Drax')
        self.s1.remove('Gamora')
        self.s1.add('Rocket')

        self.assertEqual(self.s1.get_final_set(), {'Starlord', 'Drax', 'Rocket'})

if __name__ == '__main__':
    unittest.main()



