import unittest
from unittest.mock import patch, Mock

from Familytree.family_creation import Family
from Familytree.individual import Person
from Familytree import variables
from tests import mock_member_creation


class TestFamilyTree(unittest.TestCase):

    def setUp(self):
        self.family_test = Family()

    def test_initialization(self):
        self.assertEqual(self.family_test.family, {})

    @patch('Familytree.family_creation.Person', return_value=(mock_member_creation(
        id=1, name='Baby', gender='Female')))
    def test_add_parent(self, mock_member):
        # if tree is empty
        # success case
        result = self.family_test.add_parent('Baby', 'Female')
        mock_member.assert_called_with(1, 'Baby', 'Female')

        self.assertEqual(
            isinstance(self.family_test.family.get('Baby', None), Mock),
            True
        )
        self.assertEqual(result, variables.PARENT_ADDITION_SUCCEEDED)

        # error case
        result = self.family_test.add_parent('wrongBaby', 'Female')
        self.assertEqual(
            isinstance(self.family_test.family.get('wrongBaby', None), Mock),
            False
        )
        self.assertEqual(result, variables.PERSON_NOT_FOUND)

    @patch('Familytree.family_creation.Person', return_value=mock_member_creation(
        id=2, name='Baby', gender='Male'))
    def test_add_child(self, mock_member):
        # if the name of new member already exists
        self.family_test.family['Baby'] = mock_member_creation(id=1, name='Baby', gender='Female')
        result = self.family_test.add_child('Baby', 'Male', 'Baby-mother')
        mock_member.assert_called_with(2, 'Baby', 'Male')
        self.assertEqual(
            isinstance(self.family_test.family.get('Baby', None), Mock),
            True
        )
        self.assertEqual(self.family_test.family['Baby'].id, 1)
        self.assertEqual(result, variables.CHILD_ADDITION_FAILED)

        # if either mother do not exist
        result = self.family_test.add_child('Baby-boy', 'Male', 'Baby-error')
        mock_member.assert_called_with(2, 'Baby-boy', 'Male')
        self.assertEqual(
            isinstance(self.family_test.family.get('Baby-error', None), Mock),
            False
        )
        self.assertEqual(result, variables.PERSON_NOT_FOUND)

        # if mothers gender isn't a valid one
        self.family_test.family['Baby'] = mock_member_creation(id=1, name='Baby', gender='Male')
        result = self.family_test.add_child('Baby-boy', 'Male', 'Baby')
        mock_member.assert_called_with(2, 'Baby-boy', 'Male')
        self.assertFalse(self.family_test.family['Baby'].gender in variables.Gender[variables.female])
        self.assertEqual(result, variables.CHILD_ADDITION_FAILED)

        # if spouse isn't assigned for a mother
        self.family_test.family['Baby'] = mock_member_creation(id=1, name='Baby', gender='Female')
        result = self.family_test.add_child('Baby-boy', 'Male', 'Baby')
        mock_member.assert_called_with(2, 'Baby-boy', 'Male')
        self.assertEqual(self.family_test.family['Baby'].spouse, None)
        self.assertEqual(result, variables.CHILD_ADDITION_FAILED)

        # success case
        self.family_test.family['Hubby'] = mock_member_creation(id=2, name='Hubby', gender='Male')
        self.family_test.family['Baby'].spouse = self.family_test.family['Hubby']
        self.family_test.family['Hubby'].spouse = self.family_test.family['Baby']
        result = self.family_test.add_child('Baby-boy', 'Male', 'Baby')
        mock_member.assert_called_with(3, 'Baby-boy', 'Male')
        self.assertEqual(
            isinstance(self.family_test.family.get('Baby-boy', None), Mock),
            True
        )
        self.assertEqual(result, variables.CHILD_ADDITION_SUCCEEDED)

        # for testing add_spouse method

    @patch('Familytree.family_creation.Person', return_value=mock_member_creation())
    def test_add_spouse(self, mock_member):
        # if name already exists
        self.family_test.family['Hubby'] = mock_member_creation(id=1, name='Hubby', gender='Male')
        result = self.family_test.add_spouse('Hubby', 'Female', 'Hubby')
        mock_member.assert_called_with(2, 'Hubby', 'Female')
        self.assertEqual(
            isinstance(self.family_test.family.get('Hubby', None), Mock),
            True
        )
        self.assertEqual(self.family_test.family['Hubby'].id, 1)
        self.assertEqual(result, variables.SPOUSE_ADDITION_FAILED)

        # if spouse doesnt exist
        result = self.family_test.add_spouse('Baby', 'Female', 'Hubby-error')
        mock_member.assert_called_with(2, 'Baby', 'Female')
        self.assertEqual(self.family_test.family.get('Hubby-error', None), None)
        self.assertEqual(result, variables.PERSON_NOT_FOUND)

        # if spouse id already assigned
        self.family_test.family['Baby'] = mock_member_creation(id=2, name='Baby', gender='Female')
        self.family_test.family['Hubby'].spouse = self.family_test.family['Baby']
        result = self.family_test.add_spouse('Baby2', 'Female', 'Hubby')
        mock_member.assert_called_with(3, 'Baby2', 'Female')
        self.assertNotEqual(self.family_test.family['Hubby'].spouse, None)
        self.assertEqual(result, variables.SPOUSE_ADDITION_FAILED)

        # success case
        self.family_test.family['Hubby'].spouse = None
        result = self.family_test.add_spouse('NewBaby', 'Female', 'Hubby')
        mock_member.assert_called_with(3, 'NewBaby', 'Female')
        self.assertEqual(result, variables.SPOUSE_ADDITION_SUCCEEDED)

        # for testing get relation ship method

    @patch('Familytree.family_creation.Person.get_relatives', side_effect=[
        None,
        [
            mock_member_creation(id=1, name="Ramesh"),
            mock_member_creation(id=2, name="Suresh")
        ]
    ])
    def test_get_relationship(self, mock_get_relationship):
        self.assertEqual(
            self.family_test.get_relationship("Ramesh", "brother_in_law"),
            variables.PERSON_NOT_FOUND
        )
        self.family_test.family["Ramesh"] = Person(1, "Ramesh", "Male")
        self.assertEqual(
            self.family_test.get_relationship("Ramesh", "Brother-In-Law"),
            variables.NONE
        )
        self.assertEqual(
            self.family_test.get_relationship("Ramesh", "Brother-In-Law"),
            "Ramesh Suresh"
        )
        mock_get_relationship.assert_called_with('Brother-In-Law')


if __name__ == "__main__":
    unittest.main()
