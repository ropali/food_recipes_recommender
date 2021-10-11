from .db import DB


class PlaceModel(DB):

    TABLE_NAME = 'places'

    def __init__(self):
        super().__init__()
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (url TEXT, desc TEXT, state VARCHAR(50), country VARCHAR(50), ratings VARCHAR(15), total_reviews VARCHAR(20), tagline VARCHAR(200) ,images TEXT)")

        self.con.commit()

    def save(self, data):
        self.insert(
            f"INSERT INTO {self.TABLE_NAME} VALUES (:url,:desc,:state,:country,:ratings,:total_reviews,:tagline,:images)", data)

    def all(self, **kwargs):
        return self.find_all(f"select * from {self.TABLE_NAME}")


class UrlVisited(DB):

    TABLE_NAME = 'visted'

    def __init__(self):
        super().__init__()
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (link TEXT)")

        self.con.commit()

    def save(self, data):
        self.insert(
            f"INSERT INTO {self.TABLE_NAME} VALUES (:link)", data)

    def all(self, **kwargs):
        return self.find_all(f"select * from {self.TABLE_NAME}")

    def find(self,link):
        self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE link=:link",{'link':link})
        return self.cursor.fetchone()
