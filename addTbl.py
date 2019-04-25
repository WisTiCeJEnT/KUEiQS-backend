import psycopg2

try:
    connection = psycopg2.connect(user = "nfldsmzmkmufoc",
                                  password = "a2b3353086041df6ebeeb998ebaad167cd75872717c6c774a2e51955c19811c2",
                                  host = "ec2-184-73-210-189.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "d7sef34h54mlib")
                                  
    cursor = connection.cursor()

    create_table = '''CREATE TABLE examTbl
        ( examID SERIAL PRIMARY KEY NOT NULL,
        courseID TEXT NOT NULL,
        room TEXT,
        date TEXT,
        time TEXT,
        startID BIGINT NOT NULL,
        endID BIGINT NOT NULL,
        sec INT NOT NULL,
        year INT NOT NULL,
        sem INT NOT NULL,
        mf TEXT NOT NULL
        );'''
    cursor.execute(create_table)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            