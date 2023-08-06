import json
from requests.models import Response

CLASS_NAME = u'class_name'
KEY = u'key'
MANDATORY = u'mandatory'
OPTIONAL = u'optional'
PROPERTY = u'property'
TYPE = u'type'
PROPERTY_NAME = u'property_name'
PROPERTIES = u'properties'
DEFAULT = u'default'
ATTRIBUTES = u'attributes'
FILENAME = u"filename"
MIXIN_IMPORTS = u'mixin_imports'


class MandatoryFieldMissing(Exception):
    pass


class JsonApiPropertiesClass(object):

    def __init__(self,
                 response=None,
                 parent=None):
        """
        Provides base class for API classes that use properties instead of
        keys into a dictionary.

        It's not mandatory to call __init__. You can explicitly set self.response_dict instead
        if that makes more sense in your subclass

        :param response: One of: None - Expect the request method to be overriden that returns
                                        one of the remaining response types...
                                 requests.models.Response - request has already been made
                                 JSON String - request has been made / this is part of a response
                                               hierarchy.
                                 Dictionary - JSON has already been unpacked. (Don't supply lists)
        :param parent: Can pass the parent object, so that a subclass can access its properties.
                       Useful inside the request method, for example.
        """

        if response is None:
            # No response, must fetch
            response = self.request()

        if isinstance(response, Response):
            self._response = response
            response = response.json()

        try:
            self.response_dict = json.loads(response)
        except:
            self.response_dict = response

        self.parent = parent
        super(JsonApiPropertiesClass, self).__init__()  # Required for co-operative multiple inheritance

    def request(self):
        raise NotImplementedError(u'request==None passed for {cls} where the request method has not be overridden'
                                  .format(cls=unicode(self.__class__)))

    def mandatory(self,
                  key):
        try:
            return self.response_dict[key]
        except KeyError:
            raise MandatoryFieldMissing(key)

    def optional(self,
                 key,
                 default=None):
        return self.response_dict.get(key, default)

    def get_property(self,
                     item):
        try:
            return getattr(self, item)
        except AttributeError:
            pass
        try:
            return getattr(self.parent.item)
        except AttributeError as ae:
            pass
        try:
            return self.parent.get_property(item)
        except AttributeError as ae:
            raise ValueError(u'Could not find "{item}" in object tree'.format(item=item))
