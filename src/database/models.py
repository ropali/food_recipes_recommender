from .db import DB


class RecipeModel(DB):

    TABLE_NAME = 'reciepes'

    def __init__(self):
        super().__init__()
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (url VARCHAR(250), recipe TEXT, title VARCHAR(200), summary TEXT, ingredients TEXT, nutritions TEXT, prep_cook_timings TEXT ,image_url TEXT)")

        self.con.commit()

    def save(self, data):
        self.insert(
            f"INSERT INTO {self.TABLE_NAME} VALUES (:url,:recipe,:title,:summary,:ingredients,:nutritions,:prep_cook_timings,:image_url)", data)

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
