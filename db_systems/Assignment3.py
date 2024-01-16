# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 3 - SQL & Programming Languages
# Alexis Gonzalez
import time
import pymysql
import texttable


def get_password():
    with open('password.txt', 'r') as file:
        return file.read().strip()

password = get_password()
user = "Alexis"

def list_db_data(cursor, sql, desc):
    cursor.execute(sql)
    results = [row[0] for row in cursor]
    print(desc + ":", results)
    return results

def log_query(query_text, query_desc, query_db, query_rows, query_user, query_assn, query_dur, conn = None):
    query_text = query_text.replace("'", "\\'")
    query_desc = query_desc.replace("'", "\\'")
    query = f"INSERT into query (query_text, query_desc, query_db, query_rows, query_user, query_assn, query_dur) \nvalues ('{query_text}','{query_desc}','{query_db}',{query_rows},'{query_user}','{query_assn}',{query_dur})"
    new_conn = False
    if conn is None:
        new_conn = True
        conn = pymysql.connect(host="localhost", user="root", passwd=get_password(), db="udb")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    if new_conn:
        conn.close()

def run_query(query_text, query_desc, query_db, assignment):
    query_src = assignment
    conn = pymysql.connect(host="localhost", user="root", passwd=password, db=query_db)
    start = time.time()
    cursor = conn.cursor()
    if query_text.upper().startswith("CALL"):
        call_procedure(query_text, cursor)
    else:
        cursor.execute(query_text)
    end = time.time()
    duration = end - start
    rows = cursor.fetchall()
    conn.commit()
    log_query(query_text, query_desc, query_db, len(rows), user, query_src, duration)
    conn.close()
    query_upper = query_text.upper()
    if query_upper.startswith("SELECT") or query_upper.startswith("(SELECT") or query_upper.startswith("SHOW") or query_upper.startswith("DESC"):
        headers = [desc[0] for desc in cursor.description]
        if len(rows) == 0:
            data = [[None for _ in headers]]
        else:
            data = [[col for col in row] for row in rows]
        return headers, data
    else:
        return [], []


def call_procedure(query_text, cursor):
    proq_query = query_text[4:].strip()
    idx1 = proq_query.index('(')
    idx2 = proq_query.index(')')
    arg = int(proq_query[idx1 + 1: idx2])
    proc = proq_query[:idx1]
    print(f"PROC QUERY {proc}")
    cursor.callproc(proc, (arg,))

def print_table(title, headers, data, alignments = None):
   if alignments is None:
       alignments = ['l'] * len(headers)
   tt = texttable.Texttable(0)
   tt.set_cols_align(alignments)
   tt.add_rows([headers] + data, header=True)
   print(title)
   print(tt.draw())

def preliminary(password):
    conn = pymysql.connect(host="localhost", user="root", passwd=password)
    cursor = conn.cursor()
    databases = list_db_data(cursor, "SHOW DATABASES", "Databases")
    cursor.execute("USE udb")
    tables = list_db_data(cursor, "SHOW TABLES", "Tables in udb")
    for table in tables:
        columns = list_db_data(cursor, "DESC " + table, "Columns in table " + table)
    conn.cursor()
    return tables

def main():
    assignment = "Assignment 3"
    password = get_password()
    tables = preliminary(password)
    for table in tables:
        query = "select * from " + table
        desc = "retrieve all rows from table " + table
        headers, data = run_query(query, desc, "udb", assignment)
        print_table("table " + table, headers, data)

if __name__ == '__main__':
    main()