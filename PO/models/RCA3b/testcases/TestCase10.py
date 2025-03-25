##########################################Scenario: Validate the value for LF_Inv_AVAIL_QTY When searched for a material Then the LF_Inv_AVAIL_QTY should show the AVAIL_QTY for the material from VW_INVENTORYSNAPSHOT at location 99 #####################
import sys
sys.path.append('PO\models\RCA3b')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_10():
    try:
        general_logger.info("*******************TESTCASE 10 : Validate the value for LF_Inv_AVAIL_QTY When searched for a material Then the LF_Inv_AVAIL_QTY should show the AVAIL_QTY for the material from VW_INVENTORYSNAPSHOT at location 99*******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3b\error_records\TESTCASE10\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3b\RCA3b.json',0,None,True,10,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 10, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)



