import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('starwars_database.db')
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def create_table(conn):
    """
    Since SQLITE doesn't allow array of foreign keys as a datatype we create a reference table
    (people_starships_relationships) that holds all the relatinoships between people and starships
    as references to unique URL's from each table.
    """
    table_type_list = [
        '''CREATE TABLE IF NOT EXISTS people (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    height integer,
                    mass integer,
                    hair_color text,
                    skin_color text,
                    eye_color text,
                    birth_year text,
                    gender text,
                    homeworld text,
                    films blob,
                    species blob,
                    vehicles blob,
                    created text,
                    edited text,
                    url text);''',
        '''CREATE TABLE IF NOT EXISTS starships (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        model text,
                        manufacturer text,
                        cost_in_credits text,
                        length text,
                        max_atmosphering_speed text,
                        crew text,
                        passengers text,
                        cargo_capacity text,
                        consumables text,
                        hyperdrive_rating text,
                        MGLT text,
                        starship_class text,
                        films blob,
                        created text,
                        edited text,
                        url text);''',
        '''CREATE TABLE IF NOT EXISTS people_starships_relationships (
                                            people_reference text,
                                            starship_reference text);'''
    ]
    try:
        c = conn.cursor()
        for each in table_type_list:
            c.execute(each)
    except Error as e:
        print(e)

"""
TODO: for all three add_foo functions, add a check to see if a similar entry exists and
return if it does. 
"""
def add_people(person_data, conn):
    """
    add single row to people table
    :param tuple person_data: collected data from single entry from response for people
    :param sqlite database connection conn: connection to database
    :return:
    """
    sql = ''' INSERT INTO people(name, height, mass, hair_color, skin_color, eye_color, birth_year,
            gender, homeworld, films, species, vehicles, created, edited, url) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person_data)
    return cur.lastrowid


def add_starships(ship_data, conn):
    """
    add single row to starships tables
    :param tuple ship_data: collected data from single entry from response for starships
    :param sqlite database connection conn: connection to database
    :return:
    """

    sql = ''' INSERT INTO starships(name, model, manufacturer, cost_in_credits, length,
            max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, hyperdrive_rating,
            MGLT, starship_class, films, created, edited, url) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, ship_data)


def add_people_starships_relationship(relationship_dict, conn):
    """
    takes dictionary of relationships and iterates over them to add to relationship table
    :param relationship_dict: dict of people ship relationship PERSON_URL:[SHIP_URLS]
    :param conn: SQLITE database conneciton
    :return:
    """
    sql = ''' INSERT INTO people_starships_relationships(people_reference, starship_reference)
            VALUES(?,?) '''
    for key in relationship_dict:
        for value in relationship_dict[key]:
            to_insert = (key, value)
            cur = conn.cursor()
            cur.execute(sql, to_insert)
