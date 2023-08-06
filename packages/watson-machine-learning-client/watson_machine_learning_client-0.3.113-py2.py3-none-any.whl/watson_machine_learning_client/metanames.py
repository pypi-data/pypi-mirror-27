################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################
from repository_v3.mlrepository import MetaNames


class TrainingConfigurationMetaNames:

    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = "description"
        self.AUTHOR_NAME = "author_name"
        self.AUTHOR_EMAIL = "author_email"
        self.FRAMEWORK_NAME = "framework_name"
        self.FRAMEWORK_VERSION = "framework_version"
        # TODO needed when bug fixed
        #self.RUNTIME_NAME = "runtime_name"
        #self.RUNTIME_VERSION = "runtime_version"
        self.TRAINING_DATA_REFERENCE = "training_data"
        self.TRAINING_RESULTS_REFERENCE = "training_results"
        self.EXECUTION_COMMAND = "command"
        self.EXECUTION_RESOURCE_SIZE = "resource"

    def show(self):
        return list(self.__dict__.keys())

    # TODO maybe we should add method to show sample values as well


class ModelDefinitionMetaNames:

    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = "description"
        self.AUTHOR_NAME = "author_name"
        self.AUTHOR_EMAIL = "author_email"
        self.FRAMEWORK_NAME = "framework_name"
        self.FRAMEWORK_VERSION = "framework_version"
        self.RUNTIME_NAME = "runtime_name"
        self.RUNTIME_VERSION = "runtime_version"
        self.TRAINING_DATA_REFERENCE = "training_data_reference"
        
    def show(self):
        return list(self.__dict__.keys())

    # TODO maybe we should add method to show sample values as well



class ModelMetaNames:

    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = MetaNames.DESCRIPTION
        self.AUTHOR_NAME = MetaNames.AUTHOR_NAME
        self.AUTHOR_EMAIL = MetaNames.AUTHOR_EMAIL
        self.FRAMEWORK_NAME = MetaNames.FRAMEWORK_NAME
        self.FRAMEWORK_VERSION = MetaNames.FRAMEWORK_VERSION
        self.RUNTIME_NAME = "runtime_name"
        self.RUNTIME_VERSION = "runtime_version"

    def show(self):
        return list(self.__dict__.keys())

    # TODO maybe we should add method to show sample values as well
