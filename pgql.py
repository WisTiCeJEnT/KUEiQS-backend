import psycopg2
try:
    connection = psycopg2.connect(user = "nfldsmzmkmufoc",
                                  password = "a2b3353086041df6ebeeb998ebaad167cd75872717c6c774a2e51955c19811c2",
                                  host = "ec2-184-73-210-189.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "d7sef34h54mlib")
    cursor = connection.cursor()

    create_table_query = '''SELECT stdid FROM stddata'''

    cursor.execute(create_table_query)
    print(cursor.fetchall())
    connection.commit()
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
