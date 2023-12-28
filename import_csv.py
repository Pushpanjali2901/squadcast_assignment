from connection import connect_to_postgres
import pandas as pd
import json

connection = connect_to_postgres()


def import_movies(path):
    file = open(path, 'r', encoding='utf-8')           #Opens the given file
    data = pd.read_csv(file)                           #Read the file

    # The code for transferring the csv data to database table
    cursor = connection.cursor()                      
    table_name = 'movies'
    column_names = json.dumps(("id", "title", "year", "country", "genre", "director", "minutes", "posters"))
    insert_query = "INSERT INTO {} {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s);".format(table_name, column_names).replace('[', '(').replace(']', ')')

    for index in data.index:
        print(index)
        try:
            values = (str(data["id"][index]),
                    str(data["title"][index]),
                    str(data["year"][index]),
                    str(data["country"][index]),
                    str(data["genre"][index]),
                    str(data["director"][index]),
                    str(data["minutes"][index]),
                    str(data["poster"][index])
                    )
            cursor.execute(insert_query, values)
            connection.commit()
        except:
            pass
    
    cursor.close()
    connection.close()

import_movies('movies.csv')
