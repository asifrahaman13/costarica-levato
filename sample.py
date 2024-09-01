from tabulate import tabulate


# Pretty print class to print data from data frame in a tabular format
class PrettyPrint:

    @staticmethod
    def print_dataframe(data: dict, title: str):
        print(f"{title}")
        print(tabulate(data, headers="keys", tablefmt="grid"))


import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")


from enum import Enum

# All the operators that can be used in the SQL queries
class SQLOperator(Enum):
    INCLUDES = "includes"
    GREATER_THAN_EQUAL_TO = "greater-than-equal-to"
    LESS_THAN_EQUAL_TO = "less-than-equal-to"


class SQLFilter:
    def __init__(self, connection):
        self.connection = connection

    def generate_sql_condition(self, condition):
        col_name, operator, value = condition
        table_alias, column_name = col_name.split(".")

        # Generate the SQL condition based on the operator
        if operator == SQLOperator.INCLUDES.value:
            value = tuple(value) if len(value) > 1 else f"('{value[0]}')"
            return f"{table_alias}.{column_name} IN {value}", []
        elif operator == SQLOperator.GREATER_THAN_EQUAL_TO.value:
            return f"{table_alias}.{column_name} >= %s", [value]
        elif operator == SQLOperator.LESS_THAN_EQUAL_TO.value:
            return f"{table_alias}.{column_name} <= %s", [value]
        else:
            raise ValueError(f"Unsupported condition: {operator}")

    def filter_data(self, filter_conditions, output_columns):
        cursor = self.connection.cursor()

        # Generate SQL WHERE conditions from the filter conditions
        where_conditions = []
        parameters = []

        for condition in filter_conditions:
            condition_str, condition_params = self.generate_sql_condition(condition)
            where_conditions.append(condition_str)
            parameters.extend(condition_params)

        where_clause = " AND ".join(where_conditions)

        # Generate the SELECT clause with table aliases
        select_clause = ", ".join(
            (
                f"ea.{col}" if col in ["event_city", "event_name", "event_country", "event_start_date"]
                else f"ca.{col}" if col in ["company_industry", "company_name", "company_url"]
                else f"pa.{col}" if col in ["person_first_name", "person_last_name", "person_seniority"]
                else col
            )
            for col in output_columns
        )

        # Define the SQL query
        query = f"""
            SELECT {select_clause}
            FROM event_attributes ea
            JOIN company_attributes ca ON ea.event_url = ca.event_url
            LEFT JOIN people_attributes pa ON ca.company_url = pa.company_url
            WHERE {where_clause};
        """

        # Print the query and parameters for debugging
        print("Executing SQL query:")
        print(query)
        print("With parameters:")
        print(parameters)

        # Execute the query with parameters
        cursor.execute(query, tuple(parameters))
        result = cursor.fetchall()

        # Extract column names from the select clause for DataFrame
        columns = [col.split('.')[-1] for col in select_clause.split(', ')]

        # Convert the result to a pandas DataFrame
        result_df = pd.DataFrame(result, columns=columns)

        return result_df
    

# Establishing the connection
connection = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port,
)

# Instantiate the SQLFilter class
sql_filter = SQLFilter(connection)


# Define filter arguments and output columns
filter_arguments = [
    ["pa.person_first_name", "includes", ["John"]],
]
output_columns = [
    "person_first_name",
]

# Apply the filter and get the results
result_df = sql_filter.filter_data(filter_arguments, output_columns)
PrettyPrint.print_dataframe(result_df, "Filtered Result")