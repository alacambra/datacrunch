class Object:
    def __init__(self, row):

        self.project_id = row[1]
        self.id = row[0]
        self.description = row[3]
        self.subject = row[2]
