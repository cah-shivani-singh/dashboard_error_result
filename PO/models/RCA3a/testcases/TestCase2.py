import sys
sys.path.append('PO\models\RCA3a')
from wrapper import general_logger,error_logger
from po_utils import check_duplicate
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_2():
    try:
        general_logger.info("*******************TESTCASE 2 - CHECK FOR DUPLICATES*******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3a\error_records\TESTCASE2\{timestamp}'
        check_duplicate(general_logger,error_logger,2,'PO\models\RCA3a\RCA3a.json',error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 02, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)

