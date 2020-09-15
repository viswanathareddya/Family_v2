import unittest
from Familytree.individual import Person
from Familytree import variables
from unittest.mock import patch, Mock
from tests import mock_member_creation


class Testperson(unittest.TestCase):

    def setUp(self):
        self.person = Person(1, "Jane", "Female")

    def test_initialization(self):
        # check instance
        self.assertEqual(isinstance(self.person, Person), True)

        # check properties
        self.assertEqual(self.person.id, 1)
        self.assertEqual(self.person.name, "Jane")
        self.assertEqual(self.person.gender, "Female")
        self.assertEqual(self.person.mother, None)
        self.assertEqual(self.person.father, None)
        self.assertEqual(self.person.spouse, None)
        self.assertEqual(self.person.children, [])

    def test_assign_mother(self):
        mother_error_case = "error_value"
        mother_error_male_case = Person(2, "male_person", "Male")
        mother_success_case = Person(3, "Mother", "Female")

        # error case
        self.assertRaises(ValueError, self.person.assign_mother, mother_error_case)
        self.assertRaises(ValueError, self.person.assign_mother, mother_error_male_case)

        # success case
        self.person.assign_mother(mother_success_case)
        self.assertEqual(self.person.mother.name, "Mother")
        self.assertTrue(self.person.mother.gender, "Female")

    def test_assign_father(self):
        father_error_case = "error_value"
        father_error_female_case = Person(2, "female_father", "Female")
        father_success_case = Person(3, "Father", "Male")

        # error cases
        self.assertRaises(ValueError, self.person.assign_father, father_error_case)
        self.assertRaises(ValueError, self.person.assign_father, father_error_female_case)

        # success case
        self.person.assign_father(father_success_case)
        self.assertEqual(self.person.father.name, "Father")
        self.assertTrue(self.person.father.gender, "Male")

    def test_assign_spouse(self):
        spouse_error_case = "error_value"
        spouse_error_same_gender = Person(2, "same_gender_spouse", "Female")
        spouse_success_case = Person(3, "Husband", "Male")

        # error cases
        self.assertRaises(ValueError, self.person.assign_spouse, spouse_error_case)
        self.assertRaises(ValueError, self.person.assign_spouse, spouse_error_same_gender)

        # success case
        self.person.assign_spouse(spouse_success_case)
        self.assertEqual(self.person.spouse.name, "Husband")
        self.assertEqual(self.person.spouse.gender, "Male")

    def test_add_children(self):
        child_error_case = "error_Case"
        child_success_case = Person(4, "Daughter", "Female")

        # error case
        self.assertRaises(ValueError, self.person.add_children, child_error_case)

        # success case
        self.person.add_children(child_success_case)
        self.assertEqual(len(self.person.children), 1)
        self.assertEqual(self.person.children[0].name, "Daughter")
        self.assertEqual(self.person.children[0].gender, "Female")

    def test_get_paternal_grandmother(self):
        child = Person(7, "alpha", "Male")
        father = Person(8, "beta", "Male")
        grandmother = Person(9, "charlie", "Female")

        # error cases
        self.assertEqual(child.get_paternal_grandmother(), None)

        child.father = father
        self.assertEqual(child.get_paternal_grandmother(), None)

        child.father.mother = grandmother
        self.assertEqual(child.get_paternal_grandmother(), grandmother)

    def test_get_maternal_grandmother(self):
        child = Person(7, "alpha", "Male")
        mother = Person(8, "beta", "Female")
        grandmother = Person(9, "charlie", "Female")

        # error cases
        self.assertEqual(child.get_paternal_grandmother(), None)

        child.mother = mother
        self.assertEqual(child.get_paternal_grandmother(), None)

        child.mother.mother = grandmother
        self.assertEqual(child.get_maternal_grandmother(), grandmother)

    def test_get_spouse_mother(self):
        member = Person(7, "alpha", "Male")
        spouse = Person(8, "alpha_spouse", "Female")
        spouse_mother = Person(9, "alpha_spousemother", "Female")

        # error cases
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(), spouse_mother)

    @patch('Familytree.individual.Person.get_paternal_grandmother', side_effect=[
        None,
        mock_member_creation(),
        mock_member_creation(children=[Person(3, "Father", "Male")]),
        mock_member_creation(children=[
            Person(3, "Father", "Male"),
            Person(4, "Uncle", "Male")
        ]),
        mock_member_creation(children=[
            Person(3, "Father", "Male"),
            Person(4, "Uncle", "Male"),
            Person(5, "Aunt", "Female")
        ])
    ])
    def test_get_paternal_aunt(self, mock_paternal_grandmother):
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(
            isinstance(self.person.get_paternal_grandmother, Mock),
            True
        )
        self.assertEqual(self.person.get_paternal_aunt(), [])
        self.assertEqual(self.person.get_paternal_aunt(), [])
        self.assertEqual(self.person.get_paternal_aunt(), [])
        self.assertEqual(self.person.get_paternal_aunt(), [])

        paternal_aunts = self.person.get_paternal_aunt()
        self.assertEqual(len(paternal_aunts), 1)
        self.assertEqual(paternal_aunts[0].name, "Aunt")
        self.assertTrue(paternal_aunts[0].gender in variables.Gender[variables.female])

        # to check that the mock_get_paternal_grandmother was called instead
        # of self.member.get_paternal_grandmother
        mock_paternal_grandmother.assert_called_with()

    @patch('Familytree.individual.Person.get_paternal_grandmother', side_effect=[
        None,
        mock_member_creation(),
        mock_member_creation(children=[Person(3, "Father", "Male")]),
        mock_member_creation(children=[
            Person(3, "Aunt", "Female"),
            Person(4, "Father", "Male")
        ]),
        mock_member_creation(children=[
            Person(3, "Father", "Male"),
            Person(4, "Uncle", "Male"),
            Person(5, "Aunt", "Female")
        ])
    ])
    def test_get_paternal_uncle(self, mock_paternal_grandmother):
        self.person.father = Person(3, "Father", "Male")
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(
            self.person.get_paternal_grandmother, Mock),
            True
        )

        self.assertEqual(self.person.get_paternal_uncle(), [])
        self.assertEqual(self.person.get_paternal_uncle(), [])
        self.assertEqual(self.person.get_paternal_uncle(), [])
        self.assertEqual(self.person.get_paternal_uncle(), [])

        paternal_uncle = self.person.get_paternal_uncle()
        self.assertEqual(len(paternal_uncle), 1)
        self.assertEqual(paternal_uncle[0].name, "Uncle")
        self.assertTrue(paternal_uncle[0].gender in variables.Gender[variables.male])

        # to check that the mock_get_paternal_grandmother was called instead
        # of self.member.get_paternal_grandmother
        mock_paternal_grandmother.assert_called_with()

    @patch('Familytree.individual.Person.get_maternal_grandmother', side_effect=[
        None,
        mock_member_creation(),
        mock_member_creation(children=[Person(3, "Mother", "Female")]),
        mock_member_creation(children=[
            Person(3, "Mother", "Female"),
            Person(4, "Uncle", "Male")
        ]),
        mock_member_creation(children=[
            Person(3, "Mother", "Female"),
            Person(4, "Uncle", "Male"),
            Person(5, "Aunt", "Female")
        ])
    ])
    def test_get_maternal_aunt(self, mock_maternal_grandmother):
        self.person.mother = Person(3, "Mother", "Female")
        # check if get_maternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(
            self.person.get_maternal_grandmother, Mock),
            True
        )

        self.assertEqual(self.person.get_maternal_aunt(), [])
        self.assertEqual(self.person.get_maternal_aunt(), [])
        self.assertEqual(self.person.get_maternal_aunt(), [])
        self.assertEqual(self.person.get_maternal_aunt(), [])

        maternal_aunts = self.person.get_maternal_aunt()
        self.assertEqual(len(maternal_aunts), 1)
        self.assertEqual(maternal_aunts[0].name, "Aunt")
        self.assertTrue(maternal_aunts[0].gender in variables.Gender[variables.female])

        # to check that the mock_get_maternal_grandmother was called instead of
        # self.member.get_maternal_grandmother
        mock_maternal_grandmother.assert_called_with()

    @patch('Familytree.individual.Person.get_maternal_grandmother', side_effect=[
        None,
        mock_member_creation(),
        mock_member_creation(children=[Person(3, "Mother", "Female")]),
        mock_member_creation(children=[
            Person(3, "Aunt", "Female"),
            Person(4, "Mother", "Female")
        ]),
        mock_member_creation(children=[
            Person(3, "Mother", "Female"),
            Person(4, "Uncle", "Male"),
            Person(5, "Aunt", "Female")
        ])
    ])
    def test_get_maternal_uncle(self, mock_maternal_grandmother):
        # check if get_maternal_grandmother has been replaced by a mock
        self.assertEqual(
            isinstance(self.person.get_maternal_grandmother, Mock),
            True
        )

        self.assertEqual(self.person.get_maternal_uncle(), [])
        self.assertEqual(self.person.get_maternal_uncle(), [])
        self.assertEqual(self.person.get_maternal_uncle(), [])
        self.assertEqual(self.person.get_maternal_uncle(), [])

        maternal_uncle = self.person.get_maternal_uncle()
        self.assertEqual(len(maternal_uncle), 1)
        self.assertEqual(maternal_uncle[0].name, "Uncle")
        self.assertTrue(maternal_uncle[0].gender in variables.Gender[variables.male])

        # to check that the mock_get_maternal_grandmother was called
        # instead of self.member.get_maternal_grandmother
        mock_maternal_grandmother.assert_called_with()

    @patch('Familytree.individual.Person.get_siblings', return_value=[
        mock_member_creation(
            name="Alpha", gender='Male', spouse=mock_member_creation(
                name="Beta", gender='Female', spouse=mock_member_creation(
                    name="Alpha")
            )
        ),
        mock_member_creation(
            name="Charlie", gender='Female', spouse=mock_member_creation(
                name="Delta", gender='Male', spouse=mock_member_creation(
                    name="Charlie")
            )
        ),
        mock_member_creation(
            name="Charlie", gender='Female'
        )
    ])
    def test_get_sibling_spouses(self, mock_siblings):
        self.assertEqual(len(self.person.get_sibling_spouses()), 2)
        mock_siblings.assert_called_with()

    def test_get_spouse_siblings(self):
        self.assertEqual(len(self.person.get_spouse_siblings()), 0)
        self.person.spouse = mock_member_creation(name="Wife")

        spouse_siblings = [
            mock_member_creation(name="Alpha"),
            mock_member_creation(name="Beta")
        ]
        self.assertEqual(len(spouse_siblings), 2)

    @patch('Familytree.individual.Person.get_spouse_siblings', return_value=[
        mock_member_creation(name="Alpha", gender='Male'),
        mock_member_creation(name="Beta", gender='Female')
    ])
    @patch('Familytree.individual.Person.get_sibling_spouses', return_value=[
        mock_member_creation(name="Charlie", gender='Male'),
        mock_member_creation(name="Delta", gender='Female')
    ])
    def test_get_brother_in_law(self, mock_sibling_spouses,
                                mock_spouse_siblings):
        self.assertEqual(len(self.person.get_brother_in_law()), 2)
        mock_sibling_spouses.assert_called_with()
        mock_spouse_siblings.assert_called_with()

    @patch('Familytree.individual.Person.get_spouse_siblings', return_value=[
        mock_member_creation(name="Alpha", gender='Male'),
        mock_member_creation(name="Beta", gender='Female')
    ])
    @patch('Familytree.individual.Person.get_sibling_spouses', return_value=[
        mock_member_creation(name="Charlie", gender='Male'),
        mock_member_creation(name="Delta", gender='Female')
    ])
    def test_get_sister_in_law(self, mock_sibling_spouses,
                               mock_spouse_siblings):
        self.assertEqual(len(self.person.get_sister_in_law()), 2)
        mock_sibling_spouses.assert_called_with()
        mock_spouse_siblings.assert_called_with()

    def test_get_son(self):
        person = Person(5, "Father", "Male")
        son = Person(7, "Son", "Male")
        daughter = Person(8, "Daughter", "Female")

        self.assertEqual(person.get_son(), [])
        person.children.append(daughter)
        self.assertEqual(person.get_son(), [])
        person.children.append(son)
        sons = person.get_son()
        self.assertEqual(len(sons), 1)
        self.assertEqual(sons[0].name, "Son")
        self.assertTrue(sons[0].gender in variables.Gender[variables.male])

    def test_get_daughter(self):
        person = Person(5, "Mother", "Female")
        son = Person(7, "Son", "Male")
        daughter = Person(9, "Daughter", "Female")

        self.assertEqual(person.get_daughter(), [])
        person.children.append(son)
        self.assertEqual(person.get_daughter(), [])
        person.children.append(daughter)
        daughters = person.get_daughter()
        self.assertEqual(len(daughters), 1)
        self.assertEqual(daughters[0].name, "Daughter")
        self.assertTrue(daughters[0].gender in variables.Gender[variables.female])

    def test_get_siblings(self):
        person = Person(5, "Dummy", "Male")
        mother = Person(9, "Mother", "Female")
        son = Person(7, "Son", "Male")
        daughter = Person(7, "Daughter", "Female")

        self.assertEqual(person.get_siblings(), [])
        person.mother = mother
        self.assertEqual(person.get_siblings(), [])
        mother.children.extend([person, son, daughter])
        person.mother = mother
        siblings = person.get_siblings()
        self.assertEqual(len(siblings), 2)

    @patch('Familytree.individual.Person.get_father', return_value=["Father"])
    @patch('Familytree.individual.Person.get_mother', return_value=["Mother"])
    @patch('Familytree.individual.Person.get_spouse', return_value=["Spouse"])
    @patch('Familytree.individual.Person.get_siblings', return_value=["brother", "sister"])
    @patch('Familytree.individual.Person.get_daughter', return_value=["daughter", "daughters"])
    @patch('Familytree.individual.Person.get_son', return_value=["son", "sonny"])
    @patch('Familytree.individual.Person.get_sister_in_law', return_value=["sis", "sissy"])
    @patch('Familytree.individual.Person.get_brother_in_law', return_value=["brother", "bro"])
    @patch('Familytree.individual.Person.get_maternal_uncle', return_value=["uncles", "uncle"])
    @patch('Familytree.individual.Person.get_maternal_aunt', return_value=["aunt", "aunty"])
    @patch('Familytree.individual.Person.get_paternal_uncle', return_value=["uncle", "uncles"])
    @patch('Familytree.individual.Person.get_paternal_aunt', return_value=["aunty", "aunt"])
    def test_get_relationship(self, mock_get_paternal_aunt,
                              mock_get_paternal_uncle,
                              mock_get_maternal_aunt, mock_get_maternal_uncle,
                              mock_get_brother_in_law, mock_get_sister_in_law,
                              mock_get_son, mock_get_daughter,
                              mock_get_siblings, mock_get_spouse,
                              mock_get_mother, mock_get_father):
        person = Person(1, "man", "Male")

        self.assertEqual(person.get_paternal_aunt(), ["aunty", "aunt"])
        mock_get_paternal_aunt.assert_called_with()

        self.assertEqual(person.get_paternal_uncle(), ["uncle", "uncles"])
        mock_get_paternal_uncle.assert_called_with()

        self.assertEqual(person.get_maternal_aunt(), ["aunt", "aunty"])
        mock_get_maternal_aunt.assert_called_with()

        self.assertEqual(person.get_maternal_uncle(), ["uncles", "uncle"])
        mock_get_maternal_uncle.assert_called_with()

        self.assertEqual(person.get_brother_in_law(), ["brother", "bro"])
        mock_get_brother_in_law.assert_called_with()

        self.assertEqual(person.get_sister_in_law(), ["sis", "sissy"])
        mock_get_sister_in_law.assert_called_with()

        self.assertEqual(person.get_son(), ["son", "sonny"])
        mock_get_son.assert_called_with()

        self.assertEqual(person.get_daughter(), ["daughter", "daughters"])
        mock_get_daughter.assert_called_with()

        self.assertEqual(person.get_siblings(), ["brother", "sister"])
        mock_get_siblings.assert_called_with()

        self.assertEqual(person.get_spouse(), ["Spouse"])
        mock_get_spouse.assert_called_with()

        self.assertEqual(person.get_mother(), ["Mother"])
        mock_get_mother.assert_called_with()

        self.assertEqual(person.get_father(), ["Father"])
        mock_get_father.assert_called_with()


if __name__ == '__main__':
    unittest.main()
