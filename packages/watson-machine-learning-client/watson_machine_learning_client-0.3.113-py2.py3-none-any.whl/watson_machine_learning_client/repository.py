################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


from repository_v3.mlrepositoryclient import MLRepositoryClient
from repository_v3.mlrepositoryartifact import MLRepositoryArtifact
from repository_v3.mlrepository import MetaProps
import requests
import json
from .utils import get_headers
from .metanames import ModelDefinitionMetaNames, ModelMetaNames
import os
from .training import Training


class Repository:
    """
    Manage your models using Watson Machine Learning Repository.
    """

    def __init__(self, wml_credentials, wml_token, ml_repository_client, instance_details):
        self._wml_credentials = wml_credentials
        self._wml_token = wml_token
        self._ml_repository_client = ml_repository_client
        self._instance_details = instance_details
        self.DefinitionMetaNames = ModelDefinitionMetaNames()
        self.ModelMetaNames = ModelMetaNames()

    def store_definition(self, training_definition, meta_props):
        """
           Store training definition into Watson Machine Learning repository on IBM Cloud.

           Args:
               training_definition (str):  path to zipped model_definition.

               meta_props (dict): meta data of the training definition. To see available meta names use:
               >>> client.repository.DefinitionMetaNames.show()


           Returns:
               definition url (str) - stored training definition url.

           A way you might use me is

           >>> metadata = {
           >>>  client.repository.DefinitionMetaNames.NAME: "my_training_definition",
           >>>  client.repository.DefinitionMetaNames.DESCRIPTION: "my_description",
           >>>  client.repository.DefinitionMetaNames.AUTHOR_NAME: "John Smith",
           >>>  client.repository.DefinitionMetaNames.AUTHOR_EMAIL: "js@js.com",
           >>>  client.repository.DefinitionMetaNames.FRAMEWORK_NAME: "tensorflow",
           >>>  client.repository.DefinitionMetaNames.FRAMEWORK_VERSION: "1.2",
           >>>  client.repository.DefinitionMetaNames.RUNTIME_NAME: "python",
           >>>  client.repository.DefinitionMetaNames.RUNTIME_VERSION: "3.5",
           >>> }
           >>> published_model_definition = client.repository.store_definition(training_definition_filepath, meta_props=metadata)
        """

        # TODO to be replaced with repository client

        training_definition_metadata_required = {
                               "name": meta_props[self.DefinitionMetaNames.NAME],
                               "description": meta_props[self.DefinitionMetaNames.DESCRIPTION],
                               "framework": {
                                   "name": meta_props[self.DefinitionMetaNames.FRAMEWORK_NAME],
                                   "version": meta_props[self.DefinitionMetaNames.FRAMEWORK_VERSION],
                                   "runtimes": [{
                                        "name": meta_props[self.DefinitionMetaNames.RUNTIME_NAME],
                                        "version": meta_props[self.DefinitionMetaNames.RUNTIME_VERSION]
                                    }]
                                }
        }

        if self.DefinitionMetaNames.TRAINING_DATA_REFERENCE in meta_props.keys():
            training_data_reference = {
                "training_data_reference": meta_props[self.DefinitionMetaNames.TRAINING_DATA_REFERENCE],
                "author": {
                    "name": meta_props[self.DefinitionMetaNames.AUTHOR_NAME],
                    "email": meta_props[self.DefinitionMetaNames.AUTHOR_EMAIL]
                }
            }
            training_definition_metadata = {**training_definition_metadata_required, **training_data_reference}
        else:
            training_definition_metadata = training_definition_metadata_required

        experiments_endpoint = '{}/v3/ml_assets/experiments'.format(self._wml_credentials['url'])
        response_experiment_post = requests.post(experiments_endpoint, json=training_definition_metadata,
                                                 headers=get_headers(self._wml_token))

        if response_experiment_post.status_code == 201:
            experiment_version_content_url = response_experiment_post.json().get('entity').get(
                'experiment_version').get('content_url')
            # save model definition content
            put_header = {'Authorization': "Bearer " + self._wml_token, 'Content-Type': 'application/octet-stream'}
            data = open(training_definition, 'rb').read()
            response_experiment_put = requests.put(experiment_version_content_url, data=data, headers=put_header)

            if response_experiment_put.status_code == 200:
                return response_experiment_post.json().get('entity').get('experiment_version').get('url')
            else:
                error_msg = 'Saving model definition content failed.' + '\n' + "Error msg: " + response_experiment_put.text
                print(error_msg)
                return None
        else:
            error_msg = 'Saving model definition metadata failed.' + '\n' + "Error msg: " + response_experiment_post.text
            print(error_msg)
            return None

    def _publish_from_object(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store model from object in memory into Watson Machine Learning repository on Cloud
        """
        try:
            ml_repository_client = MLRepositoryClient(self._wml_credentials['url'])
            ml_repository_client.authorize(self._wml_credentials['username'], self._wml_credentials['password'])

            if meta_props is None:
                meta_data = MetaProps({})
            else:
                meta_data = MetaProps(meta_props)

            if 'pyspark.ml.pipeline.PipelineModel' in str(type(model)):
                model_artifact = MLRepositoryArtifact(model, name=name, meta_props=meta_data, training_data=training_data)
            else:
                model_artifact = MLRepositoryArtifact(model, name=name, meta_props=meta_data, training_data=training_data, training_target=training_target)

            saved_model = ml_repository_client.models.save(model_artifact)
        except:
            error_msg = "Publishing model failed."
            print(error_msg)
            raise
        else:
            return saved_model

    def _publish_from_training(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store trained model from object storage into Watson Machine Learning repository on IBM Cloud
        """
        ml_asset_endpoint = '{}/v3/models/{}/ml_asset'.format(self._wml_credentials['url'], model)
        models_obj = Training(self._wml_credentials, self._wml_token, self._instance_details)
        details = models_obj.get_details(model)

        if details is not None:
            base_payload = {self.DefinitionMetaNames.NAME: name}

            if meta_props is None:
                payload = base_payload
            else:
                payload = dict(base_payload, **meta_props)

            response_model_put = requests.put(ml_asset_endpoint, json=payload, headers=get_headers(self._wml_token))

            if response_model_put.status_code == 202:
                saved_model_details = json.loads(response_model_put.text)
                model_guid = saved_model_details['entity']['ml_asset_guid']
                content_status_endpoint = self._wml_credentials['url'] + '/v3/ml_assets/models/' + str(model_guid)
                response_content_status_get = requests.get(content_status_endpoint, headers=get_headers(self._wml_token))

                if response_content_status_get.status_code == 200:
                    state = json.loads(response_content_status_get.text)['entity']['model_version']['content_status']['state']

                    while ('persisted' not in state) and ('persisting_failed' not in state):
                        response_content_status_get = requests.get(content_status_endpoint, headers=get_headers(self._wml_token))
                        state = json.loads(response_content_status_get.text)['entity']['model_version']['content_status']['state']

                    if 'persisted' in state:
                        return saved_model_details
                    else:
                        error_msg = 'Saving trained model in repository failed.' + '\n' + "Error msg: " + response_content_status_get.text
                        print(error_msg)
                        return None

                else:
                    error_msg = 'Unable to check saved model content status.' + '\n' + "Error msg: " + response_content_status_get.text
                    print(error_msg)
                    return None
            else:
                error_msg = 'Saving trained model in repository failed.' + '\n' + "Error msg: " + response_model_put.text
                print(error_msg)
                return None

    def _publish_from_file(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store saved model into Watson Machine Learning repository on IBM Cloud
        """
        import tarfile
        import zipfile

        model_filepath = model
        if os.path.isdir(model):
            # TODO currently tar.gz is required for tensorflow - the same ext should be supported for all frameworks
            if os.path.basename(model) == '':
                model = os.path.dirname(model)
            filename = os.path.basename(model) + '.tar.gz'
            current_dir = os.getcwd()
            os.chdir(model)
            target_path = os.path.dirname(model)

            with tarfile.open(os.path.join('..', filename), mode='w:gz') as tar:
                tar.add('.')

            os.chdir(current_dir)
            model_filepath = os.path.join(target_path, filename)

        if tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath):
            try:
                ml_repository_client = MLRepositoryClient(self._wml_credentials['url'])
                ml_repository_client.authorize(self._wml_credentials['username'], self._wml_credentials['password'])

                if meta_props is None:
                    error_msg = "meta_props value have to be specified"
                    print(error_msg)
                    raise ValueError(error_msg)
                else:
                    meta_data = MetaProps(meta_props)

                model_artifact = MLRepositoryArtifact(model_filepath, name=name, meta_props=meta_data)
                saved_model = ml_repository_client.models.save(model_artifact)
            except:
                error_msg = "Publishing model failed."
                print(error_msg)
                raise
            else:
                return saved_model
        else:
            error_msg = 'Saving trained model in repository failed.\n{} file does not have valid format'.format(model_filepath)
            print(error_msg)
            return None

    def publish(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        This method is deprecated. Please use store_model() instead.
        """
        print("Method is deprecated. Use store_model() instead.")
        return self.store_model(model, name, meta_props=meta_props, training_data=training_data, training_target=training_target)

    def store_model(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store trained model into Watson Machine Learning repository on Cloud.

        Args:
            model (object/str):  The train model object (e.g: spark PipelineModel), or path to saved model, or trained model guid.

            name (str):  The name for model to use.

            meta_props (dict): meta data of the training definition. To see available meta names use:
            >>> client.repository.ModelMetaNames.show()

            training_data (spark dataframe, pandas dataframe, numpy.ndarray or list):  Spark DataFrame supported for spark models. Pandas dataframe, numpy.ndarray or list supported for scikit-learn models.

            training_target (array): array with labels required for scikit-learn models.

        Returns:
            stored_model (object/str) - the stored model artifact or url to stored model.

        A way you might use me with spark model is

        >>> published_model = client.repository.store_model(local_model, name, meta_props={"authorName":"John Smith"}, training_data=None)
        >>> print published_model.uid
           0123-0123-0123

         A way you might use me with scikit-learn model is

        >>> published_model = client.repository.store_model(local_model, name, meta_props=None, training_data=None, training_target=None)
        >>> print published_model.uid
           0123-0123-0123

        """

        if not isinstance(model, str):
            saved_model = self._publish_from_object(model=model, name=name, meta_props=meta_props, training_data=training_data, training_target=training_target)
        else:
            if os.path.isfile(model) or os.path.isdir(model):
                saved_model = self._publish_from_file(model=model, name=name, meta_props=meta_props, training_data=training_data, training_target=training_target)
            else:
                saved_model = self._publish_from_training(model=model, name=name, meta_props=meta_props, training_data=training_data, training_target=training_target)

        return saved_model

    def load(self, artifact_uid):
        """
        Load model from repository to object in local environment.

        Args:
            artifact_uid (string):  Published model UID.

        Returns:
            model (object) - trained model.

        A way you might use me is

        >>> model = client.repository.load(model_uid)
        """

        try:
            ml_repository_client = MLRepositoryClient(self._wml_credentials['url'])
            ml_repository_client.authorize(self._wml_credentials['username'], self._wml_credentials['password'])
            loaded_model = ml_repository_client.models.get(artifact_uid)
            loaded_model = loaded_model.model_instance()
        except:
            error_msg = "Loading model failed."
            print(error_msg)
            raise
        else:
            return loaded_model

    def delete(self, artifact_uid):
        """
          Delete model from repository.

          Args:
              artifact_uid (string):  Published model UID.

          Returns:
              status (str) - deletion status.

          A way you might use me is
          >>> client.repository.delete(model_uid)
        """
        try:
            deleted = self._ml_repository_client.models.remove(artifact_uid)
            return deleted
        except:
            error_msg = "Model deletion failed."
            print(error_msg)
            raise

    def get_details(self, artifact_uid=None):
        """
           Get metadata of model or models. If model uid is not specified returns all models metadata.

           Args:
               artifact_uid (str):  Published model UID (optional).

           Returns:
               model details (dict) - stored model(s) metadata.

           A way you might use me is

           >>> model_details = client.repository.get_details(model_uid)
           >>> models_details = client.repository.get_details()
           """
        if artifact_uid is None:
            response_get = requests.get(
                self._instance_details.
                get('entity').
                get('published_models').
                get('url'),
                headers=get_headers(self._wml_token))
        else:
            response_get = requests.get(
                self._instance_details.
                get('entity').
                get('published_models').
                get('url') + "/" + artifact_uid,
                headers=get_headers(self._wml_token))

        if response_get.status_code == 200:
            return json.loads(response_get.text)
        else:
            error_msg = 'Getting model details failed.' + '\n' + "Error msg: " + response_get.text
            print(error_msg)
            return None

    def list(self):
        """
           List stored models.

           A way you might use me is

           >>> client.repository.list()
        """
        from tabulate import tabulate

        details = self.get_details()
        resources = details['resources']
        values = [(m['metadata']['guid'], m['entity']['name'],
                   m['entity']['model_type']) for m in resources]
        table = tabulate([["GUID", "NAME", "FRAMEWORK"]] + values)
        print(table)
