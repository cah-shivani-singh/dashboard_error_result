##########################################Scenario: Validate short qty for the identified invoice is due to Product in Quarantine, When searching for any specific Process date, Then total number of invoices in rca3a showing 'Product in Quarantine - FDC' matches the count of invoices where blocked quantity in quarantine>=0.5*short quantity #####################
import sys
sys.path.append('PO\models\RCA3a')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_9():
    try:
        general_logger.info("*******************TESTCASE-09: Validate short qty for the identified invoice is due to Product in Quarantine, When searching for any specific Process date, Then total number of invoices in rca3a showing 'Product in Quarantine - FDC' matches the count of invoices where blocked quantity in quarantine>=0.5*short quantity*******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3a\error_records\TESTCASE9\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3a\RCA3a.json',0,None,True,9,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 09, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)


