import sqlite3


class Database:
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect(name + ".db")
        self.c = self.conn.cursor()

        print("Checking for already existing database...")
        try:
            sql = "CREATE TABLE %s (time VARCHAR, velocity REAL, lat REAL, long REAL, identifier INTEGER)" % self.name
            self.c.execute(sql)
        except sqlite3.OperationalError:
            print("Database already exists")

    def enter_data(self, data_=None):
        if data_ is None:
            return
        sql = "INSERT INTO %s (time, velocity, lat, long, identifier) VALUES (?,?,?,?,?)" % self.name

        self.c.execute(sql, (data_.time, data_.velocity, data_.long, data_.lat, data_.identifier))
        self.conn.commit()

    def read_from_database(self, index=None):
        if index is None:
            sql = "SELECT * FROM %s WHERE identifier > -1" % self.name
        else:
            sql = "SELECT * FROM %s WHERE identifier == %d" % (self.name, index)
        return self.c.execute(sql)

    def clear_all(self):
        sql = "DELETE FROM %s WHERE identifier > -1" % self.name
        self.c.execute(sql)
        self.conn.commit()

    def clear_id(self, index=None):
        if index is None:
            return
        sql = "DELETE FROM %s WHERE identifier == ?" % self.name
        self.c.execute(sql, [(index)])
        self.conn.commit()

    def largest_identifier(self):
        sql = "SELECT MAX(identifier) FROM %s WHERE identifier > -1" % self.name
        for row in self.c.execute(sql):
            if row[0] is None:
                return -1
            else:
                return row[0]

