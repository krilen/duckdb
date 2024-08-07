# https://youtu.be/HJGiMTLcpDs?si=zph2bM1siZ009YWP
#
# Need to import the module to use duckdb
# Module needs to be installed
import duckdb

# Simple way of using duckdb (in-memory mode)
"""
cursor = duckdb.connect()
print(cursor.execute("SELECT 42").fetchall()) # => [(42,)]
"""

# With duckdb you must FIRST create a connection to the database
# 1. Pesistant connection - save to disk
#    Needs a path to the database ...
#
# 2. In-Memory Database - only stored in memory
#    ...

# Import data from CSV file - https://duckdb.org/docs/data/csv/overview

# Pass the file into duckdb and we get back a relation in duck DB (type: DuckDBPyRelation)
#print(duckdb.sql("SELECT * FROM 'employees.csv'"))

# More specific to CSV
#print(duckdb.read_csv('employees.csv'))
#
# Key word arguments (paraments) can be added to cusomize how it is read
# Filename - adds a column with the filename that the data comes from
#print(duckdb.read_csv('employees.csv', filename=True))
#
# Header - If the header of the colums are present in the CSV file
#print(duckdb.read_csv('employees.csv', header=False)) # -> First row contians the header from the CSV file
#
# Skip rows
#print(duckdb.read_csv('employees.csv', header=False, skiprows=1 )) # Skip the first row that contained the headers from the CSV file



# DIFFERENT FORMATS ########################

# The "DuckDBPyRelation" can be converted into different formats
#print(type(duckdb.sql("SELECT * FROM 'employees.csv'"))) # -> "<class 'duckdb.duckdb.DuckDBPyRelation'>"
#result = duckdb.sql("SELECT * FROM 'employees.csv'")

# The default is of type relation
#print(result) # default output like above

# Pandas dataframe, pyDB -> Panda dataframe (modules needs to be installed numpy and pandas)
#print(result.df())

# Polars dataframe, pyDB - Polars dataframe (needs modules pyarrow and polars)
#print(result.pl())

# Py Arrow table 
#print(result.arrow())

# Numpy array
#print(result.fetchnumpy())

# Basic python objects - a list containing tuples, one tuple for each row
#print(result.fetchall())



# ANALYTICAL QUERIES #########################
# This is the main reason to use DuckDB

# Create a table "employees"
duckdb.sql("CREATE TABLE employees AS (SELECT * FROM 'employees.csv')")

# Query the created table and you can now start analysing the data
#result = duckdb.sql("SELECT * FROM employees ORDER BY Salary ASC LIMIT 10") # The 10 lowest payed employees
#print(result)

# Get the employye with the highest bonus
"""
result = duckdb.sql('''
SELECT * FROM employees
WHERE "Bonus %" = (SELECT MAX("Bonus %")
FROM employees)
''')
print(result)
"""

# Get the output to be able to use it
# 'fetchall()' -> list containing tuples with elements
"""
result = duckdb.sql("SELECT AVG(Salary) FROM employees").fetchall() 
print(result) # => '[(90662.181,)]': In this case only one element in the tuple within the list
"""

# 'fetone()' -> single tuple
"""
result = duckdb.sql("SELECT AVG(Salary) FROM employees").fetchone()
print(result) # => '(90662.181,)'
print(result[0]) # => '90662.181': The [0] can also be placed in the query '...ployees").fetchone()[0]'
"""

# Group by Team and it average salary
"""
result = duckdb.sql("SELECT Team, AVG(Salary) FROM employees GROUP BY Team")
print(result)
"""



# CAST TYPE ###################################3

# Use the postgres way
# Convert 'Salary' of type "int64" to type "float"
"""
result = duckdb.sql("SELECT Salary::float AS Salary FROM employees LIMIT 10") 
print(result)
"""

# Cast function in SQL (postgres)
# Convert 'Bonus %' of type "double" (float) to type "int"
# OBS!!! must use " in the CAST function
"""
result = duckdb.sql('SELECT CAST("Bonus %" AS int) AS Bonus FROM employees LIMIT 10') 
print(result)
"""


# ADMIN ###########################

# Show the created tables
print(duckdb.sql("SHOW TABLES"))

# Delete the existing tables 
print(duckdb.sql("DROP TABLE employees"))

# Show the exising tables now
print(duckdb.sql("SHOW TABLES"))
