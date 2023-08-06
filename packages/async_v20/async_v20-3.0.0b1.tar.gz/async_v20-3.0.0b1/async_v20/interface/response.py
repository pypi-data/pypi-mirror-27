import ujson as json
from ..definitions.base import Specifier
from operator import itemgetter

class Response(dict):
    """A response from OANDA.

    Allows dotted attribute access
    """
    def __init__(self, data, status, bool):
        super().__init__(data)
        self.status = status
        self.bool = bool

    def __bool__(self):
        """Returns True if response contains data as per the OANDA spec.

        Returns false if a status code not defined in the endpoint spec was returned
        """
        return self.bool

    def __repr__(self):
        keys = ', '.join(self.keys())
        return f'<Status [{self.status}]: {keys}>'

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("No such attribute: " + name)

    def dict(self, json=False):
        """Convert the response to a nested dictionary

        Args:

            json: Convert object attributes to the :term:`JSON` representation

        """

        def value_to_dict(value):
            try:
                # If value is an Model object
                result = value.dict(json)
            except AttributeError:
                try:
                    result = [obj.dict(json) for obj in value]
                except (AttributeError, TypeError):
                    if json and isinstance(value, Specifier):
                        # Specifiers need to be strings for JSON
                        result = str(value)
                    else:
                        result = value
            return result

        return {key: value_to_dict(value) for key, value in self.items()}

    def json(self):
        """Return the json equivalent of the response"""
        return json.dumps(self.dict(json=True))
