import mysql.connector

class DatabaseConnection:
    hostname = None
    database = None
    username = None
    password = None
    connection = None
    cursor = None
    query = None

    def __init__(self, hostname, database, username, password):
        if not self.connection:
            self.hostname = hostname
            self.database = database
            self.username = username
            self.password = password
            self.connect()

    def connect(self):
        ''' Connect the database
        '''
        try:
            self.connection = mysql.connector.connect(
                host     = self.hostname,
                user     = self.username,
                password = self.password,
                database = self.database)
            return self.connection
        except mysql.connector.Error as err:
            print("Error connecting to database:", err)    

    def disconnect(self):
        '''Diconnect the database
        '''
        try:
            if self.connection:
                self.cursor.close()
                self.connection.close()
        except mysql.connector.Error as err:
            print("Error disconnecting from database:", err)
            
    def query(self, query):
        ''' Query the database.
            Return the list consist of quary output.
        ''' 
        result = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)

            # Check if the query is INSERT, UPDATE, or DELETE
            if query.strip().lower().startswith(('insert', 'update', 'delete')):
                # Commit changes for INSERT, UPDATE, or DELETE queries
                self.connection.commit()
                result = self.cursor.rowcount  # number of affected rows
            else:
                for row in self.cursor:
                    result.append(row)
        except mysql.connector.Error as err:
            print("Error executing query:", err)
        finally:
            if self.cursor:
                self.cursor.close()
        return result

    def count(self, table, condition = None):
        return len(self.simple_query(table, '*', condition))

## Tests
# query1 = "INSERT INTO account (case_id, account_name) VALUES ('CS0426786','ParaTestAccount6')"
# db=DatabaseConnection(hostname='localhost',
#                               database='sentiment',
#                               username='',
#                               password=''
#                               )
# db.connect()
# result = db.query(query1)
# db.disconnect()
# print(result)
  