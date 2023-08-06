"""
predictions.py - Class models Predictions as returned by the Nexbus API's predictions command.
"""
from .utilities import validate_xml_element


class Predictions(object):
    """
    Class models a Predictions list for the NextBus API service.
    """
    ELEMENT_TAG = 'predictions'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the Predictions or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs. For directions and messages a list of
        the related Direction or Message objects can be given in kwargs. If an xml_element is given the class
        will create the appropriate lists of objects from the child elements.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        directions = None
        messages = None
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)
            directions = [Direction(xml_element=e) for e in source.findall(Direction.ELEMENT_TAG)]
            messages = [Message(xml_element=e) for e in source.findall(Message.ELEMENT_TAG)]

        self.agency_title = source.get('agencyTitle', '')
        self.route_tag = source.get('routeTag', '')
        self.route_code = source.get('routeCode', '')
        self.stop_title = source.get('stopTitle', '')
        self.directions = directions or source.get('directions', [])
        self.messages = messages or source.get('messages', [])
        dir_title = source.get('dirTitleBecauseNoPredictions', None)
        if dir_title:
            self.dir_title = dir_title

    def to_dict(self):
        """
        Convert the Predictions object to a dictionary.

        :return: Dictionary of Predictions attributes.
        """
        predictions_dict = {'agencyTitle': self.agency_title,
                            'routeTag': self.route_tag,
                            'routeCode': self.route_code,
                            'stopTitle': self.stop_title,
                            'directions': [d.to_dict() for d in self.directions],
                            'messages': [m.to_dict() for m in self.messages]}

        if hasattr(self, 'dir_title_because_no_predictions'):
            predictions_dict['dirTitleBecauseNoPredictions'] = self.dir_title

        return predictions_dict


class Direction(object):
    """
    Class models the Direction attribute for predictions.
    """
    ELEMENT_TAG = 'direction'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the RouteConfig attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs. For predictions a list of
        the Prediction objects can be given in kwargs. If an xml_element is given the class
        will create the list of Prediction objects from the appropriate child elements.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        predictions = None
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)
            predictions = [Prediction(xml_element=e) for e in source.findall(Prediction.ELEMENT_TAG)]

        self.title = source.get('title', '')
        self.predictions = predictions or source.get('predictions', [])

    def to_dict(self):
        """
        Convert the Direction attributes to a dictionary.

        :return: Dictionary of Direction attributes.
        """
        return {'title': self.title,
                'predictions': [p.to_dict() for p in self.predictions]}


class Prediction(object):
    """
    Class models the Prediction attribute for directions.
    """
    ELEMENT_TAG = 'prediction'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the RouteConfig attributes or an xml_element.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)

        self.seconds = source.get('seconds', '')
        self.minutes = source.get('minutes', '')
        self.epoch_time = source.get('epochTime', '')
        self.vehicle = source.get('vehicle', '')
        self.vehicles_in_consist = source.get('vehiclesInConsist', '')
        self.is_departure = source.get('isDeparture', False)
        self.block = source.get('block', '')
        self.dir_tag = source.get('dirTag', '')
        self.branch = source.get('branch', '')
        self.affected_by_layover = bool(source.get('affectedByLayover', False))
        self.is_schedule_based = bool(source.get('isScheduleBased', False))
        self.delayed = bool(source.get('delayed', False))

        trip_tag = source.get('tripTag', None)
        if trip_tag:
            self.trip_tag = trip_tag

    def to_dict(self):
        """
        Parses the Prediction object to a dictionary

        :return: Dictionary of Prediction object attributes
        """

        prediction_dict = {'seconds': self.seconds,
                           'minutes': self.minutes,
                           'epochTime': self.epoch_time,
                           'vehicle': self.vehicle,
                           'vehiclesInConsist': self.vehicles_in_consist,
                           'isDeparture': self.is_departure,
                           'block': self.block,
                           'dirTag': self.dir_tag,
                           'branch': self.branch,
                           'affectedByLayover': self.affected_by_layover,
                           'isScheduleBased': self.is_schedule_based,
                           'delayed': self.delayed}

        if hasattr(self, 'trip_tag'):
            prediction_dict['tripTag'] = self.trip_tag

        return prediction_dict


class Message(object):
    """
    Model a message for a Prediction.
    """
    ELEMENT_TAG = 'message'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the RouteConfig attributes or an xml_element.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)

        self.text = source.get('text', '')
        self.priority = source.get('priority', '')

    def to_dict(self):
        """
        Convert Message object to a dictionary.

        :return: Message attributes as a dictionary.
        """

        return {'text': self.text,
                'priority': self.priority}
