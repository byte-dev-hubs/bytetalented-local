from mysql.connector import pooling
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pool",
    pool_size=20,
    pool_reset_session=True,
    host="localhost",
    user="root",
    password="",
    database="bytetalented"
)