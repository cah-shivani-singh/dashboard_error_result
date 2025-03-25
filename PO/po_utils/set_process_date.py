import configparser
import sys
sys.path.append(r'PO')
from jproperties import Properties
from po_utils.connection import bq_connection
import json
CONFIG_FILE_PATH = r'PO\config\config.properties'


def set_json_path(json_path,general_logger,error_logger):
    '''
    for each rca model we have different json file, so this will accespt path for each rca and set that path to config file that will be used across all functions
    '''
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set('DEFAULT','rca_json_path',json_path)
    try:
        with open(CONFIG_FILE_PATH,'w') as configfile:
            config.write(configfile)
    except FileNotFoundError as f:
        general_logger.info("Config file not found for more details check error log file")
        error_logger.error(f"Config file not found {f}")

def get_json_path():
    '''
    this function will return json path for respective RCA
    '''
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    json_path = config.get('DEFAULT','rca_json_path')
    return json_path



def get_process_dt(json_path,general_logger,error_logger):
    '''
    this will receive get the curr and prev process date and update the current and prev date with latest process date
    '''
    try:
        with open(f'{json_path}') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        error_logger.error(f"Error occured while read json file {json_path}")
    project_name=data['project_name']
    dataset=data['dataset_id']
    table_id=data['table_id']
    client = bq_connection(general_logger,error_logger)
    configs=Properties()
    try:
        with open(r'PO\config\config.properties','rb') as config_file:
            configs.load(config_file)
    except FileNotFoundError as f:
        general_logger.info("Config file not found for more details check error log file")
        error_logger.error(f"Config file not found {f}")
    general_logger.info('Process Timestamp for previous test: '+configs.get('currentrun_timestamp').data)
    previousrun=configs.get('currentrun_timestamp').data
    recordcheck=True
    query="select max(Process_Date) from `"+project_name+".UNFILLED_UNITS_DEV.DATAPOINT_UNFILL_INVOICE_CDL`"
    try:
        client_query = client.query(query) #it will run on gcp
    except Exception as error:
        error_logger.error(error)
    try:
        processdatetable = client_query.result().to_dataframe()
    except Exception as error:
        error_logger.error(error)
    
    general_logger.info('Current Timestamp: ',str(processdatetable.iloc[0,0]))
    currentrun=str(processdatetable.iloc[0,0])
    
    if currentrun!=previousrun:
        process_date=currentrun  
        configs.__setitem__('previousrun_timestamp',previousrun)
        configs.__setitem__('currentrun_timestamp',process_date)
          
    else:
        recordcheck=False
    try:
        with open(r'PO\config\config.properties','wb') as config_file:
            configs.store(config_file)
    except FileNotFoundError as f:
        general_logger.info("Config file not found for more details check error log file")
        error_logger.error(f"Config file not found {f}")
    if recordcheck:
        total_data_query=f"SELECT * FROM `{project_name}.{dataset}.{table_id}` where date(process_date)=date('{process_date}') limit 10"
        try:
            client_query = client.query(total_data_query)
        except Exception as error:
            error_logger.error(error)

        try:
            total_records = client_query.result().to_dataframe()
        except Exception as error:
            error_logger.error(error)
        if len(total_records)==0:
            return ''
        general_logger.info("Total number of unique records in "+table_id+" for the Process Date("+process_date+ "): "+str(len(total_records)))
        return process_date
    else:
        return ''

#edit timestamp file with latest process timestamp
"""def set_process_date(process_date):
    configs=Properties()
    try:
    
        with open(r'PO\config\config.properties','rb') as config_file:
            configs.load(config_file)
    except FileNotFoundError as f:
        print(f"config file not found {f}")
    prev_run=configs.get('previousrun_timestamp').data
    configs.__setitem__('previousrun_timestamp',prev_run)
    configs.__setitem__('currentrun_timestamp',process_date)
    try:
        with open('PO\config\config.properties','wb') as config_file:
            configs.store(config_file)
    except FileNotFoundError as f:
        print(f"config file not found {f}")
"""


def write_config(general_logger,error_logger):
    '''
    this will write the latest process date in timestamp.properties file
    '''
    try:
      with open(r"PO\config\timestamp.properties","w") as config_file:
            json_path = get_json_path().strip()
            process_date=get_process_dt(json_path,general_logger,error_logger)
            config_file.write(f"process_date={process_date}\n")
            general_logger.info(f"data stored in timestamp.properties {process_date}")
    except FileNotFoundError as f:
        general_logger.info("Config file not found for more details check error log file")
        error_logger.error(f"Config file not found {f}")


#set_json_path(r'PO\\models\\RCA13\\rca13.json')


#write_config()
























