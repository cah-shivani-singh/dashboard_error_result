import json
import sys
sys.path.append(r'PO')
def read_json_parameter_from_json(json_file_path,testcase_name,general_logger,error_logger):
    '''
    this will read the json file and returns project_name,dataset_id,table_id,sql_queries,top_75
    '''
    try:
        with open(f'{json_file_path}','r') as file:
            data=json.load(file)
            project_name=data['project_name']
            dataset_id=data['dataset_id']
            table_id=data['table_id']
            sql_queries=data["test_cases"].get(f"{testcase_name}").get("sql_query")
            top_75=data["test_cases"].get(f"{testcase_name}").get("top_75")
        return project_name,dataset_id,table_id,sql_queries,top_75
    except FileNotFoundError:
        error_logger.error(f"Error: JSON file not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        error_logger.error("Error  : Failed to decode the JSON file: check the JSON structure.")
        return None
    except Exception as e:
        error_logger.error(f"An unexpected error occured while reading the JSON file : {str(e)}")
        return None
    
def read_description(json_file_path,testcase_no,general_logger,error_logger):
    '''
    this will read json file for each testcase and return the description of each testcase
    '''
    try:
        with open(f'{json_file_path}','r') as file:
            data=json.load(file)
        description = data["test_cases"].get(f"TEST_CASE_{testcase_no}").get("description")
        return description
    except FileNotFoundError:
        error_logger.error(f"Error: JSON file not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        error_logger.error("Error  : Failed to decode the JSON file: check the JSON structure.")
        return None
    except Exception as e:
        error_logger.error(f"An unexpected error occured while reading the JSON file : {str(e)}")
        return None


