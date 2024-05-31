from utils.connection import connection_pool

class Usercity:
    def __init__(self, user_id, city, country, timezone):
        self.user_id = user_id
        self.city = city
        self.country = country
        self.timezone = timezone
        
    def get_db_connection(self):
        return connection_pool.get_connection()
    
    def insert_new_city(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        
        cursor.execute("INSERT INTO tbl_user_city (user_id, city, country, timezone) VALUES (%s, %s, %s, %s)", (self.user_id, self.city, self.country, self.timezone))
        connection_object.commit()
        connection_object.close()
        return True
    
    def delete(self):
        connection_object = self.get_db_connection()
        cursor = connection_object.cursor()
        cursor.execute("DELETE FROM tbl_user_city WHERE city = %s", (self.city,))
        connection_object.commit()
        connection_object.close()
        return True
        
    @staticmethod
    def getUserCityByUserId(user_id):
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT * FROM tbl_user_city WHERE user_id = %s", (user_id,))
        user_timezone_list = cursor.fetchall()
        connection_object.close()
        return user_timezone_list