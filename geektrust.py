import sys
from Familytree.family_creation import Family


class Queries:
    def __init__(self):
        self.family = Family()

    # Method calling the add child method from family creation package
    # for the addition of a member to the family through
    # mother.
    def calling_add_child_method(self, *details):
        if len(details) < 2 or len(details) > 3:
            return None
        if len(details) == 2:
            return 'self.family.add_parent("{}", "{}")'.format(
                details[0],
                details[1]
            )
        return 'self.family.add_child("{}", "{}", "{}")'.format(
            details[1],
            details[2],
            details[0]
        )

    # Method calling the add spouse method for the addition of spouse for a member in the family.
    def calling_add_spouse_method(self, *details):
        if len(details) != 3:
            return None
        return 'self.family.add_spouse("{}", "{}", "{}")'.format(
            details[1],
            details[2],
            details[0]
        )

    # Method for calling the method to extract the relatives of particular relation of a member which was requested.
    def calling_get_relationship_method(self, *details):
        if len(details) != 2:
            return None
        relationships = ['Mother',
                         'Father',
                         'Spouse',
                         'Son',
                         'Daughter',
                         'Siblings',
                         'Maternal-Uncle',
                         'Maternal-Aunt',
                         'Paternal-Uncle',
                         'Paternal-Aunt',
                         'Brother-In-Law',
                         'Sister-In-Law'
                         ]

        if details[1] in relationships:
            relationship = details[1]
        else:
            return None

        return 'self.family.get_relationship("{}", "{}")'.format(
            details[0],
            relationship
        )

    # Method for processing the file and segregating the different kinds of queries and passing the arguments accordingly.
    def decoding_input(self, filename):
        switch_method_Calling = {
            'ADD_CHILD': self.calling_add_child_method,
            'GET_RELATIONSHIP': self.calling_get_relationship_method,
            'ADD_SPOUSE': self.calling_add_spouse_method
        }

        with open(filename, 'r') as fr:
            instructions = fr.readlines()

        outputs = []
        for instruction in instructions:
            tokens = instruction.strip().split(" ")
            construct_method = switch_method_Calling.get(tokens[0], None)
            if construct_method is None:
                continue
            output_method = construct_method(*tuple(tokens[1:]))
            if output_method is None:
                continue
            outputs.append(eval(output_method))
        return outputs

    # Method for printing the output to stdout
    def print_output(self, outputs):
        for output in outputs:
            print(output)

    # Method calling other methods which read and passe the queries for the respective methods for further executions
    def main(self):
        input_file = sys.argv[1]  # Taking the input file from cli for the execution
        commands = self.decoding_input(input_file)
        self.print_output(commands)


if __name__ == "__main__":
    query = Queries()
    fixed_family = './setup.instructions.txt'   # Datafile for loading the family tree
    query.decoding_input(fixed_family)          # pre-Loads the data of the family
    query.main()                                # Takes a file as input and Executes the queries given in file
