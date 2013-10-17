class Project:

    def __init__(self, row):

        self.id = row[0]
        self.name = row[1]
        self.description = row[2]
        self.parent_id = row[3]

    def __repr__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.description) + " " + str(self.parent_id)

    def __str__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.description) + " " + str(self.parent_id)