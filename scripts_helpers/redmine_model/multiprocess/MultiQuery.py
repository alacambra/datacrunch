import multiprocessing

class MultiQuery(multiprocessing.Process):

    def __init__(self, query, db, pipe):
        self.query = query
        self.db = db
        self.pipe = pipe
        super(MultiQuery, self).__init__()

    def run(self):
        cur = self.db.cursor()
        q = cur.execute(self.query)
        self.pipe.send(cur.fetchall())
        self.pipe.close()