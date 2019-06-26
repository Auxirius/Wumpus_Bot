#Import sqlite3 because database
import sqlite3

#Create the connection to the db with auto commit ON
conn = sqlite3.connect("database.db", isolation_level=None)
cur = conn.cursor()

#Create tables if they don't exist
def create_tables():
	query = """
	CREATE TABLE IF NOT EXISTS "prefixes" (
	"server"	TEXT UNIQUE,
	"prefix"	TEXT
	);
	"""

	cur.execute(query)

#Get the server prefixes
def get_prefixes():
	#sql statement
	cur.execute("SELECT * FROM prefixes")

	#Turn it into json
	prefixes = {}
	for row in cur.fetchall():
		prefixes[row[0]] = row[1]

	return prefixes

#Update the prefixes every 5 minutes
def set_prefixes(prefixes_json):
	#Turn the json into a list of tuples
	prefixes = []
	for key in prefixes_json.keys():
		prefixes.append( (key, prefixes_json[key]) )

	#Create the query
	query = """
	INSERT OR REPLACE INTO prefixes (server, prefix) VALUES (?,?)
	"""

	#Execute the query for all of the prefixes
	cur.executemany(query, prefixes)

#Get the user profile
def get_profile(id):
	query = """
	SELECT coins, pfp FROM users WHERE id=?
	"""

	#Run the query
	cur.execute(query, (id,))
	
	#Get the results and return them a json
	json = {}
	r = cur.fetchall()[0]
	
	#json stuff
	json["coins"] = r[0]
	json["pfp"] = r[1]

	return json