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


class BuilderConfig(object):
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
        'buckets': 'list[str]',
        'tags': 'list[BuilderTagsType]',
        'functions': 'list[BuilderFunctionsType]',
        'aggregate_window': 'BuilderConfigAggregateWindow'
    }

    attribute_map = {
        'buckets': 'buckets',
        'tags': 'tags',
        'functions': 'functions',
        'aggregate_window': 'aggregateWindow'
    }

    def __init__(self, buckets=None, tags=None, functions=None, aggregate_window=None):  # noqa: E501,D401,D403
        """BuilderConfig - a model defined in OpenAPI."""  # noqa: E501
        self._buckets = None
        self._tags = None
        self._functions = None
        self._aggregate_window = None
        self.discriminator = None

        if buckets is not None:
            self.buckets = buckets
        if tags is not None:
            self.tags = tags
        if functions is not None:
            self.functions = functions
        if aggregate_window is not None:
            self.aggregate_window = aggregate_window

    @property
    def buckets(self):
        """Get the buckets of this BuilderConfig.

        :return: The buckets of this BuilderConfig.
        :rtype: list[str]
        """  # noqa: E501
        return self._buckets

    @buckets.setter
    def buckets(self, buckets):
        """Set the buckets of this BuilderConfig.

        :param buckets: The buckets of this BuilderConfig.
        :type: list[str]
        """  # noqa: E501
        self._buckets = buckets

    @property
    def tags(self):
        """Get the tags of this BuilderConfig.

        :return: The tags of this BuilderConfig.
        :rtype: list[BuilderTagsType]
        """  # noqa: E501
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Set the tags of this BuilderConfig.

        :param tags: The tags of this BuilderConfig.
        :type: list[BuilderTagsType]
        """  # noqa: E501
        self._tags = tags

    @property
    def functions(self):
        """Get the functions of this BuilderConfig.

        :return: The functions of this BuilderConfig.
        :rtype: list[BuilderFunctionsType]
        """  # noqa: E501
        return self._functions

    @functions.setter
    def functions(self, functions):
        """Set the functions of this BuilderConfig.

        :param functions: The functions of this BuilderConfig.
        :type: list[BuilderFunctionsType]
        """  # noqa: E501
        self._functions = functions

    @property
    def aggregate_window(self):
        """Get the aggregate_window of this BuilderConfig.

        :return: The aggregate_window of this BuilderConfig.
        :rtype: BuilderConfigAggregateWindow
        """  # noqa: E501
        return self._aggregate_window

    @aggregate_window.setter
    def aggregate_window(self, aggregate_window):
        """Set the aggregate_window of this BuilderConfig.

        :param aggregate_window: The aggregate_window of this BuilderConfig.
        :type: BuilderConfigAggregateWindow
        """  # noqa: E501
        self._aggregate_window = aggregate_window

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
        if not isinstance(other, BuilderConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
