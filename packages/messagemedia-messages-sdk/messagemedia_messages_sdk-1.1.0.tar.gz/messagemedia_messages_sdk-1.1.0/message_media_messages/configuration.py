# -*- coding: utf-8 -*-

"""
   message_media_messages.configuration

"""
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
    are accessible without instance creation.

    """

    # Set the array parameter serialization method
    # (allowed: indexed, unindexed, plain, csv, tsv, psv)
    array_serialization = "indexed"

    # The base Uri for API calls
    base_uri = 'http://api.messagemedia.com'

    # The username to use with basic authentication
    # TODO: Set an appropriate value
    basic_auth_user_name = "TODO: Replace"

    # The password to use with basic authentication
    # TODO: Set an appropriate value
    basic_auth_password = "TODO: Replace"

    # The username to use with HMAC authentication
    # TODO: Set an appropriate value
    hmac_auth_user_name = None

    # The password to use with HMAC authentication
    # TODO: Set an appropriate value
    hmac_auth_password = None

