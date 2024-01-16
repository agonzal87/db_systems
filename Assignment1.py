# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 1 - Relational Model and Algebra
# Alexis Gonzalez
import copy
import texttable

# create a copy of the table with the old column heading replaced with the new one
def rename(table,old_column_name,new_column_name):
    table2 = copy.deepcopy(table)
    for j in range(len(table2[0])):
        if table2[0][j] == old_column_name:
            table2[0][j] = new_column_name
    return table2

# return a table of all rows that satisfy the criteria,
#     a tuple of the form (column_name,column_value)
# if no criteria is provided, return all rows
def select(table,predicate=None):
    if predicate is None:
        return
    headers = table[0]
    table2 = []
    for row in table[1:]:
        for j in range(len(row)):
            # predicate[0] is column name, predicate[1] is column value
            if predicate[0] == headers[j] and predicate[1] == row[j]:
                table2.append(row)
    return [headers] + table2

# returns a new 2-D table with only the column names provided in the list column_names
# if column_names is “*”, then include all columns
def project(table, column_names=["*"]):
    if column_names is None:
        return table
    table2 = []
    headers = table[0]
    headers2 = []
    for j in range(len(headers)):
        if headers[j] in column_names:
            headers2.append(headers[j])

    for row in table[1:]:
        row2 = []
        for j in range(len(row)):
            if headers[j] in column_names:
                row2.append(row[j])
        table2.append(row2)
    return [headers2] + table2

def display(table, title = "Title"):
    headers = table[0]
    data = table[1:]
    alignments = ["l"] * len(headers)
    print_table(title, headers, data, alignments)

def print_table(title, headers, data, alignments):
   tt = texttable.Texttable(0)
   tt.set_cols_align(alignments)
   tt.add_rows([headers] + data, True)
   print(title)
   print(tt.draw())
   print()

def create(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        table = [line.strip().split(",") for line in lines]
    return table

# create a sorted copy of the table in ascending order by the values in column column_name
def sort(table,column_name):
    headers = table[0]
    idx = table[0].index(column_name)
    table2 = sorted(table[1:], key=lambda l: l[idx])
    return [headers] + table2


def main():
    countries = create('countries.csv')
    cities = create('cities.csv')
    display(countries, "Countries")
    display(cities, "Cities")

    display(rename(rename(cities, "CityName", "Name"), "CityPopulation", "Population"), "Cities")

    countries_capital = project(countries, ["Name", "Capital"])
    display(countries_capital, "Country Capitals")

    countries_india = select(countries, ["Name", "India"])
    display(countries_india, "India")

    display(sort(countries, "Name"), "Countries in Alphabetical Order")

if __name__ == '__main__':
    main()
