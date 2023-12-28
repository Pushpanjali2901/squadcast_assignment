import psycopg2
# PostgreSQL database credentials to connect with the database
db_credentials = {
    "host": "dpg-cm5ufsed3nmc73aoectg-a.oregon-postgres.render.com",
    "database": "movie_db_2pzx",
    "user": "movie_db_2pzx_user",
    "password": "d2o83deqtsSOuOmYggQcpI2rNi47KXgB",
    "port": "5432",
}

# Function to establish a connection to the PostgreSQL database
def connect_to_postgres():
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(**db_credentials)

        return connection
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None


