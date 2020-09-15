from Familytree import variables


class Person:
    # A person class with the details corresponding to his family initialized with only his name, gender
    # can be added only through mother apart from the initialization of family tree.
    def __init__(self, num, name, gender):
        self.id = num
        self.name = name
        self.gender = gender
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    # assigning mother details
    def assign_mother(self, mother):
        if not isinstance(mother, Person):
            raise ValueError('Invalid value for mother')
        if mother.gender not in variables.Gender[variables.female]:
            raise ValueError(
                'Invalid gender value for mother.'
                'Mother should be a Female'
            )
        self.mother = mother

    # assigning father details.
    def assign_father(self, father):
        if not isinstance(father, Person):
            raise ValueError('Invalid value for father')
        if father.gender not in variables.Gender[variables.male]:
            raise ValueError(
                'Invalid gender value for father.'
                'Father should be a Male'
            )
        self.father = father

    # assigning spouse incase if there is any.
    def assign_spouse(self, spouse):
        if not isinstance(spouse, Person):
            raise ValueError('Invalid value for spouse')
        if self.gender == spouse.gender:
            raise ValueError(
                'Invalid gender value for spouse.'
                'Spouse and member cannot have the same gender.'
            )
        self.spouse = spouse

    # adding children for parents when ever a new child is added.
    def add_children(self, child):
        if not isinstance(child, Person):
            raise ValueError('Invalid value for child')
        self.children.append(child)

    # methods for getting relations
    def get_mother(self):
        if self.mother is None:
            return None
        return [self.mother]

    def get_father(self):
        if self.father is None:
            return None
        return [self.father]

    def get_spouse(self):
        if self.spouse is None:
            return None
        return [self.spouse]

    # get mother of father for the requested self, used for getting the relations attached to her
    def get_paternal_grandmother(self):
        if self.father is None:
            return None
        if self.father.mother is None:
            return None
        return self.father.mother

    # get mother of mother for the requested self, used for getting the relations attached to her
    def get_maternal_grandmother(self):
        if self.mother is None:
            return None
        if self.mother.mother is None:
            return None
        return self.mother.mother

    # get mother of spouse for the requested self, used for getting the relations attached to her
    def get_spouse_mother(self):
        if self.spouse is None:
            return None
        if self.spouse.mother is None:
            return None
        return self.spouse.mother

    # using fathers mother getting the female siblings
    def get_paternal_aunt(self):
        grandmother = self.get_paternal_grandmother()
        if grandmother is None:
            return []
        if not grandmother.children:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.female],
                grandmother.children
            )
        )

    # Using fathers mother getting  the male siblings
    def get_paternal_uncle(self):
        grandmother = self.get_paternal_grandmother()
        if grandmother is None:
            return []
        if not grandmother.children:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.male] and x.name != self.father.name,
                grandmother.children
            )
        )

    # Getting mothers sisters using her mother
    def get_maternal_aunt(self):
        grandmother = self.get_maternal_grandmother()
        if grandmother is None:
            return []
        if not grandmother.children:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.female] and x.name != self.mother.name,
                grandmother.children
            )
        )

    # Getting mothers brothers using her mother
    def get_maternal_uncle(self):
        grandmother = self.get_maternal_grandmother()
        if grandmother is None:
            return []
        if not grandmother.children:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.male],
                grandmother.children
            )
        )

    # Getting spouses of siblings using siblings
    def get_sibling_spouses(self):
        siblings = self.get_siblings()
        if not siblings:
            return []
        sibling_spouses = [
            sibling.spouse for sibling in siblings if sibling.spouse
        ]
        return sibling_spouses

    def get_spouse_siblings(self):
        if self.spouse is None:
            return []
        return self.spouse.get_siblings()

    def get_brother_in_law(self):
        results = self.get_sibling_spouses() + self.get_spouse_siblings()
        if not results:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.male],
                results
            )
        )

    def get_sister_in_law(self):
        results = self.get_sibling_spouses() + self.get_spouse_siblings()
        if not results:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.female],
                results
            )
        )

    def get_son(self):
        if not self.children:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.male],
                self.children
            )
        )

    def get_daughter(self):
        if not self.children:
            return []
        return list(
            filter(
                lambda x: x.gender in variables.Gender[variables.female],
                self.children
            )
        )

    def get_siblings(self):
        if self.mother is None:
            return []
        if not self.mother.children:
            return []
        return list(
            filter(
                lambda x: x.name != self.name,
                self.mother.children
            )
        )

    def get_relatives(self, relation):
        switch = {
            'Mother': self.get_mother(),
            'Father': self.get_father(),
            'Spouse': self.get_spouse(),
            'Son': self.get_son(),
            'Daughter': self.get_daughter(),
            'Siblings': self.get_siblings(),
            'Paternal-Uncle': self.get_paternal_uncle(),
            'Paternal-Aunt': self.get_paternal_aunt(),
            'Maternal-Uncle': self.get_maternal_uncle(),
            'Maternal-Aunt': self.get_maternal_aunt(),
            'Brother-In-Law': self.get_brother_in_law(),
            'Sister-In-Law': self.get_sister_in_law()
        }

        output = switch.get(
            relation, None)
        if output == [] or output is None:
            return None
        return output
