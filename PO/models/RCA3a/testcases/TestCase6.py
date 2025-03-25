##########################################Scenario: The blocked quantity in quarantine should be atleast half of the shorted quantity for an invoice,When searched for the blocked quantity in quarantine for a particular material-plantThen the blocked quantity (CF_INSME_Qty) >= 0.5*shorted quantity(CF_CIN_DC_SHORT_QTY) #####################
import sys
sys.path.append('PO\models\RCA3a')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_6():
    try:
        general_logger.info("*******************TESTCASE-06: The blocked quantity in quarantine should be atleast half of the shorted quantity for an invoice,When searched for the blocked quantity in quarantine for a particular material-plantThen the blocked quantity (CF_INSME_Qty) >= 0.5*shorted quantity(CF_CIN_DC_SHORT_QTY) *******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3a\error_records\TESTCASE6\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3a\RCA3a.json',0,None,True,6,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 06, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)




