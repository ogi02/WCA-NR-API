import os
import sqlite3
from sqlite3 import Cursor

from wca_nr_api.config.constants import *
from wca_nr_api.config.logger import logger

def execute_sql_script() -> None:
	"""
	Executes the SQL script from the WCA export into the local database.
	"""

	# Get path to SQL script
	sql_file_location = os.path.join(EXPORTS_FOLDER, FILTERED_EXPORTS_SQL_FILENAME)
	logger.info(f"Executing SQL script {sql_file_location}")

	# Open SQL script in reading mode
	with open(sql_file_location, "r", encoding="utf8") as sql_file:
		sql_script = sql_file.read()

	# Open DB file and execute SQL script
	with DB() as database:
		database.executescript(sql_script)


class DB:
	def __enter__(self) -> Cursor:
		"""
		Creates a connection to the database.

		:return: (Cursor) The SQLite3 cursor
		"""

		# Get path to database
		database_file_location = os.path.join(DATABASE_FOLDER, DATABASE_FILENAME)
		# Create connection
		self.conn = sqlite3.connect(database_file_location)
		# Return cursor
		return self.conn.cursor()

	def __exit__(self, type, value, traceback) -> None:
		"""
		Commits the changes made to the database and closes the connection.
		"""

		# Commit changes
		self.conn.commit()
		# Close connection
		self.conn.close()
