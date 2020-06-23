import sqlite3
import unittest
import requests
from sqlite3 import Error

from main import database
from main.swa_api_caller import aggregate_requests


class TestDatabaseMethods(unittest.TestCase):
    def test_aggregate_results(self):
        """
        tests if aggregate_results functions correctly
        :return:
        """
        answer = requests.get('https://swapi.dev/api/people/').json()['count']
        results = len(aggregate_requests(requests.get('https://swapi.dev/api/people/')))
        self.assertEqual(results, answer)

    def test_add_people(self):
        """
        test that add_people is adding the correct number of people
        :return:
        """
        conn = None
        try:
            conn = sqlite3.connect('test.db')
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

        results = aggregate_requests(requests.get('https://swapi.dev/api/people/'))
        database.create_table(conn)
        for each in results:
            film_string = each['films'][0]
            for x in range(1, len(each['films'])):
                film_string += ", " + each['films'][x]

            if each['species']:
                # checking to see if species is empty
                species_string = each['species'][0]
                for x in range(1, len(each['species'])):
                    film_string += ", " + each['species'][x]
            else:
                species_string = ''

            if each['vehicles']:
                # checking to se if vehicles is empty
                vehicles_string = each['vehicles'][0]
                for x in range(1, len(each['vehicles'])):
                    film_string += ", " + each['vehicles'][x]
            else:
                vehicles_string = ''

            data_tuple = (each['name'], each['height'], each['mass'], each['hair_color'], each['skin_color'],
                          each['eye_color'], each['birth_year'], each['gender'], each['homeworld'], film_string,
                          species_string, vehicles_string, each['created'], each['edited'], each['url'])
            database.add_people(data_tuple, conn)
        # checks to see if you can find the name luke skywalker (if this collumn is right rest should be good)
        # TODO: realistically should test rest of collumns
        select_single_person = """ SELECT * FROM people WHERE name = 'Luke Skywalker'"""
        cursor = conn.cursor()
        single_name = cursor.execute(select_single_person).fetchall()
        self.assertEqual(single_name[0][1], 'Luke Skywalker')
        #checks the number of entries should be matching number of people results from api call
        select_all_rows = """SELECT * FROM people"""
        all_rows = cursor.execute(select_all_rows).fetchall()
        self.assertEqual(len(results), len(all_rows))


if __name__ == '__main__':
    unittest.main()