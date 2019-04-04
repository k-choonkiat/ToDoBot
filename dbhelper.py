import sqlite3


class DBHelper:
    # creation of database and giving it a name
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        # conn is a connection object that represents the db
        self.conn = sqlite3.connect(dbname)

    def setup(self):# creates a new table and has one column ; description
        stmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemindex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(stmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text,owner):
        # '?' acts as the placeholder 
        stmt = "INSERT INTO items (description,owner) VALUES (?,?)"
        args = (item_text,owner )
        # here when we execute, args will fill up the placeholder (?,?)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner =(?)"
        args = (item_text,owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self,owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args =(owner,)
        return [x[0] for x in self.conn.execute(stmt,args)]
