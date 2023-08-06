import requests
from urlparse import urljoin
from utils import transform_to_json


class QueryResult(object):
    def __init__(self, response):
        self.response = response

    @property
    def __rows(self):
        return self.response['rows']

    @property
    def __headers(self):
        return self.headers['rows']

    def rows(self):
        rows = self.__rows
        for row in rows:
            yield transform_to_json(row)

    def __str__(self):
        return "<Results len = %s>" % len(self.__rows)


class FoxtrotException(Exception):
    def __init__(self, message):
        self.message = message


class Foxtrot(object):
    def __init__(self, uri):
        self.uri = uri
        self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def select(self, query):
        api = urljoin(self.uri, 'foxtrot/v1/fql')
        print api
        try:
            res = requests.post(api, data=query, headers=self.headers, timeout=2)
            if res.status_code == 204:
                return QueryResult({'rows': [], 'headers': []})
            if res.status_code != 200:
                raise FoxtrotException("Bad Query ")
            return QueryResult(res.json())
        except requests.exceptions.ConnectionError:
            raise FoxtrotException("Could not connect to node")
        except ValueError as e:
            raise FoxtrotException("Unknown response"+e)
