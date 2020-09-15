from unittest.mock import Mock


def mock_member_creation(id=None, name=None, gender=None,
                         mother=None, spouse=None, father=None,
                         children=None):
    person = Mock()
    person.id = id
    person.name = name
    person.gender = gender
    person.mother = mother
    person.spouse = spouse
    person.father = father
    person.children = children
    return person


