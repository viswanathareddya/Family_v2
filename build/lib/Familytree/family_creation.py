from Familytree.individual import Person
from Familytree import variables


class Family:

    def __init__(self):
        self.family = {}

    def add_parent(self, name, gender):
        _id = len(self.family.keys()) + 1
        parent = Person(_id, name, gender)
        if _id == 1:
            self.family[name] = parent
            return variables.PARENT_ADDITION_SUCCEEDED

        return variables.PERSON_NOT_FOUND

    # Method for adding a child(member) after checking for various cases of constraints to add a member
    def add_child(self, name, gender, mother):
        _id = len(self.family.keys()) + 1
        new_member = Person(_id, name, gender)

        if name in self.family:
            return variables.CHILD_ADDITION_FAILED

        mothers_data = self.family.get(mother, None)
        if mothers_data is None:
            return variables.PERSON_NOT_FOUND

        if mothers_data.gender not in variables.Gender[variables.female]:  # ("Female", "female"):
            return variables.CHILD_ADDITION_FAILED

        fathers_data = mothers_data.spouse
        if fathers_data is None:
            return variables.CHILD_ADDITION_FAILED
        try:
            new_member.assign_mother(mothers_data)
            new_member.assign_father(fathers_data)
            self.family[mother].add_children(new_member)
            self.family[fathers_data.name].add_children(new_member)
            self.family[name] = new_member
            return variables.CHILD_ADDITION_SUCCEEDED
        except ValueError:
            return variables.CHILD_ADDITION_FAILED

    # method for adding a member and assigning them as a spouse for a member in the family
    def add_spouse(self, name, gender, spouse_name):
        _id = len(self.family.keys()) + 1
        new_member = Person(_id, name, gender)
        if self.family is None:
            return variables.SPOUSE_ADDITION_FAILED

        if name in self.family:
            return variables.SPOUSE_ADDITION_FAILED

        spouse = self.family.get(spouse_name, None)
        if spouse is None:
            return variables.PERSON_NOT_FOUND

        if spouse.gender == new_member.gender:
            return variables.SPOUSE_ADDITION_FAILED

        if spouse.spouse is not None:
            return variables.SPOUSE_ADDITION_FAILED

        try:

            new_member.assign_spouse(self.family[spouse.name])
            self.family[name] = new_member
            self.family[spouse.name].assign_spouse(self.family[name])

            return variables.SPOUSE_ADDITION_SUCCEEDED
        except ValueError:
            return variables.SPOUSE_ADDITION_FAILED

    # Method for getting the relatives with a relationship type mentioned for a given member of the family
    def get_relationship(self, name, relation):
        if name not in self.family.keys():
            return variables.PERSON_NOT_FOUND
        person = self.family[name]
        output = person.get_relatives(relation)
        if output is None:
            return variables.NONE
        final_output = ' '.join(
                list(
                    map(
                        lambda x: x.name,
                        sorted(output, key=lambda key: key.id)
                    )
                )
            )
        return final_output
