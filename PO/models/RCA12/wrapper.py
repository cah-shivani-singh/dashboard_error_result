import logging
import os
import importlib
from datetime import datetime
import sys
sys.path.append(r'PO')
import re
from po_utils.count_pass_failed_tescases import get_count,initialize_count
from po_utils.display_pass_failed_tc import display_pi_chart_for_tc
from po_utils.set_process_date import set_json_path,write_config
import configparser

timestamp = datetime.now().strftime('%Y-%m-%d')
folder_path=rf'PO\models\RCA12\log_info\{timestamp}'
os.makedirs(folder_path,exist_ok=True) 
log_file = f'{folder_path}\execution_log.log'
error_file=f'{folder_path}\execution_log_error.log'

general_logger=logging.getLogger('general_logger')
if not general_logger.hasHandlers():
    general_handler=logging.FileHandler(log_file)
    general_handler.setLevel(logging.INFO)
    general_logger.addHandler(general_handler)
    general_logger.setLevel(logging.INFO)
    general_logger.propagate = False

error_logger=logging.getLogger('error_logger')
if not error_logger.hasHandlers():
    error_handler = logging.FileHandler(error_file)
    error_handler.setLevel(logging.ERROR)
    error_logger.addHandler(error_handler)
    error_logger.setLevel(logging.ERROR)
    error_logger.propagate=False
overall_function_list = [
    'exec_testcase_1',
    'exec_testcase_2',
    'exec_testcase_3',
    'exec_testcase_4',
    'exec_testcase_5',
    'exec_testcase_6',
    'exec_testcase_7',
    'exec_testcase_8',
    'exec_testcase_9',
    'exec_testcase_10',
    'exec_testcase_11',
    'exec_testcase_12',
    'exec_testcase_13',
    'exec_testcase_14',
    'exec_testcase_15',
    'exec_testcase_16',
    'exec_testcase_17',
    'exec_testcase_18',
    'exec_testcase_19'

]
failed_function_list= []

def natural_sort_keys(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)',s)]

def collect_test_functions(function_list):
    test_case_dir = os.path.dirname(__file__) + '/testcases'
    test_case_files = sorted([f for f in os.listdir(test_case_dir) if f.endswith('.py') and f != '__init__.py'],key=natural_sort_keys)
    test_functions = []
    for test_case_file in test_case_files:
        module_name = f'models.RCA12.testcases.{test_case_file[:-3]}'
        try:
            module = importlib.import_module(module_name)
            for function_name in function_list:
                if hasattr(module,function_name):
                    func = getattr(module,function_name)
                    test_functions.append((test_case_file,func))
                    break
        except Exception as e:
            general_logger.info(f"Error while importing module {module_name} for more info check error log file")
            error_logger.error(f"Error importing {module_name} : {e}")
    return test_functions


def run_all_test_cases(function_list):
    test_functions = collect_test_functions(function_list)
    for test_case_file, func in test_functions:
        try :
            print(f"Executing {func.__name__} from {test_case_file}")
            if not func():
                failed_function_list.append(func.__name__)
            general_logger.info('\n')

        except Exception as e:
            general_logger.info(f"Error while running {func.__name__} from {test_case_file} for more info check error log file")
            error_logger.error(f"Error while running {func.__name__} from {test_case_file} : {e}")
            general_logger.info('\n')
    return failed_function_list

def read_failed_tests_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'FAILED_TESTS' in config:
        failed_tests = config['FAILED_TESTS']['tests'].split(',')
        return failed_tests,config
    return [],config

def write_failed_test_to_config(failed_tests,config,config_file):
    config['FAILED_TESTS'] = {'tests': ','.join(failed_tests)}
    with open(config_file,'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    initialize_count(general_logger,error_logger)
    #set_json_path(r'PO\\models\\RCA12\\rca12.json')
    write_config()

    """    failed_tests,config = read_failed_tests_from_config(r'PO\config\config.properties')
    new_failed_tests = run_all_test_cases(overall_function_list)
    write_failed_test_to_config(new_failed_tests,config,r'PO\config\config.properties') 
    failed_tc = read_failed_tests_from_config(r'PO\config\config.properties')[0]"""
    run_all_test_cases(overall_function_list)

    

    no_of_tc = len(overall_function_list)
    dict = get_count(general_logger,error_logger)
    no_of_pass_tc = int(dict['pass_tc_count'].strip())
    no_of_failed_tc = no_of_tc - no_of_pass_tc
    if no_of_failed_tc < 0:
        no_of_failed_tc=0
    general_logger.info(f"Total Number of TestCases : {no_of_tc}")
    general_logger.info(f"Total Number of pass TestCases : {no_of_pass_tc}")
    general_logger.info(f"Total Number of failed TestCases : {no_of_failed_tc}")
    display_pi_chart_for_tc(19, 17,2,rf'{folder_path}')


