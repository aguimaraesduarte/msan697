def database(client, dbname):
    return client[dbname]

def import_query(dbname, collection_name, input_file_name):
    mongoimport_query = "mongoimport --db %s --collection %s --file %s" % (dbname, collection_name, input_file_name)
    return mongoimport_query

def drop_table_query(db, collection_name):
    db[collection_name].drop()
