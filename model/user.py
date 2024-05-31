
import bcrypt
from utils.connection import connection_pool

class User:
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def get_db_connection(self):
        return connection_pool.get_connection()
    
    def sign_up(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()

        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (self.email,))
        user = cursor.fetchone()

        if user:
            connection_object.close()
            return False

        hashed_password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')
        cursor.execute("INSERT INTO tbl_user (email, password) VALUES (%s, %s)", (self.email, hashed_password))
        connection_object.commit()
        connection_object.close()
        
        return True
    
    def sign_in(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (self.email,))
        user = cursor.fetchone()
        connection_object.close()
        
        if user:
            # Encode the hashed password to a byte string before comparing
            if bcrypt.checkpw(self.password.encode(), user[2].encode('utf-8')):
                return user[0]
            
            else:
                return False
        return None
    
    @staticmethod
    def get_user_by_email(email):
        connection_object = connection_pool.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        connection_object.close()

        if user_data is not None:
            # Assuming User class has an initializer that accepts the data as parameters
            # Replace 'id', 'name', 'email', 'password' with actual column names
            user = User(id=user_data[0], name=user_data[1], email=user_data[2], password=user_data[3])
            return user
        else:
            return None
    
    @staticmethod
    def get_users():
        connection_object = connection_pool.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_user")
        users = cursor.fetchall()
        connection_object.close()
        return users