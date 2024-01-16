# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 6 - DDL and DML Practice
# Alexis Gonzalez

import Assignment5 as as5


def main():
    comments, queries = as5.read_queries("Assignment6.sql")
    as5.process_queries(comments, queries, "udb", "Assignment 6")

    comments, queries = as5.read_queries("Analytics.sql")
    as5.process_queries(comments, queries, "udb", "Assignment 6a")

if __name__ == '__main__':
    main()