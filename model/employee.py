from utils.connection import connection_pool

class Employee:
    
    def __init__(self, name, dob, email, phone, address, id_front,id_back, selfie, status):
        self.name = name
        self.dob = dob
        self.email = email
        self.phone = phone
        self.address = address
        self.id_front = id_front
        self.id_back = id_back
        self.selfie = selfie
        self.status = status
    
    def get_db_connection(self):
        return connection_pool.get_connection()
    
    def insert_new_employee(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM tbl_employee WHERE email = %s", (self.email,))
        existing_email = cursor.fetchone()
        if existing_email is None:
            cursor.execute("INSERT INTO tbl_employee (name, dob, email, phone, address, id_front_name, id_back_name, selfie_name, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.name, self.dob, self.email, self.phone, self.address, self.id_front, self.id_back, self.selfie, self.status))
            connection_object.commit()
            connection_object.close()
            return True 

        else:
            connection_object.close() # Email already exists
            return False
    def delete(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("DELETE FROM tbl_employee WHERE email = %s", (self.email,))
        connection_object.commit()
        connection_object.close()
    
    @staticmethod
    def editById(id, column, value):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        
        # Fetch the employee first
        if column == 'email':
            cursor.execute("SELECT * FROM tbl_employee WHERE email = %s", (value,))
            existing_email = cursor.fetchone()
            if existing_email:
                connection_object.close()
                return False  # Email already exists

        cursor.execute(f"UPDATE tbl_employee SET {column} = %s WHERE id = %s", (value, id))
        connection_object.commit()
        connection_object.close()
        return True
    
    @staticmethod
    def deleteById(id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        
        cursor.execute("DELETE FROM tbl_employee WHERE id = %s", (id,))
        connection_object.commit()
        connection_object.close()
        return True
    
    @staticmethod
    def getEmployees():
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_employee ")
        employee_list = cursor.fetchall()
        connection_object.close()
        return employee_list