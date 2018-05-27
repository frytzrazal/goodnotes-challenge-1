import unittest
from lww_element_set import LwwElementSet


class TestLwwElementSetScenarios(unittest.TestCase):
    """Test cases for scenarios in using the LwwElementSet.
        A set instantiated in each test case simulates a different node/server in the network.

        This set of test cases looks at the final set that is resolved for each node"""

    def test_add(self):
        s1 = LwwElementSet()
        s1.add('Groot')
        self.assertEqual(s1.get_final_set(), {'Groot'})

        # adding the same element again should have no effect in final set
        s1.add('Groot')
        self.assertEqual(s1.get_final_set(), {'Groot'})

    def test_remove(self):
        s1 = LwwElementSet()
        s1.add('Rocket')
        s1.remove('Rocket')
        self.assertEqual(s1.get_final_set(), set())

        # Removing from an empty set should have no effect in final set
        s1.remove('Rocket')
        self.assertEqual(s1.get_final_set(), set())

    def test_merge_commutative(self):
        s1 = LwwElementSet()
        s2 = LwwElementSet()
        s1.add('Groot')
        s2.add('Rocket')

        s1_merge = s1.merge(s2)

        s1 = LwwElementSet()
        s2 = LwwElementSet()
        s1.add('Groot')
        s2.add('Rocket')

        s2_merge = s2.merge(s1)

        # Merging one way or the other should result to the same state
        self.assertEqual(s1_merge, s2_merge)

    def test_merge_add_basic(self):
        s1 = LwwElementSet()
        s2 = LwwElementSet()

        # Each adds their own element
        s1.add('Groot')
        s2.add('Rocket')

        s1.merge(s2)
        self.assertEqual(s1.get_final_set(), {'Groot', 'Rocket'})

        # Merge again. Merge should be idempotent
        s1.merge(s2)
        self.assertEqual(s1.get_final_set(), {'Groot', 'Rocket'})

        # Merge back. Both sets should have the same state now
        s2.merge(s1)
        self.assertEqual(s1, s2)

    def test_merge_remove_basic(self):
        s1 = LwwElementSet()
        s2 = LwwElementSet()

        # s1 adds-removes, s2 should not have the element
        s1.add('Groot')
        s1.remove('Groot')

        s2.merge(s1)
        self.assertEqual(s2.get_final_set(), set())

    def test_add_remove(self):
        s1 = LwwElementSet()
        s2 = LwwElementSet()

        # s1 adds element but s2 removes it
        s1.add('Groot')
        s2.merge(s1)
        s2.remove('Groot')

        # s1 should also see it removed after merge
        s1.merge(s2)
        self.assertEqual(s2.get_final_set(), set())

    def test_add_remove_2(self):
        s1 = LwwElementSet()
        s2 = LwwElementSet()

        # s1 adds element but s2 removes it
        s1.add('Groot')
        s2.merge(s1)
        s2.remove('Groot')

        # then s1 adds the element again, after s2 does the removal
        s1.add('Groot')

        # the last write of the element should be in effect
        # since it happened after the removal
        s1.merge(s2)
        self.assertEqual(s1.get_final_set(), {'Groot'})

    def test_add_remove_3(self):
        s1 = LwwElementSet()
        s2 = LwwElementSet()

        s1.add('Groot')

        s2.add('Groot') # s2 adds its own and removes it right after
        s2.remove('Groot') # Removes element even though s2 does not see it
        s1.merge(s2)

        # s2's element is the last written
        # so the addition and removal gets reflected back
        self.assertEqual(s1.get_final_set(), set())

if __name__ == '__main__':
    unittest.main()