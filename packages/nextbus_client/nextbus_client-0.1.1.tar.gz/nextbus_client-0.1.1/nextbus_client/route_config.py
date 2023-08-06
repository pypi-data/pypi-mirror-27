"""
route_config.py - Class models a RouteConfig and related objects from the NextBus API
"""
from .utilities import validate_xml_element


class RouteConfig(object):
    """
    Class models a Route Configuration for the NextBus API service.
    """
    ELEMENT_TAG = 'route'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the RouteConfig attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs. For directions, stops, and paths a list of
        the related Direction, Stop, or Path objects can be given in kwargs. If an xml_element is given the class
        will parse the sub-elements to a list of the appropriate object time instead.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        directions = None
        stops = None
        paths = None
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)
            directions = [Direction(xml_element=e) for e in source.getchildren() if e.tag == Direction.ELEMENT_TAG]
            stops = [Stop(xml_element=e) for e in source.getchildren() if e.tag == Stop.ELEMENT_TAG]
            paths = [Path(xml_element=e) for e in source.getchildren() if e.tag == Path.ELEMENT_TAG]

        self.tag = source.get('tag', '')
        self.title = source.get('title', '')
        self.region_title = source.get('regionTitle', '')
        self.short_title = source.get('shortTitle', '')
        self.color = source.get('color', '')
        self.opposite_color = source.get('oppositeColor', '')
        self.lat_min = source.get('latMin', '')
        self.lat_max = source.get('latMax', '')
        self.lon_min = source.get('lonMin', '')
        self.lon_max = source.get('lonMax', '')
        self.directions = directions or source.get('directions', [])
        self.stops = stops or source.get('stops', [])
        self.paths = paths or source.get('paths', [])

    def to_dict(self):
        """
        Parse the RouteConfig to a dictionary.

        :return: Dictionary of Route attributes
        """
        return {'tag': self.tag,
                'title': self.title,
                'regionTitle': self.region_title,
                'shortTitle': self.short_title,
                'color': self.color,
                'oppositeColor': self.opposite_color,
                'latMin': self.lat_min,
                'latMax': self.lat_max,
                'lonMin': self.lon_min,
                'lonMax': self.lon_max,
                'directions': [d.to_dict() for d in self.directions],
                'stops': [s.to_dict() for s in self.stops],
                'paths': [p.to_list() for p in self.paths]}


class Direction(object):
    """
    Class models a Direction for a Route
    """
    ELEMENT_TAG = 'direction'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the Direction attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs.

        :param kwargs: keyword arguments for Direction object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        stops = None
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)
            stops = [Stop(xml_element=e) for e in source.getchildren() if e.tag == Stop.ELEMENT_TAG]

        self.tag = source.get('tag', '')
        self.title = source.get('title', '')
        self.name = source.get('name', '')
        self.use_for_ui = bool(source.get('useForUI', False))
        self.stops = stops or source.get('stops', [])

    def to_dict(self):
        """
        Parse the Direction to a dictionary for easier json conversion.
        :return: Dictionary of Direction attributes
        """
        return {'tag': self.tag,
                'title': self.title,
                'name': self.name,
                'useForUI': self.use_for_ui,
                'stops': [s.to_dict() for s in self.stops]}


class Stop(object):
    """
    Class models a Stop for a Route or Direction
    """
    ELEMENT_TAG = 'stop'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the Stop attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs.

        :param kwargs: keyword arguments for Stop object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)

        self.tag = source.get('tag', '')

        # Some versions of Stop have additional attributes. Only add them to the class if they exist.
        title = source.get('title')
        if title:
            self.title = title

        short_title = source.get('shortTitle')
        if short_title:
            self.short_title = short_title

        lat = source.get('lat')
        if lat:
            self.lat = lat

        lon = source.get('lon')
        if lon:
            self.lon = lon

    def to_dict(self):
        """
        Parse the Stop to a dictionary.

        :return: Dictionary of Stop attributes
        """
        stop = {'tag': self.tag}
        if hasattr(self, 'title'):
            stop['title'] = self.title
        if hasattr(self, 'short_title'):
            stop['shortTitle'] = self.short_title
        if hasattr(self, 'lat'):
            stop['lat'] = self.lat
        if hasattr(self, 'lon'):
            stop['lon'] = self.lon

        return stop


class Path(object):
    """
    Class models a Path for a Route
    """
    ELEMENT_TAG = 'path'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the Stop attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs. In this case points can be a
        list of Point objects given as the kwarg 'points'. If an xml element attribute is given it will
        parse the points from the xml as though a 'path' element was given instead.

        :param kwargs: keyword arguments for Stop object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)
            self.points = [Point(xml_element=e) for e in source.getchildren() if e.tag == 'point']
        else:
            self.points = source.get('points', [])

    def to_list(self):
        """
        Parse the Path to a list of Points as dictionaries for easy json conversion.

        :return: List of Path attributes with Points as dictionaries.
        """
        path = []
        for point in self.points:
            path.append(point.to_dict())

        return path


class Point(object):
    """
    Class models a Point for a Path
    """
    ELEMENT_TAG = 'point'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the Route attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs.get('xml_element', None) or kwargs

        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)

        self.lat = source.get('lat', '')
        self.lon = source.get('lon', '')

    def to_dict(self):
        """
        Parse the Path to a dictionary.

        :return: Dictionary of Path attributes
        """
        return {'lat': self.lat,
                'lon': self.lon}
