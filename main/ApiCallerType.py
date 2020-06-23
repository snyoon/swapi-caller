import fire
from main.swa_api_caller import call_swapi


class ApiCallerType(object):
    """
    Fire calls on this class to differentiate different API calls.
    Original functionality only requires for starships and people but api takes
    films, people, planets, species, starships, vehicles.
    """

    def films(self):
        """
        todo: add films functionality
        """
        raise fire.core.FireError('swapi-caller does not support films calls at this time')
        return self

    def people(self):
        call_swapi('people')
        return self

    def planets(self):
        """
        todo: add planets functionailty
        """
        raise fire.core.FireError('swapi-caller does not support planets calls at this time')
        return self

    def species(self):
        """
        todo: add species functionailty
        """
        raise fire.core.FireError('swapi-caller does not support species calls at this time')
        return self

    def starships(self):
        call_swapi('starships')
        return self

    def vehicles(self):
        """
        todo: add vehicles functionailty
        """
        raise fire.core.FireError('swapi-caller does not support vehicles calls at this time')
        return self

