# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 5 - Tables, views, and meta-data
# Alexis Gonzalez
import Assignment3 as as3
import OutputUtil as ou


# [6] Define a function that
# Reads the SQL file
# Parses into a list of queries separated by semicolons (the SQL convention)
# Separates the comment part from the query part
# Executes each query using run_query
# Logs each query along with its comment (you get this automatically when executing vis run_query)
# Collects the headers and data that are returned and uses that to build an HTML table
# Gathers all the tables into a single HTML file, with the "Table of Contents" at the top

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_number(x):
    return isinstance(x, int) or isinstance(x, float) or (isinstance(x, str) and is_float(x))
def process_queries(comments, queries, db, assignment):
        tables = []
        for i in range(len(queries)):
            query = queries[i]
            comment = comments[i]
            try:
                headers, data = as3.run_query(query, comment, db, assignment)
                if len(headers) == 0:
                    continue
                numeric = [all([is_number(data[i][j]) for i in range(len(data))]) for j in range(len(data[0]))]
                types = ["N" if numeric[j] else "S" for j in range(len(numeric))]
                alignments = ["r" if numeric[j] else "l" for j in range(len(numeric))]
                table = [comment, headers, types, alignments, data]
                tables.append(table)
            except Exception as e:
                print(f"Error processing query: {query}\nError: {e}\n\n")
        output_file = assignment.replace(" ", "") + ".html"
        title = f"All Queries for '{assignment}'"
        ou.write_html_file_new(output_file, title, tables, True, None, True)

# [7] Define a function that
# Collects the queries recorded for each assignment separately
# Makes a table of queries for each assignment to date
# Gathers all the tables into a single HTML file, with the "Table of Contents" at the top

def read_queries(file_name):
    with open(file_name, "r") as file:
        comments = []
        sqls = []
        text = file.read()
        queries = text.strip().split(';')
        for query in queries:
            if len(query.strip()) == 0:
                continue
            if "*/" in query:
                comment, sql = query.split("*/", 1)
                comment = comment.replace("/*", "").strip()
            else:
                comment = f"Query from: '{file_name}'"
                sql = query
            sql = sql.strip()
            if "CREATE FUNCTION" in sql.upper() or "CREATE PROCEDURE" in sql.upper():
                sql = sql.replace("##", ";")
                print(f"REPLACED ## {sql}")
            comments.append(comment)
            sqls.append(sql)

        return comments, sqls


def retrieve_query_log(assignments, db):
    tables = []
    for assignment in assignments:
        sql = f"select * from query where query_assn = '{assignment}'"
        desc = f"Retrieve all Queries Executed for {assignment}"
        headers, data = as3.run_query(sql, desc, db, assignments[-1])
        alignments = ["l"] * len(headers)
        types = ["S"] * len(headers)
        table = [desc, headers, types, alignments, data]
        tables.append(table)
    output_file = assignment.replace(" ", "") + "-query-history.html"
    title = "All Queries for Assignments to Date"
    ou.write_html_file_new(output_file, title, tables, True, None, True)

def main():
    comments, queries = read_queries("Assignment4.sql")
    process_queries(comments, queries, "udb", "Assignment 4")

    comments, queries = read_queries("Assignment5.sql")
    process_queries(comments, queries, "udb", "Assignment 5")

    # assignments = [f"Assignment {i}" for i in range(3,6)]
    # retrieve_query_log(assignments, "udb")

    comments, queries = read_queries("Analytics.sql")
    process_queries(comments, queries, "udb", "Assignment 5 Analytics")

if __name__ == '__main__':
    main()