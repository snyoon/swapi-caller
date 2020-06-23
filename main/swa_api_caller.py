import requests
import main.database as database


def call_swapi(command_type):
    """
    Does the initial call the swapi.dev
    :param string command_type: type of api call (people, starship, etc..)
    :return:
    """

    # aggregate all the results into a single list.
    # checks to see if api call is valid/good, if not kicks out with RequestException
    try:
        results = aggregate_requests(requests.get('https://swapi.dev/api/{}'.format(command_type)))
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    conn = database.create_connection()
    if conn is not None:
        database.create_table(conn)
    else:
        print("Error! Cannot create the database connection.")

    people_starships_dict = {}
    # Adds api call to db depending on api call type. currently on people & starship calls are supported
    # TODO have to add a way to check that there has been a change from the last time it was called before executing
    if command_type == 'people':
        for each in results:
            '''
            add relationship information to dictionary to later add to table
            assumes each person knows about all related starships
            
            checks to see if starships field is empty if it is skips over this part
            '''
            if each['starships']:
                people_starships_dict[each['url']] = []
                for ship in each['starships']:
                    people_starships_dict[each['url']].append(ship)

            '''
            TODO: films, species, vehicles should all have their seperate table related to each entry in people
            currently the api result is just translated to a string representation.
            '''
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
    elif command_type == 'starships':
        for each in results:
            '''
            TODO: films should have its own seperate table related to each entry in starships
            currently the api result is just translated to a string representation.
            '''
            film_string = each['films'][0]
            for x in range(1, len(each['films'])):
                film_string += ", " + each['films'][x]

            data_tuple = (each['name'], each['model'], each['manufacturer'], each['cost_in_credits'], each['length'],
                          each['max_atmosphering_speed'], each['crew'], each['passengers'], each['cargo_capacity'],
                          each['consumables'], each['hyperdrive_rating'], each['MGLT'], each['starship_class'],
                          film_string, each['created'], each['edited'], each['url'])
            database.add_starships(data_tuple, conn)
    database.add_people_starships_relationship(people_starships_dict, conn)

    conn.commit()
    conn.close()


def aggregate_requests(request):
    """
    recursivly call onto 'next' in the api requests till there are no more pages
    :param request: a single request page from swapi.dev
    :return: json array of all results from swapi.dev
    """
    json_request = request.json()
    if json_request['next']:
        return json_request['results'] + aggregate_requests(requests.get(json_request['next']))
    else:
        return json_request['results']