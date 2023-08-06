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
import time
import tqdm
from .metanames import TrainingConfigurationMetaNames
import sys


class Training:
    """
       Train new models.
    """

    def __init__(self, wml_credentials, wml_token, instance_details):
        self._wml_credentials = wml_credentials
        self._wml_token = wml_token
        self._instance_details = instance_details
        self._base_models_url = wml_credentials['url'] + "/v3/models"
        self.ConfigurationMetaNames = TrainingConfigurationMetaNames()


    # def get_frameworks(self):
    #     """
    #        Get list of supported frameworks.
    #
    #        Returns:
    #            json - supported frameworks for training.
    #
    #        A way you might use me is
    #
    #        >>> model_details = client.training.get_frameworks()
    #     """
    #
    #     response_get = requests.get(self._base_models_url + "/frameworks", headers=get_headers(self._wml_token))
    #
    #     if response_get.status_code == 200:
    #         return json.loads(response_get.text)
    #     else:
    #         error_msg = 'Getting supported frameworks failed.' + '\n' + "Error msg: " + response_get.text
    #         print(error_msg)
    #         return None

    def get_status(self, training_run_uid):
        """
              Get training status.

              Returns:
                  status (dict) - training run status.

              A way you might use me is

              >>> training_status = client.training.get_status()
        """

        details = self.get_details(training_run_uid)

        if details is not None:
            return details['entity']['status']
        else:
            error_msg = 'Getting trained model status failed. Unable to get model details.'
            print(error_msg)
            return None

    def get_details(self, training_run_uid=None):
        """
              Get trained model details.

              Args:
                  trained_run_uid (str): ID of trained model (optional, if not provided all runs details are returned).

              Returns:
                  details (dict) - training run(s) details.

              A way you might use me is

              >>> trained_model_details = client.training.get_details(training_run_uid)
              >>> trained_models_details = client.training.get_details()
        """

        if training_run_uid is None:
            response_get = requests.get(self._base_models_url, headers=get_headers(self._wml_token))

            if response_get.status_code == 200:
                return json.loads(response_get.text)
            else:
                error_msg = 'Getting trained models list failed.' + '\n' + "Error msg: " + response_get.text
                print(error_msg)
                return None
        else:
            get_details_endpoint = '{}/v3/models/'.format(self._wml_credentials['url']) + training_run_uid
            model_training_details = requests.get(get_details_endpoint, headers=get_headers(self._wml_token))

            if model_training_details.status_code == 200:
                return json.loads(model_training_details.text)
            else:
                error_msg = 'Getting trained model details failed.' + '\n' + "Error msg: " + model_training_details.text
                print(error_msg)
            return None

    def cancel(self, training_run_uid):
        """
              Cancel model training.

              Args:
                  training_run_uid (str): ID of trained model.

              Returns:
                  status (bool) - True if operation succeeded.

              A way you might use me is

              >>> client.training.cancel(training_run_uid)
        """

        patch_endpoint = self._base_models_url + '/' + str(training_run_uid)
        patch_payload = [
            {
                "op": "replace",
                "path": "/status/state",
                "value": "canceled"
            }
        ]

        response_patch = requests.patch(patch_endpoint, json=patch_payload, headers=get_headers(self._wml_token))

        if response_patch.status_code == 204:
            return True
        else:
            error_msg = 'Cancelling model training failed.' + '\n' + "Error msg: " + response_patch.text
            print(error_msg)
            return False

    def run(self, definition_location, meta_props, asynchronous=True):
        """
           Train new model.
            Args:
               definition_location_url (str): url to saved model_definition/pipeline.

               meta_props (dict): meta data of the training configuration. To see available meta names use:
               >>> client.training.ConfigurationMetaNames.show()

               asynchronous (bool): Default True means that training job is submitted and progress can be checked later.
               False - method will wait till job completion and print training stats.

           Returns:
               training_run_uid (str) - ID of model being trained.

           A way you might use me is

           >>> metadata = {
           >>>  client.training.ConfigurationMetaNames.NAME: "Hand-written Digit Recognition",
           >>>  client.training.ConfigurationMetaNames.AUTHOR_NAME: "John Smith",
           >>>  client.training.ConfigurationMetaNames.DESCRIPTION: "Hand-written Digit Recognition training",
           >>>  client.training.ConfigurationMetaNames.FRAMEWORK_NAME: "tensorflow",
           >>>  client.training.ConfigurationMetaNames.FRAMEWORK_VERSION: "1.2-py3",
           >>>  client.training.ConfigurationMetaNames.EXECUTION_COMMAND: "python3 convolutional_network.py --trainImagesFile ${DATA_DIR}/train-images-idx3-ubyte.gz --trainLabelsFile ${DATA_DIR}/train-labels-idx1-ubyte.gz --testImagesFile ${DATA_DIR}/t10k-images-idx3-ubyte.gz --testLabelsFile ${DATA_DIR}/t10k-labels-idx1-ubyte.gz --learningRate 0.001 --trainingIters 1000",
           >>>  client.training.ConfigurationMetaNames.EXECUTION_RESOURCE_SIZE: "small",
           >>>  client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCE: [
           >>>      {
           >>>          "connection": {
           >>>              "auth_url": "https://s3-api.us-geo.objectstorage.service.networklayer.com",
           >>>              "userId": "***",
           >>>              "password": "***"
           >>>          },
           >>>          "source": {
           >>>              "container": "wml-dev",
           >>>              "type": "s3_datastore"
           >>>          }
           >>>      }
           >>>  ],
           >>> client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE: {
           >>>          "connection": {
           >>>              "auth_url": "https://s3-api.us-geo.objectstorage.service.networklayer.com",
           >>>              "userId": "***",
           >>>              "password": "***"
           >>>          },
           >>>          "source": {
           >>>              "container": "wml-dev-results",
           >>>              "type": "s3_datastore"
           >>>          }
           >>>      },
           >>> }
           >>> trained_model_details = client.training.run(definition_location, meta_props=metadata)
        """

        # TODO it should 1:1 url bug opened -> it should take direct link to definition or definition_version
        definition_location_tmp = str(definition_location).replace(self._wml_credentials['url'], '') + '/content'

        training_configuration_metadata = {
            "model_definition": {
                "framework": {
                    "name": meta_props[self.ConfigurationMetaNames.FRAMEWORK_NAME],
                    "version": meta_props[self.ConfigurationMetaNames.FRAMEWORK_VERSION]
                },
                "name": meta_props[self.ConfigurationMetaNames.NAME],
                "author": meta_props[self.ConfigurationMetaNames.AUTHOR_NAME],
                "description": meta_props[self.ConfigurationMetaNames.DESCRIPTION],
                "definition_location": definition_location_tmp,
                "execution": {
                    "command": meta_props[self.ConfigurationMetaNames.EXECUTION_COMMAND],
                    "resourceType": meta_props[self.ConfigurationMetaNames.EXECUTION_RESOURCE_SIZE]
                }
            },
            "training_data": meta_props[self.ConfigurationMetaNames.TRAINING_DATA_REFERENCE],
            "training_results": meta_props[self.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE]
        }

        train_endpoint = '{}/v3/models'.format(self._wml_credentials['url'])
        response_train_post = requests.post(train_endpoint, json=training_configuration_metadata,
                                            headers=get_headers(self._wml_token))
        trained_model_guid = None

        if response_train_post.status_code == 202:
            trained_model_guid = response_train_post.json().get('metadata').get('guid')

            if asynchronous is True:
                return trained_model_guid
            else:
                models_obj = Training(self._wml_credentials, self._wml_token, self._instance_details)
                start = time.time()
                status = models_obj.get_status(trained_model_guid)
                state = status['state']

                print("Training started ...")

                # TODO add iterations progress based on details
                while ('completed' not in state) and ('error' not in state) and ('canceled' not in state):
                    elapsed_time = time.time() - start
                    print("Elapsed time: " + str(elapsed_time) + " -> training state: " + str(state))
                    sys.stdout.flush()
                    status = models_obj.get_status(trained_model_guid)
                    state = status['state']
                    for i in tqdm.tqdm(range(10)):
                        time.sleep(1)

                print('Training DONE.')
                return trained_model_guid
        else:
            if trained_model_guid is not None:
                error_msg = 'Training ' + trained_model_guid + ' failed.' + '\nError msg: ' + response_train_post.text
            else:
                error_msg = 'Training failed.' + '\nError msg: ' + response_train_post.text
            print(error_msg)
            return None

    def list(self):
        """
           List training runs.

           A way you might use me is

           >>> client.training.list()
        """
        from tabulate import tabulate

        details = self.get_details()
        resources = details['resources']
        values = [(m["metadata"]['guid'], m["entity"]['status']['state'], m['metadata']['created_at'],
                   m['entity']['model_definition']['framework']['name']) for m in resources]
        table = tabulate([["GUID (training)", "STATE", "CREATED", "FRAMEWORK"]] + values)
        print(table)

    def delete(self, training_run_uid):
        """
            Delete trained model.

            Args:
                training_run_uid (str) - ID of trained model.

            Returns:
                status (bool) - True if operation succeeded.

            A way you might use me is

            >>> trained_models_list = client.training.delete(training_run_uid)
        """
        response_delete = requests.delete(self._base_models_url + '/' + str(training_run_uid),
                                          headers=get_headers(self._wml_token))

        if response_delete.status_code != 204:
            error_msg = 'Trained model deletion failed.' + '\n' + "Error msg: " + response_delete.text
            print(error_msg)
            return False
        else:
            return True

    def monitor(self, training_run_uid):
        """
            Monitor training log file (prints log content to console).

            Args:
                training_run_uid (str) - ID of trained model.

            A way you might use me is

            >>> client.training.monitor(training_run_uid)
        """
        from lomond import WebSocket

        monitor_endpoint = self._wml_credentials['url'].replace('https',
                                                                'wss') + "/v3/models/" + training_run_uid + "/monitor"
        websocket = WebSocket(monitor_endpoint)
        websocket.add_header(bytes("Authorization", "utf-8"), bytes("bearer " + self._wml_token, "utf-8"))

        print("Log monitor started.")

        for event in websocket:
            if event.name == 'text':
                status = json.loads(event.text)['status']
                if 'message' in status:
                    print(status["message"])

        print("Log monitor done.")
