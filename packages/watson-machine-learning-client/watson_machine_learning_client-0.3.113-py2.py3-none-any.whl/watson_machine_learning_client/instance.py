################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import requests
import json
from .utils import get_headers


class ServiceInstance:
    """
        Connect, get details and check usage of your Watson Machine Learning service instance.
    """
    def __init__(self, wml_credentials, wml_token):
        self.wml_credentials = wml_credentials
        self.wml_token = wml_token

    def get_details(self):
        """
             Get information about our instance of Watson Machine Learning service.

             Returns:
                 instance_details (dict) - metadata of service instance.

             A way you might use me is

             >>> instance_details = client.service_instance.get_details()
        """
        if self.wml_credentials is not None:
            response_get_instance = requests.get(
                self.wml_credentials['url'] + "/v3/wml_instances/"
                + self.wml_credentials['instance_id'],
                headers=get_headers(self.wml_token))

            if response_get_instance.status_code == 200:
                return json.loads(response_get_instance.text)
            else:

                error_msg = "Getting instance details failed." + '\n' + \
                            'Error msg: ' + response_get_instance.text
                print(error_msg)
                return None
        else:
            error_msg = "Unable to authorize to Watson Machine Learning service instance. Credentials not found."
            print(error_msg)
            return None
