from utils.connection import connection_pool

class Candidate:
    def __init__(self, candidate_name, candidate_email, candidate_phone, candidate_position, candidate_photo_name):
        self.name = candidate_name
        self.email = candidate_email
        self.phone = candidate_phone
        self.position = candidate_position
        self.photo_name = candidate_photo_name
    
    def get_db_connection(self):
        return connection_pool.get_connection()
    
    def insert_new_candidate(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        
        # Check if the applyurl already exists
        cursor.execute("SELECT * FROM tbl_support_candidate WHERE email = %s", (self.email,))
        existing_candidate = cursor.fetchone()
        
        if existing_candidate is None:
            # If the applyurl does not exist, insert the new records
            
            cursor.execute("INSERT INTO tbl_support_candidate (name, email, phone, position, photo_name) VALUES (%s, %s, %s, %s, %s)", (self.name, self.email, self.phone, self.position,self.photo_name))
            connection_object.commit()
            connection_object.close()
            return True
            
        else:
            connection_object.close()
            return False
    
    def delete(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("DELETE FROM tbl_support_candidate WHERE email = %s", (self.email,))
        connection_object.commit()
        connection_object.close()
    
    @staticmethod
    def editById(id, column, value):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        if column == 'email':
            cursor.execute("SELECT * FROM tbl_support_candidate WHERE email = %s", (value,))
            existing_email = cursor.fetchone()
            
            if existing_email:
                connection_object.close()
                return False  # Email already exists

        cursor.execute(f"UPDATE tbl_support_candidate SET {column} = %s WHERE id = %s", (value, id))
        connection_object.commit()
        connection_object.close()
        return True

    @staticmethod
    def deleteById(id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        
        cursor.execute("DELETE FROM tbl_support_candidate WHERE id = %s", (id,))
        connection_object.commit()
        connection_object.close()
        return True
        
    @staticmethod
    def getCandidates():
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_support_candidate ")
        candidate_list = cursor.fetchall()
        connection_object.close()
        return candidate_list
    
    @staticmethod
    def getCandidateById(id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_support_candidate WHERE id = %s", (id,))
        candidate = cursor.fetchone()
        connection_object.close()
        return Candidate(candidate[1], candidate[2], candidate[3], candidate[4], candidate[5])