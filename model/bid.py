from utils.connection import connection_pool

class Bid:
    def __init__(self, user_id, applyurl, companyname, position):
        self.user_id = user_id
        self.applyurl = applyurl
        self.companyname = companyname
        self.position = position

    def get_db_connection(self):
        return connection_pool.get_connection()

    def insert_new_bid(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        
        # Check if the applyurl already exists
        cursor.execute("SELECT * FROM tbl_bidlog WHERE apply_url = %s", (self.applyurl,))
        existing_bid = cursor.fetchone()
        
        if existing_bid is None:
            # If the applyurl does not exist, insert the new records
            
            cursor.execute("INSERT INTO tbl_bidlog (user_id, apply_url, company_name, position) VALUES (%s, %s, %s, %s)", (self.user_id, self.applyurl, self.companyname, self.position))
            connection_object.commit()
            connection_object.close()
            return True
            
        else:
            connection_object.close()
            return False
        

    def edit(self, email, applyurl, companyname, position):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("UPDATE tbl_bidlog SET email = %s, applyurl = %s, companyname = %s, position = %s WHERE apply_url = %s", (email, applyurl, companyname, position, self.applyurl))
        connection_object.commit()
        connection_object.close()

    def delete(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("DELETE FROM tbl_bidlog WHERE apply_url = %s", (self.applyurl,))
        connection_object.commit()
        connection_object.close()
        
    @staticmethod
    def editById(id, column, value, user_id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        
        if column == 'apply_url':
            cursor.execute("SELECT * FROM tbl_bidlog WHERE apply_url = %s", (value,))
            existing_email = cursor.fetchone()
            if existing_email:
                connection_object.close()
                return False  # Email already exists
        
        cursor.execute(f"UPDATE tbl_bidlog SET {column} = %s WHERE id = %s", (value, id))
        connection_object.commit()
        connection_object.close()
        return True
        
    @staticmethod
    def deleteById(id, user_id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        
        # Fetch the bid first
        cursor.execute("SELECT user_id FROM tbl_bidlog WHERE id = %s", (id,))
        bid = cursor.fetchone()
        # Check if the bid exists and the user_id matches
        if bid and bid[0] == user_id:
            # Proceed with the deletion
            cursor.execute("DELETE FROM tbl_bidlog WHERE id = %s", (id,))
            connection_object.commit()
            connection_object.close()
            return True
        
        elif bid and bid[0] != user_id:
            connection_object.close()
            return False
        
        else:
            connection_object.close()
            return None

    @staticmethod
    def getBids(date):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_bidlog WHERE DATE(created_at) = %s", (date,))
        bid_list = cursor.fetchall()
        connection_object.close()
        return bid_list
    
    @staticmethod
    def getBidById(id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_bidlog WHERE id = %s", (id,))
        bid = cursor.fetchone()
        connection_object.close()
        return bid