# Python dependencies
import os.path
from typing import Any

# Project dependencies
from wca_nr_api.config.constants import *
from wca_nr_api.config.logger import logger


def filter_sql_dump(table_filters: dict[str, Any]) -> None:
    """
    Extracts:
      - The CREATE TABLE statements for the given tables.
      - All INSERT statements for the given tables.
      - Applies different filters per table.

    :param table_filters: (dict) Dictionary of {table_name: filter_value}.
    """

    in_create_table, in_insert, insert_statement = None, None, None
    insert_values = []

    sql_dump_filename = os.path.join(EXPORTS_FOLDER, EXPORTS_SQL_FILENAME)
    filtered_sql_dump_filename = os.path.join(EXPORTS_FOLDER, FILTERED_EXPORTS_SQL_FILENAME)

    # Flags for all the tables in the filter
    sql_tables_flags = create_flags_dict(table_filters)

    logger.info(f"Starting filtering SQL dump. Input - {sql_dump_filename}, output - {filtered_sql_dump_filename}")

    with open(sql_dump_filename, "r", encoding="utf-8", errors="ignore") as infile, \
            open(filtered_sql_dump_filename, "w", encoding="utf-8") as outfile:

        # DROP tables if they exist
        for table in table_filters:
            outfile.write(f"DROP TABLE IF EXISTS `{table}`;")

        for line in infile:
            stripped_line = line.strip()

            # Detect and extract CREATE TABLE statements
            for table in table_filters:
                if stripped_line.startswith(f"CREATE TABLE `{table}`"):
                    # Start capturing the CREATE statement
                    in_create_table = table
                    outfile.write(stripped_line)
                    break
                if in_create_table == table:
                    if stripped_line.startswith(")"):
                        outfile.write(");\n")
                        # Stop capturing the CREATE statement
                        sql_tables_flags[in_create_table]["create_processed"] = True
                        logger.info(f"Processed CREATE statement for table `{in_create_table}`.")
                        in_create_table = None
                    else:
                        # Continue writing CREATE statement
                        # Change collation from "utf8mb4_unicode_ci" to "NOCASE" for SQLite 3 to work
                        replaced_line = stripped_line.replace("utf8mb4_unicode_ci", "NOCASE")
                        outfile.write(replaced_line)

            # Detect and extract multi-line INSERT INTO statements
            for table in table_filters:
                if stripped_line.startswith(f"INSERT INTO `{table}`"):
                    # Start capturing INSERT statement
                    in_insert = table
                    insert_statement = stripped_line
                    break

                if in_insert == table:
                    # For ranks single and ranks average tables take only NRs
                    if in_insert in (TABLE_RANKS_AVERAGE, TABLE_RANKS_SINGLE):
                        if int(stripped_line.strip("(),;").split(",")[-1]) == 1:
                            insert_values.append(stripped_line.rstrip(',;'))

                    # For Persons take only Bulgaria
                    if in_insert == TABLE_PERSONS:
                        if os.environ["WCA_COUNTRY"] in stripped_line:
                            insert_values.append(stripped_line.rstrip(',;'))

                    # End of multi-line INSERT statement
                    if stripped_line.endswith(";"):
                        # Join INSERT statement with all values for insertion
                        if len(insert_values) > 0:
                            joined_inserts = insert_statement + " " + ", ".join(insert_values) + ";\n"
                            outfile.write(joined_inserts)
                        # Reset tracking
                        in_insert = insert_statement = None
                        insert_values = []

            # Detect if the tables have been extracted to their fullest
            for table in table_filters:
                if f"ALTER TABLE `{table}` ENABLE KEYS" in line:
                    logger.info(f"Processed all INSERT statements for table `{table}`.")
                    sql_tables_flags[table]["insert_processed"] = True

            # Check if all tables have been extracted
            if all(flag['create_processed'] and flag['insert_processed'] for flag in sql_tables_flags.values()):
                break

    logger.info(f"Finished filtering SQL dump. Output - {filtered_sql_dump_filename}")


def create_flags_dict(table_filters: dict[str, Any]) -> dict[str, Any]:
    """
    Transforms table_filters dictionary into a new dictionary with boolean flags
    for whether the CREATE TABLE and INSERT INTO statements have been processed.

    :param table_filters: (dict) The dictionary containing table names and their respective filter values.

    :return: (dict) A new dictionary with the flags for 'create_processed' and 'insert_processed' for each table.
    """

    flags_dict = {}
    for table in table_filters:
        flags_dict[table] = {
            'create_processed': False,  # Flag for CREATE TABLE processing
            'insert_processed': False  # Flag for INSERT INTO processing
        }

    return flags_dict
