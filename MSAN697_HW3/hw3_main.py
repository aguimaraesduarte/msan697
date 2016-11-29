import json #json lilbrary
import time

import json_key_value
import cassandra_function
from  user_definition import *

#open a file ("input_file_name") as an input.
with open(input_file_name, 'r') as input_file:
    data = json.load(input_file)

#Connect to Cassandra
#https://datastax.github.io/python-driver/getting_started.html
#Instantiate a cluster
cluster = cassandra_function.Cluster()
session = cassandra_function.connect_session(cluster)

#Drop a keyspace
cassandra_function.drop_keyspace(session, keyspace)

# Q1
# Create a keyspace
cassandra_function.create_keyspace(session, keyspace)

# Choose a keyspace
session.set_keyspace(keyspace)

# Q2
# Create DB tables
table_name = "items"
column_and_type_list = "itemId INT, name VARCHAR, shortDescription TEXT, customerRating DOUBLE, numReviews INT, qty INT"
primary_key_list =  "itemId"
cassandra_function.create_table(session, table_name,column_and_type_list, primary_key_list)

# Insert Data
# FINISH THIS.
# TODO : WRITE CODE TO INSERT DATA FROM "data" in line 10. USE insert_into_table() FUNCTION IN cassandra_function.py
for item in data['items']:
	itemId = item['itemId']
	column_names = "itemId, "
	values = '%s, ' %itemId
	try:
		name = item['name']
		column_names += "name, "
		values += "'%s', " %name.replace("'", "''")
	except:
		pass
	try:
		shortDescription = item['shortDescription']
		column_names += "shortDescription, "
		values += "'%s', " %shortDescription.replace("'", "''")
	except:
		pass
	try:
		customerRating = item['customerRating']
		column_names += "customerRating, "
		values += '%s, ' %customerRating
	except:
		pass
	try:
		numReviews = item['numReviews']
		column_names += "numReviews, "
		values += '%s, ' %numReviews
	except:
		pass
	qty = itemId % 100
	column_names += "qty"
	values += '%s' %qty
	#print column_names, values
	cassandra_function.insert_into_table(session, table_name, column_names, values)
# Ex. cassandra_function.insert_into_table(session, "items", "itemId, name, ....", "VALUE, VALUE, .....")

# Q3
"""
column_names = "*"
table_name = "items"
constraint = "itemId = 47027011"
#constraint = "qty = 11 ALLOW FILTERING"
#constraint = "name = 'MLB Women''s San Francisco Giants Short Sleeve Top'"
for row in cassandra_function.select_data(session,  table_name, column_names, constraint):
	print row
"""

#Q4
"""
column_names = "*"
table_name = "items"
constraint = "name = 'MLB Women''s San Francisco Giants Short Sleeve Top'"
#constraint = "name = 'MLB Women''s San Francisco Giants Short Sleeve Top' ALLOW FILTERING"
for row in cassandra_function.select_data(session,  table_name, column_names, constraint):
	print row
"""
question =  "Does select 'MLB Women''s San Francisco Giants Short Sleeve Top' work in the items table table work without ALLOW FILTERING?"
answer = "No" #Choose one
print ("%s - %s") %(question, answer)

# Q5
# Create Materized View
view_name = "materialized_items_view"
column_names = "*"
table_name = "items"
constraint = "name IS NOT NULL"
primary_keys = "name, itemId"
cassandra_function.create_materialized_view(session, view_name, column_names, table_name, constraint, primary_keys)

# Wait until materialized view is created.
select_table_query = "SELECT COUNT(*) AS ct FROM items"
base_table_row_count = session.execute(select_table_query)[0].ct
ct = 0
while ct != base_table_row_count:
    time.sleep(1)
    select_materialized_view_query = "SELECT COUNT(*) AS ct FROM materialized_items_view"
    rows = session.execute(select_materialized_view_query)
    ct= rows[0].ct
    
# Q6
# Select data from view
column_names = "*"
table_name =  "materialized_items_view"
constraint = "name = 'MLB Women''s San Francisco Giants Short Sleeve Top'"
returned_rows = cassandra_function.select_data(session,  table_name, column_names, constraint)
for row in returned_rows:
	print row

# Q7
"""
table_name = "materialized_items_view"
column = "numReviews"
value = "10"
constraint = "name = 'NFL Men''s San Francisco 49Ers C Hyde 28 Player Tee' and itemId = 52507967"
cassandra_function.update_data(session,  table_name, column, value, constraint)
"""

question = "Can you update data in materialized views?"
answer = "no"
print ("%s - %s") %(question, answer)

# Q8
"""
table_name = "items"
column = "numReviews"
value = "10"
constraint = "itemId = 52507967"
cassandra_function.update_data(session,  table_name, column, value, constraint)

table_name = "items"
column_names = "*"
constraint = "itemId = 52507967"
returned_rows = cassandra_function.select_data(session,  table_name, column_names, constraint)
for row in returned_rows:
	print row

table_name = "materialized_items_view"
column_names = "*"
constraint = "name = 'NFL Men''s San Francisco 49Ers C Hyde 28 Player Tee'"
returned_rows = cassandra_function.select_data(session,  table_name, column_names, constraint)
for row in returned_rows:
	print row
"""

question = "When you update data in a base(original) table, is the content also updated in the corresponding materialized view?"
answer = "yes"
print ("%s - %s") %(question, answer)

# Close communication.
cluster.shutdown()
