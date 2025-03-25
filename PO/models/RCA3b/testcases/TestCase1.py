####################TEST CASE 1 DDL VALIDATION COLUMN NAME AND DATA TYPE VALIDATION ####################
import sys
sys.path.append('PO\models\RCA3b')
from wrapper import general_logger,error_logger
from po_utils import check_ddl_validation
import warnings
warnings.filterwarnings('ignore')

def exec_testcase_1():
    try:
        general_logger.info("*******************TESTCASE 1 - DDL VALIDATION COLUMN NAME AND DATA TYPE VALIDATION*******************")
        check_ddl_validation(general_logger,error_logger,'PO\models\RCA3b\RCA3b.json',r'PO\models\RCA3b\rca3b_schema.csv',1)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 01, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)

