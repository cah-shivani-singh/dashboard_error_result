##########################################Scenario: Validate total blocked qty for Quarantine Storage Location should always be > 0, When searched for any invoice date, Then  CF_INSME_Qty > 0#####################
import sys
sys.path.append('PO\models\RCA3a')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_5():
    try:
        general_logger.info("******************* TESTCASE-05 : Scenario: Validate total blocked qty for Quarantine Storage Location should always be > 0, When searched for any invoice date, Then  CF_INSME_Qty > 0 *******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3a\error_records\TESTCASE5\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3a\RCA3a.json',0,None,True,5,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 05, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)

