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


class Deployments:
    """
        Deploy and score published models.
    """
    def __init__(self, wml_credentials, wml_token, instance_details):
        self.wml_credentials = wml_credentials
        self.wml_token = wml_token
        self.instance_details = instance_details

    def get_details(self, deployment_url=None):
        """
           Get information about your deployment(s).

           Args:
               deployment_url (str):  Deployment URL (optional).

           Returns:
               deployment_details (dict) - metadata of deployment(s).

           A way you might use me is

            >>> deployment_details = client.deployments.get_details(deployment_url)
            >>> deployments_details = client.deployments.get_details()
        """
        if deployment_url is None:
            response_get = requests.get(
                self.instance_details.
                get('entity').
                get('deployments').
                get('url'),
                headers=get_headers(self.wml_token))
        else:
            response_get = requests.get(
                deployment_url,
                headers=get_headers(self.wml_token))

        if response_get.status_code == 200:
            return json.loads(response_get.text)
        else:
            error_msg = 'Getting deployment details failed.' + '\n' + "Error msg: " + response_get.text
            print(error_msg)
            return None

    def create(self, model_uid, name, description='Model deployment'):
        """
            Create model deployment (online).

            Args:
                model_uid (string):  Published model UID.

                name (string): Deployment name.

                description (string): Deployment description.

            Returns:
                deployment (dict) - details of created deployment.

            A way you might use me is

             >>> deployment = client.deployments.create(model_uid, "Deployment X", "Online deployment of XYZ model.")
         """
        response_online = requests.post(
            self.instance_details.
            get('entity').
            get('published_models').
            get('url') + "/" + model_uid + "/" + "deployments",
            json={'name': name, 'description': description, 'type': 'online'},
            headers=get_headers(self.wml_token))
        if response_online.status_code == 201:
            return json.loads(response_online.text)
        else:
            error_msg = 'Deployment creation for ' + str(model_uid) + ' failed.' + '\nError msg: ' + response_online.text
            print(error_msg)
            return None

    @staticmethod
    def get_scoring_url(deployment):
        """
            Get scoring_url from deployment details.

            Args:
                deployment (dict):  Created deployment details.

            Returns:
                scoring_url (string) - scoring endpoint URL that is used for making scoring requests.

            A way you might use me is

             >>> scoring_endpoint = client.deployments.get_scoring_url(deployment)
        """
        try:
            scoring_url = deployment.get('entity').get('scoring_url')
        except:
            error_msg = "Getting scoring url failed."
            print(error_msg)
            raise
        else:
            return scoring_url

    @staticmethod
    def get_deployment_url(deployment_details):
        """
            Get deployment_url from deployment details.

            Args:
               deployment_details (dict):  Created deployment details.

            Returns:
               deployment_url (str) - deployment URL that is used to manage the deployment

               A way you might use me is

            >>> scoring_endpoint = client.deployments.get_deployment_url(deployment)
        """
        try:
            deployment_url = deployment_details.get('metadata').get('url')
        except:
            error_msg = "Getting deployment url failed."
            print(error_msg)
            raise
        else:
            return deployment_url

    def delete(self, deployment_url):
        """
            Delete model deployment.

            Args:
                deployment_url (str):  Deployment URL.

            Returns:
                response (bool):  status of delete action.

            A way you might use me is

            >>> client.deployments.delete(deployment_url)
        """
        response_delete = requests.delete(
            deployment_url,
            headers=get_headers(self.wml_token))

        if response_delete.status_code != 204:
            error_msg = 'Deployment deletion failed.' + '\n' + "Error msg: " + response_delete.text
            print(error_msg)
            return False
        else:
            return True

    def score(self, scoring_url, payload):
        """
            Make scoring requests against deployed model.

              Args:
                 scoring_url (string):  scoring endpoint URL.

                 payload (dict): records to score.

              Returns:
                  scoring result (dict) - scoring result containing prediction and probability.

              A way you might use me is

              >>> scoring_payload = {"fields": ["GENDER","AGE","MARITAL_STATUS","PROFESSION"],
              "values": [["M",23,"Single","Student"],["M",55,"Single","Executive"]]}
              >>> predictions = client.deployments.score(scoring_url, scoring_payload)
        """
        response_scoring = requests.post(
            scoring_url,
            json=payload,
            headers=get_headers(self.wml_token))
        if response_scoring.status_code == 200:
            return json.loads(response_scoring.text)
        else:
            error_msg = 'Scoring failed.' + '\nError code:' + str(response_scoring.status_code) + "\nError msg: " + response_scoring.text
            print(error_msg)
            return None

