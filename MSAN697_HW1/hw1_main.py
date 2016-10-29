import json #json lilbrary

import json_key_value
import postgres_function
from  user_definition import *

#open a file ("input_file_name") as an input.
input_file_name = 'walmart_search_san_francisco.json'
with open(input_file_name, 'r') as input_file:
    data = json.load(input_file)
    #Q1
    print(json_key_value.get_data_value(data, "totalResults"))
    #Q2
    print(json_key_value.count_data(data, "items"))

#open database
#given as a parameter
db_conn = postgres_function.connectdb(dbname, usr_name)
cursor = postgres_function.db_cursor(db_conn)

#Q3
# Create DB tables, inventory and items
table_name = "inventory"
column_and_type_list = "itemId INTEGER, qty INTEGER"
postgres_function.create_table(cursor, table_name, column_and_type_list)

column_list = "itemId, qty"
for i in range(json_key_value.count_data(data, "items")):
	values = []
	try:
		itemId = str(data['items'][i]['itemId'])
	except:
		itemId = "NULL"
	if itemId == "NULL":
		qty = "NULL"
	else:
		qty = itemId[-2:]
	
	values.append(itemId)
	values.append(qty)
	
	postgres_function.insert_into_table(cursor, "inventory", column_list, ", ".join(values))

print "inventory ok"

table_name = "items"
column_and_type_list = "itemId INTEGER, name VARCHAR, shortDescription TEXT, customerRating REAL, numReviews INTEGER"
postgres_function.create_table(cursor, table_name, column_and_type_list)

column_list = "itemId, name, shortDescription, customerRating, numReviews"
for i in range(json_key_value.count_data(data, "items")):
	values = []
	try:
		values.append(str(data['items'][i]['itemId']))
	except:
		values.append("NULL")
	try:
		values.append("'" + data['items'][i]['name'].replace("'", "''") + "'")
	except:
		values.append("NULL")
	try:
		values.append("'" + data['items'][i]['shortDescription'].replace("'", "''") + "'")
	except:
		values.append("NULL")
	try:
		values.append(str(data['items'][i]['customerRating']))
	except:
		values.append("NULL")
	try:
		values.append(str(data['items'][i]['numReviews']))
	except:
		values.append("NULL")
	postgres_function.insert_into_table(cursor, "items", column_list, ", ".join(values))

# Q4
# Select Data
table_name = "inventory"
column_names = "*"
constraint = "itemId = (SELECT itemId FROM items WHERE name like 'MLB Women''s San Francisco Giants Short Sleeve Top')"
postgres_function.select_data(cursor, table_name, column_names, constraint)
print cursor.fetchone()

db_conn.commit() #make the changes to the db persistent.

#close communication with database.
cursor.close()
db_conn.close()
