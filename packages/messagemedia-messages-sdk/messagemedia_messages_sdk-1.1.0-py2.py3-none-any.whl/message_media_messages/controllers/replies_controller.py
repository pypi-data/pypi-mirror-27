# -*- coding: utf-8 -*-

"""
    message_media_messages.controllers.replies_controller

"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..models.check_replies_response import CheckRepliesResponse
from ..exceptions.api_exception import APIException


class RepliesController(BaseController):

    """A Controller to access Endpoints in the message_media_messages API."""

    def __init__(self, client=None, call_back=None):
        super(RepliesController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def create_confirm_replies_as_received(self,
                                           body,
                                           account_header=None):
        """Does a POST request to /v1/replies/confirmed.

        Mark a reply message as confirmed so it is no longer returned in check
        replies requests.
        The confirm replies endpoint is intended to be used in conjunction
        with the check replies endpoint
        to allow for robust processing of reply messages. Once one or more
        reply messages have been processed
        they can then be confirmed using the confirm replies endpoint so they
        are no longer returned in
        subsequent check replies requests.
        The confirm replies endpoint takes a list of reply IDs as follows:
        ```json
        {
            "reply_ids": [
                "011dcead-6988-4ad6-a1c7-6b6c68ea628d",
                "3487b3fa-6586-4979-a233-2d1b095c7718",
                "ba28e94b-c83d-4759-98e7-ff9c7edb87a1"
            ]
        }
        ```
        Up to 100 replies can be confirmed in a single confirm replies
        request.

        Args:
            body (ConfirmRepliesAsReceivedRequest): TODO: type description
                here. Example: 
            account_header:  TODO: type description
                here. Example:

        Returns:
            mixed: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_confirm_replies_as_received called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_confirm_replies_as_received.')
            url = '/v1/replies/confirmed'
            _query_builder = Configuration.base_uri
            _query_builder += url
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_confirm_replies_as_received.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }

            self.add_account_header(_headers, account_header)

            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_confirm_replies_as_received.')
            json_body = APIHelper.json_serialize(body)
            _request = self.http_client.post(_query_url, headers=_headers, parameters=json_body)
            self.apply_authentication(_request, url, json_body)
            _context = self.execute_request(_request, name='create_confirm_replies_as_received')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for create_confirm_replies_as_received.')
            if _context.response.status_code == 400:
                raise APIException('', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info=True)
            raise

    def get_check_replies(self, account_header=None):
        """Does a GET request to /v1/replies.

        Check for any replies that have been received.
        Replies are messages that have been sent from a handset in response to
        a message sent by an
        application or messages that have been sent from a handset to a
        inbound number associated with
        an account, known as a dedicated inbound number (contact
        <support@messagemedia.com> for more
        information on dedicated inbound numbers).
        Each request to the check replies endpoint will return any replies
        received that have not yet
        been confirmed using the confirm replies endpoint. A response from the
        check replies endpoint
        will have the following structure:
        ```json
        {
            "replies": [
                {
                    "metadata": {
                        "key1": "value1",
                        "key2": "value2"
                    },
                    "message_id": "877c19ef-fa2e-4cec-827a-e1df9b5509f7",
                    "reply_id": "a175e797-2b54-468b-9850-41a3eab32f74",
                    "date_received": "2016-12-07T08:43:00.850Z",
                    "callback_url": "https://my.callback.url.com",
                    "destination_number": "+61491570156",
                    "source_number": "+61491570157",
                    "vendor_account_id": {
                        "vendor_id": "MessageMedia",
                        "account_id": "MyAccount"
                    },
                    "content": "My first reply!"
                },
                {
                    "metadata": {
                        "key1": "value1",
                        "key2": "value2"
                    },
                    "message_id": "8f2f5927-2e16-4f1c-bd43-47dbe2a77ae4",
                    "reply_id": "3d8d53d8-01d3-45dd-8cfa-4dfc81600f7f",
                    "date_received": "2016-12-07T08:43:00.850Z",
                    "callback_url": "https://my.callback.url.com",
                    "destination_number": "+61491570157",
                    "source_number": "+61491570158",
                    "vendor_account_id": {
                        "vendor_id": "MessageMedia",
                        "account_id": "MyAccount"
                    },
                    "content": "My second reply!"
                }
            ]
        }
        ```
        Each reply will contain details about the reply message, as well as
        details of the message the reply was sent
        in response to, including any metadata specified. Every reply will
        have a reply ID to be used with the
        confirm replies endpoint.
        *Note: The source number and destination number properties in a reply
        are the inverse of those
        specified in the message the reply is in response to. The source
        number of the reply message is the
        same as the destination number of the original message, and the
        destination number of the reply
        message is the same as the source number of the original message. If a
        source number
        wasn't specified in the original message, then the destination number
        property will not be present
        in the reply message.*
        Subsequent requests to the check replies endpoint will return the same
        reply messages and a maximum
        of 100 replies will be returned in each request. Applications should
        use the confirm replies endpoint
        in the following pattern so that replies that have been processed are
        no longer returned in
        subsequent check replies requests.
        1. Call check replies endpoint
        2. Process each reply message
        3. Confirm all processed reply messages using the confirm replies
        endpoint
        *Note: It is recommended to use the Webhooks feature to receive reply
        messages rather than polling
        the check replies endpoint.*

        Args:
            account_header:  TODO: type description
                here. Example:

        Returns:
            CheckRepliesResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_check_replies called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_check_replies.')
            url = '/v1/replies'
            _query_builder = Configuration.base_uri
            _query_builder += url
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_check_replies.')
            _headers = {
                'accept': 'application/json'
            }

            self.add_account_header(_headers, account_header)

            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_check_replies.')
            _request = self.http_client.get(_query_url, headers=_headers)
            self.apply_authentication(_request, url)
            _context = self.execute_request(_request, name='get_check_replies')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CheckRepliesResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info=True)
            raise
