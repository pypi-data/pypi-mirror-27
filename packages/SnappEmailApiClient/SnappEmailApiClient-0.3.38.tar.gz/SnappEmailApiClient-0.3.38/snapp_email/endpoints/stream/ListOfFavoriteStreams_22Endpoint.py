"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ListOfFavoriteStreams_22
from snapp_email.datacontract.utils import export_dict, fill


class ListOfFavoriteStreams_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def update(self, obj, streamId, impersonate_user_id=None, accept_type=None):
        """
        Update list of favorite Streams.
        
        :param obj: Object to be persisted
        :type obj: ListOfFavoriteStreams_22
        
        :param streamId: 
        :type streamId: 
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfFavoriteStreams_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.list.favorite-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.list.favorite-5.18+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id, data=json.dumps(data))
        
        return fill(ListOfFavoriteStreams_22, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
