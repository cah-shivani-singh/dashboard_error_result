import sys
sys.path.append('PO\models\RCA12')
from wrapper import general_logger,error_logger
import warnings
warnings.filterwarnings('ignore')
from po_utils.set_process_date import get_json_path
from po_utils.read_sql_queries_from_json import read_description
from po_utils.validation_function import validate_data
from po_utils.count_pass_failed_tescases import increment_count
from datetime import datetime

warnings.filterwarnings('ignore')
def exec_testcase_12():
    try:
        json_path = get_json_path()
        description_of_tc = read_description(rf'{json_path}',12,general_logger,error_logger) 
        general_logger.info(f"TESTCASE 12 - {description_of_tc} \n")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA12\error_records\TESTCASE12\{timestamp}'
        general_logger.info("Validationg : standard deviation of ordered qty of ship_to_customer calculated on distinct order date for a given process date")
        shipcuststd_table = validate_data(general_logger,error_logger,'PO\models\RCA12\RCA12.json',0,None,False,12,error_records_folder_name)
        general_logger.info("Validationg : variance of ordered qty of ship_to_customer calculated on distinct order date for a given process date")
        shipcustvar_table = validate_data(general_logger,error_logger,'PO\models\RCA12\RCA12.json',1,None,True,12,error_records_folder_name)
        if shipcuststd_table & shipcustvar_table:
            increment_count('pass_tc_count',general_logger,error_logger)

    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 012, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)



