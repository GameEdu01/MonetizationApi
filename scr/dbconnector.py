import psycopg


class DBConnector:

    def __init__(self, dbname, user, password, address):

        self.dbname = dbname
        self.user = user
        self.password = password
        self.address = address

        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):

        conn = None

        try:
            conn = psycopg.connect(dbname=self.dbname,
                                   user=self.user,
                                   password=self.password,
                                   host=self.address[0],
                                   port=self.address[1])
        except Exception as err:
            print(err)

        return conn

    def check_if_value_exists(self, key, value):

        self.cursor.execute("SELECT * FROM m_users")
        records = self.cursor.fetchall()
        columnNames = [column[0] for column in self.cursor.description]
        table = {}

        for i in range(len(columnNames)):
            table[columnNames[i]] = records[i]

        print(table)

        if table.get(key) == value:
            return True

        return False

    def signup_user(self, user):

        query = f"""INSERT INTO m_users(name, surname, email, phone_number, token, session)
                        VALUES({user.name}, {user.surname}, {user.email}, {user.phone_number}, test_token, test_session"""

        self.cursor.execute(query)
        self.conn.commit()
