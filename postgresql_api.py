import psycopg2
import os
try:
    connection = psycopg2.connect(user = os.environ["PG_USER"],
                                  password = os.environ["PG_PASSWORD"],
                                  host = os.environ["PG_HOST"],
                                  port = os.environ["PG_PORT"],
                                  database = os.environ["PG_DATABASE"])
    cursor = connection.cursor()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

def get_data(query_string):
    if(connection):
            cursor.execute(query_string)
            data = cursor.fetchall()
            print(data)
            return(data)

"""
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""
