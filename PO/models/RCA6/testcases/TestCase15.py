import sys
sys.path.append('PO\models\RCA6')
from wrapper import general_logger,error_logger
import warnings
warnings.filterwarnings('ignore')
from po_utils.set_process_date import get_json_path
from po_utils.read_sql_queries_from_json import read_description
from po_utils.validation_function import validate_data
from po_utils.count_pass_failed_tescases import increment_count
from datetime import datetime

warnings.filterwarnings('ignore')
def exec_testcase_15():
    try:
        json_path = get_json_path()
        description_of_tc = read_description(rf'{json_path}',15,general_logger,error_logger) 
        general_logger.info(f"TESTCASE 15 - {description_of_tc} \n")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA6\error_records\TESTCASE15\{timestamp}'
        general_logger.info("Validationg : the value of DUPLICATEMATERIAL should match with the source Material Master Model")
        nul_res = validate_data(general_logger,error_logger,'PO\models\RCA6\RCA6.json',0,None,False,15,error_records_folder_name)
        general_logger.info("Validationg : DUPLICATEMATERIAL should not be SEQUESTERED")
        shortcode_res = validate_data(general_logger,error_logger,'PO\models\RCA6\RCA6.json',1,None,True,15,error_records_folder_name)
        if nul_res & shortcode_res:
            increment_count('pass_tc_count',general_logger,error_logger)

    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 15, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)



