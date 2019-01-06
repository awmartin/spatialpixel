"""Provides a basic object to query and render OpenStreetMap data."""

import json
import urllib
import urllib2


class OpenStreetMap(object):
    """Represents a query to the OpenStreetMap API."""

    def __init__(self, query=None, bbox=None):
        self.query = query
        self.bbox = bbox

        self.data = None
        self.entities = None
        self.terms = []
    
    def set_map(self, slippymap):
        self.set_bounding_box(*slippymap.bbox)
    
    def set_bounding_box(self, latsouth, lonwest, latnorth, loneast):
        self.bbox = (latsouth, lonwest, latnorth, loneast)

    def set_query(self, query):
        self.query = query

    @property
    def query_format(self):
        return "[out:json]"
    
    @property
    def query_bbox(self):
        return "[bbox:{:f},{:f},{:f},{:f}]".format(*self.bbox)
    
    def request(self):
        if self.query is None:
            if len(self.terms) > 0:
                self.query = ""
                for term in self.terms:
                    self.query += term.term

        if self.query is None:
            return

        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = self.query_format + self.query_bbox + ";"
        overpass_query += """(%s);
out body;
>;
out skel qt;""" % self.query

        params = {'data': overpass_query}
        data = urllib.urlencode(params)
        req = urllib2.Request(overpass_url, data)
        
        response = urllib2.urlopen(req)
        contents = response.read()

        self.data = json.loads(contents)
        self._parse()

    def _parse(self):
        if self.data is None:
            return

        # Gather all the nodes and ways into referenceable dictionaries.
        nodes = {}
        ways = {}
        for elt in self.data['elements']:
            if 'type' in elt:
                if elt['type'] == 'node':
                    nodeid = elt['id']
                    nodes[nodeid] = elt
                elif elt['type'] == 'way':
                    wayid = elt['id']
                    ways[wayid] = elt

        self.entities = {'nodes': nodes, 'ways': ways}
    
    def add(self, term):
        self.terms.append(term)


class Query(object):
    def __init__(self):
        pass


class QueryTerm(object):
    def __init__(self, tags=None):
        self.tags = []

        if tags is not None:
            if isinstance(tags, str):
                self.tags.append(TagFilter(tags, None))
            elif isinstance(tags, dict):
                for key, value in tags.iteritems():
                    self.tags.append(TagFilter(key, value))

    def add_tag(self, key, value):
        self.tags.append(TagFilter(key, value))

    @property
    def term(self):
        return ""

    def __str__(self):
        return "QueryTerm"


class Relation(QueryTerm):
    @property
    def term(self):
        return "relation%s;" % "".join(map(str, self.tags))


class Way(QueryTerm):
    """Represents an OpenStreetMap query term for way[...];"""

    @property
    def term(self):
        return "way%s;" % "".join(map(str, self.tags))


class TagFilter(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return self.term
    
    @property
    def term(self):
        if self.value is None and self.key is not None:
            return "[%s]" % self.key
        if isinstance(self.value, str):
            # If the value is a string, just place it.
            return "[%s=%s]" % (self.key, self.value)
        elif isinstance(self.value, list):
            # If the value is a list of strings, then insert as a regex. For example:
            # way[highway~"^(motorway|trunk|primary|secondary|tertiary|unclassified|residential)$"];
            alternates = "|".join(map(str, self.value))
            return """[%s~"(%s)$"]""" % (self.key, alternates)
        else:
            return "[]"


class OpenStreetMapRender(object):
    pass

