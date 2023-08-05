"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ListOfFavoriteStreamsPage_22
from snapp_email.datacontract.utils import export_dict, fill


class ListOfFavoriteStreamsPage_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get(self, streamId, impersonate_user_id=None, accept_type=None):
        """
        Get list of favorite Streams.
        
        :param streamId: 
        :type streamId: 
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfFavoriteStreamsPage_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.list-page.favorite-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.list-page.favorite-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(ListOfFavoriteStreamsPage_22, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
