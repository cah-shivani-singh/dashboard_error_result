import logging
import os
import importlib
from datetime import datetime
import sys
sys.path.append(r'PO')
import re
from po_utils import get_count,initialize_count,display_pi_chart_for_tc

timestamp = datetime.now().strftime('%Y-%m-%d')
folder_path=rf'PO\models\RCA3b\log_info\{timestamp}'
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
function_list = [
    'exec_testcase_1',
    'exec_testcase_2',
    'exec_testcase_3',
    'exec_testcase_4',
    'exec_testcase_5',
    'exec_testcase_6',
    'exec_testcase_7',
    'exec_testcase_8',
    'exec_testcase_9',
    'exec_testcase_10'
]

def natural_sort_keys(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)',s)]

def collect_test_functions():
    test_case_dir = os.path.dirname(__file__) + '/testcases'
    test_case_files = sorted([f for f in os.listdir(test_case_dir) if f.endswith('.py') and f != '__init__.py'],key=natural_sort_keys)
    test_functions = []
    for test_case_file in test_case_files:
        module_name = f'models.RCA3b.testcases.{test_case_file[:-3]}'
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

def run_all_test_cases():
    test_functions = collect_test_functions()
    for test_case_file, func in test_functions:
        try :
            print(f"Executing {func.__name__} from {test_case_file}")
            func()
            general_logger.info('\n')
        except Exception as e:
            general_logger.info(f"Error while running {func.__name__} from {test_case_file} for more info check error log file")
            error_logger.error(f"Error while running {func.__name__} from {test_case_file} : {e}")
            general_logger.info('\n')
if __name__ == "__main__":
    initialize_count()
    run_all_test_cases()
    no_of_tc = len(function_list)
    dict = get_count()
    no_of_pass_tc = int(dict['pass_tc_count'].strip())
    no_of_failed_tc = no_of_tc - no_of_pass_tc
    if no_of_failed_tc < 0:
        no_of_failed_tc=0
    general_logger.info(f"Total Number of Test Cases : {no_of_tc}")
    general_logger.info(f"Total Number of pass Test Cases : {no_of_pass_tc}")
    general_logger.info(f"Total Number of failed Test Cases : {no_of_failed_tc}")
    display_pi_chart_for_tc(no_of_tc, no_of_pass_tc,no_of_failed_tc,rf'{folder_path}')

