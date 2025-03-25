##########################################The supplier should be FDC, When searched for the supplier number Then it should not be equal to 90163 #####################
import sys
sys.path.append('PO\models\RCA3a')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_3():
    try:
        general_logger.info("*******************TESTCASE0-03: The supplier should be FDC, When searched for the supplier number Then it should not be equal to 90163*******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3a\error_records\TESTCASE3\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3a\RCA3a.json',0,None,True,3,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 03, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)

