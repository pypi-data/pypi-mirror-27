################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################
import sys
from os.path import join as path_join
from pip import get_installed_distributions

for x in get_installed_distributions():
    if (x.project_name == 'watson-machine-learning-client'):
        sys.path.insert(1, path_join(x.location, 'watson_machine_learning_client', 'libs'))

from repository_v3.mlrepositoryclient import MLRepositoryClient
from .training import Training
from .repository import Repository
from .instance import ServiceInstance
from .deployments import Deployments
from .utils import get_ml_token

"""
.. module:: WatsonMachineLearningAPIClient
   :platform: Unix, Windows
   :synopsis: Watson Machine Learning API Client.

.. moduleauthor:: IBM
"""


class WatsonMachineLearningAPIClient:

    def __init__(self, wml_credentials):
        self.wml_credentials = wml_credentials
        self.wml_token, self.ml_repository_client = self._connect()
        self.service_instance = ServiceInstance(self.wml_credentials, self.wml_token)
        self.instance_details = self.service_instance.get_details()
        self.repository = Repository(self.wml_credentials, self.wml_token, self.ml_repository_client,
                                     self.instance_details)
        self.deployments = Deployments(self.wml_credentials, self.wml_token, self.instance_details)
        self.training = Training(self.wml_credentials, self.wml_token, self.instance_details)

    def _connect(self):
        if self.wml_credentials is not None:
            ml_repository_client = MLRepositoryClient(self.wml_credentials['url'])

            ml_repository_client.authorize(self.wml_credentials['username'],
                                           self.wml_credentials['password'])

            wml_token = get_ml_token(self.wml_credentials)
            return wml_token, ml_repository_client
