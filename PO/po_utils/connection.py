from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import BadRequest, NotFound, Forbidden
from google.auth.exceptions import DefaultCredentialsError, GoogleAuthError
import os
from jproperties import Properties
key_path = r"PO\credential\sa-edr-phm-ai-im-tableau@edr-phm-ai-im-pr-cah.json"
def bq_connection(general_logger,error_logger): 
    '''
    this function will be used to connect to gcp bigquery
    '''
    try:
        credentials = service_account.Credentials.from_service_account_file(key_path)
        project_id = 'edr-phm-ai-im-pr-cah'
        client = bigquery.Client(credentials= credentials,project=project_id)
        general_logger.info("sucessfully connected")
        return client
    except FileNotFoundError:
        error_logger.error(f"Error : JSON key file not found at the specified path : {key_path}")
    except DefaultCredentialsError:
        error_logger.error("Error default credential could not be found, ensure the json key path is correct")
    except GoogleAuthError as e:
        error_logger.error(f"Authentication failed {str(e)}")
    except Exception as e:
        error_logger.error(f"An unexpected error occured : {str(e)}")
