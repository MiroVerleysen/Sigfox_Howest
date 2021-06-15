# coding: utf-8

"""
Influx API Service.

No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

OpenAPI spec version: 0.1.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class FluxSuggestion(object):
    """NOTE: This class is auto generated by OpenAPI Generator.

    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'params': 'dict(str, str)'
    }

    attribute_map = {
        'name': 'name',
        'params': 'params'
    }

    def __init__(self, name=None, params=None):  # noqa: E501,D401,D403
        """FluxSuggestion - a model defined in OpenAPI."""  # noqa: E501
        self._name = None
        self._params = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if params is not None:
            self.params = params

    @property
    def name(self):
        """Get the name of this FluxSuggestion.

        :return: The name of this FluxSuggestion.
        :rtype: str
        """  # noqa: E501
        return self._name

    @name.setter
    def name(self, name):
        """Set the name of this FluxSuggestion.

        :param name: The name of this FluxSuggestion.
        :type: str
        """  # noqa: E501
        self._name = name

    @property
    def params(self):
        """Get the params of this FluxSuggestion.

        :return: The params of this FluxSuggestion.
        :rtype: dict(str, str)
        """  # noqa: E501
        return self._params

    @params.setter
    def params(self, params):
        """Set the params of this FluxSuggestion.

        :param params: The params of this FluxSuggestion.
        :type: dict(str, str)
        """  # noqa: E501
        self._params = params

    def to_dict(self):
        """Return the model properties as a dict."""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Return the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`."""
        return self.to_str()

    def __eq__(self, other):
        """Return true if both objects are equal."""
        if not isinstance(other, FluxSuggestion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
