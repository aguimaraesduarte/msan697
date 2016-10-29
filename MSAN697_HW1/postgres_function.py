import psycopg2

def connectdb(db_name, user_name):
    try:
        db_conn = psycopg2.connect(dbname=db_name, user=user_name)
    except:
        print("Not able to connect to " + db_name)
    return db_conn

def db_cursor(db_conn):
    cursor = db_conn.cursor()  # open a cursor to perform db operations.
    return cursor

def execute(db_cursor, query):
    db_cursor.execute(query)

def create_table(db_cursor, table_name, column_and_type_list):
    create_table_query = "CREATE TABLE " + table_name + "(" + column_and_type_list + ");"
    execute(db_cursor, create_table_query)

def drop_table(db_cursor, table_name):
    drop_table_query = "DROP TABLE " + table_name + ";"
    execute(db_cursor, drop_table_query)

def insert_into_table(db_cursor, table_name, column_names, values):
    insert_into_table_query =  "INSERT INTO " + table_name + "(" + column_names + ") VALUES (" + values + ");"
    execute(db_cursor, insert_into_table_query)

def select_data(db_cursor, table_name, column_name, constraint):
    select_data_query =  "SELECT " + column_name + " FROM " + table_name + " WHERE " + constraint + ";"
    execute(db_cursor, select_data_query)

