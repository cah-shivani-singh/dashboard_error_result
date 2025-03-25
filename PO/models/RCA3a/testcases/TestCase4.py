########################################## Blocked Qty for Quarantine block location is displaying correct results, When searched for all material-plant for any invoice date, Then blocked qty for Quarantine storage loc displaying should be equal to blocked quantity for the material for the dc at the time of order received #####################
import sys
sys.path.append('PO\models\RCA3a')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_4():
    try:
        general_logger.info("*******************TESTCASE-04: Blocked Qty for Quarantine block location is displaying correct results, When searched for all material-plant for any invoice date, Then blocked qty for Quarantine storage loc displaying should be equal to blocked quantity for the material for the dc at the time of order received *******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3a\error_records\TESTCASE4\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3a\RCA3a.json',0,None,True,4,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 04, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)
