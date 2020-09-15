import unittest
from unittest.mock import patch
from geektrust import Queries
from Familytree import variables


class Test_geektrust(unittest.TestCase):

    def setUp(self):
        self.queries = Queries()

    def test_calling_add_child_method(self):
        one_detail = self.queries.calling_add_child_method(
            "king")
        two_detail = self.queries.calling_add_child_method(
            "king", "male")
        three_detail = self.queries.calling_add_child_method(
            "mothers-name", "child-name", "gender")
        four_detail = self.queries.calling_add_child_method(
            "mothers-name", "child-name", "gender", 'x')
        self.assertEqual(one_detail, None)
        self.assertEqual(four_detail, None)
        self.assertEqual(
            two_detail,
            'self.family.add_parent("king", "male")'
        )
        self.assertEqual(
            three_detail,
            'self.family.add_child("child-name", "gender", "mothers-name")'
        )

    def test_calling_add_spouse_method(self):
        two_detail = self.queries.calling_add_spouse_method(
            "Baby", "Female")
        three_detail = self.queries.calling_add_spouse_method(
            "Hubby", "Baby", "Female")
        self.assertEqual(two_detail, None)
        self.assertEqual(three_detail, 'self.family.add_spouse("Baby", "Female", "Hubby")')

    def test_calling_get_relationship_method(self):
        one_detail = self.queries.calling_get_relationship_method(
            "Name")
        two_detail = self.queries.calling_get_relationship_method(
            "Hubby", "Brother-In-Law")
        invalid_detail = self.queries.calling_get_relationship_method(
            "rambo", "Random")

        self.assertEqual(one_detail, None)
        self.assertEqual(
            two_detail,
            'self.family.get_relationship("Hubby", "Brother-In-Law")'
        )
        self.assertEqual(invalid_detail, None)

    @patch(
        'geektrust.Family.get_relationship',
        return_value=variables.NONE
    )
    @patch(
        'geektrust.Family.add_spouse',
        return_value=variables.SPOUSE_ADDITION_SUCCEEDED
    )
    @patch(
        'geektrust.Family.add_child',
        return_value=variables.CHILD_ADDITION_SUCCEEDED
    )
    def test_decoding_input(self, mock_add_child, mock_add_spouse,
                            mock_get_relationship):
        with patch('builtins.open', create=True) as mock_open:  # noqa
            mock_open.return_value.__enter__.return_value.readlines.return_value = (  # noqa
                'ADD_CHILD Mother Member Male',
                'ADD_SPOUSE Spouse Wife Female',
                'GET_RELATIONSHIP Member Brother-In-Law'
            )
            output = self.queries.decoding_input('input_tmp.txt')
            self.assertEqual(
                output,
                [
                    variables.CHILD_ADDITION_SUCCEEDED,
                    variables.SPOUSE_ADDITION_SUCCEEDED,
                    variables.NONE
                ]
            )
            mock_add_child.assert_called_with("Member", "Male", "Mother")
            mock_add_spouse.assert_called_with("Wife", "Female", "Spouse")
            mock_get_relationship.assert_called_with("Member", "Brother-In-Law")

    @patch('builtins.print')
    def test_print_output(self, mock_print):
        self.queries.print_output(
            [
                variables.CHILD_ADDITION_SUCCEEDED,
                variables.SPOUSE_ADDITION_SUCCEEDED,
                variables.NONE
            ]
        )
        mock_print.assert_called_with(variables.NONE)

    @patch('geektrust.Queries.decoding_input', return_value=['RESULT'])
    def test_main(self, mock_decoding_input):
        self.assertEqual(self.queries.decoding_input('filename'), ['RESULT'])
        mock_decoding_input.assert_called_with('filename')


if __name__ == "__main__":
    unittest.main()
