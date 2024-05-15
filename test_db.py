import psycopg2

# PostgreSQL database connection parameters
DB_HOST = 'localhost'
DB_PORT = '8888'
DB_NAME = 'net_kpi'
DB_USER = 'admin'
DB_PASSWORD = 'admin'

try:
    # Establish connection to PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Successfully connected to PostgreSQL database!")

    # Close connection
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL database:", e)
