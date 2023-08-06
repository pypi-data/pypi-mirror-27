################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


def get_ml_token(watson_ml_creds):
    import requests
    import json
    if 'ml_token' not in watson_ml_creds:
        response = requests.get(watson_ml_creds['url'] + '/v3/identity/token', auth=(watson_ml_creds['username'], watson_ml_creds['password']))
        watson_ml_creds['ml_token'] = json.loads(response.text).get('token')
    return watson_ml_creds['ml_token']


def get_headers(wml_token):
    return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + wml_token}


def get_deployment_url(models_info, uid):
    [endpoint_deployments] = [x.get('entity').get('deployments').get('url') for x in models_info.get('resources') if x.get('metadata').get('guid') == uid]
    return endpoint_deployments
