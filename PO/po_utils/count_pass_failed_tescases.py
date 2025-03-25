import configparser
CONFIG_FILE_PATH = 'PO\config\config.properties'
def initialize_count(general_logger,error_logger):
    '''
    it will initalize pass_tc_count, fail_tc_count with 0 value whenever it is called
    '''
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set('DEFAULT','pass_tc_count','0')
    config.set('DEFAULT','failed_tc_count','0')
    config.set('DEFAULT','skip_tc_count','0')
    try:
        with open(CONFIG_FILE_PATH,'w') as configfile:
            config.write(configfile)
    except Exception as e:
        general_logger.info("Error while writing to config file, for more details check error log file")
        error_logger.error(f"Error while writing to config file {e}")
    general_logger.info("Counts initialized sucessfully")

def increment_count(count_type,general_logger,error_logger):
    '''
    it will incement tha count for count type, count type can be pass_tc_count, failed_tc_count
    '''
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    current_count = int(config.get('DEFAULT',count_type))
    config.set('DEFAULT',count_type,str(current_count + 1))
    try:
        with open(CONFIG_FILE_PATH,'w') as configfile:
            config.write(configfile)
    except Exception as e:
        general_logger.info("Error while writing to config file, for more details check error log file")
        error_logger.error(f"Error while writing to config file {e}")
    general_logger.info(f"{count_type} incremented sucessfully")

def get_count(general_logger,error_logger):
    '''
    it will return the count for rach count type in map format
    '''
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    pass_tc_count = config.get('DEFAULT','pass_tc_count')
    failed_tc_count = config.get('DEFAULT','failed_tc_count')
    skip_tc_count = config.get('DEFAULT','skip_tc_count')
    return {
        'pass_tc_count' : pass_tc_count,
        'failed_tc_count' : failed_tc_count,
        'skip_tc_count' : skip_tc_count
    
        }

