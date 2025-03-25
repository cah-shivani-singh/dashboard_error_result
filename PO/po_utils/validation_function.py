import sys
sys.path.append(r'PO\po_utils')
from po_utils.connection import bq_connection
from po_utils.get_process_date import get_process_date
from count_pass_failed_tescases import increment_count
from read_sql_queries_from_json import read_json_parameter_from_json
from tabulate import tabulate
from datetime import datetime
import pandas as pd
import os

import os


def check_duplicate(general_logger,error_logger,test_case_no,json_path,error_records_folder_name):
    process_date = get_process_date(general_logger,error_logger)
    '''
    it will check the duplicate : we need to pass below values
    general logger , error logger to log the error and information
    test_case_no : this field require as it with that testcase no it will read the json file and fetech sql
    json_path : path of respective rca
    error_records_folder_name : errror record folder name for each rca
    '''
    client = bq_connection(general_logger,error_logger)
    if process_date != '':
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            values = read_json_parameter_from_json(fr'{json_path}',f'TEST_CASE_{test_case_no}',general_logger,error_logger)
            if values is not None:
                project_name,dataset_id,table_id,query,top_75=values
            else:
                general_logger.info("Error the function return None due to exception")
            if process_date!='':
                
                try:
                    dups_query = query[0].format(project_name=project_name,dataset_id=dataset_id,table_id=table_id,process_date=process_date)
                    result = client.query(dups_query)
                except Exception as e:
                    general_logger.info("There is error while executing query check execution_log.log file for more info")
                    error_logger.error(f"TESTCASE - {test_case_no} : Error executing query : {e}")
                    return False
                dups_result_df = result.to_dataframe()  
                if dups_result_df.shape[0] > 0:
                    os.makedirs(error_records_folder_name,exist_ok=True) 
                    general_logger.info(f"Dups Validation Failed - Duplicates Found")
                    general_logger.info("Below are top 5 CINs for failed testcase")
                    general_logger.info(tabulate(dups_result_df.head(),headers='keys',tablefmt='grid',showindex=False))
                    #error_records_folder_name=rf'PO\RCA{test_case_no}\error_records\TESTCASE{test_case_no}'
                    f_name = f'rca{test_case_no}_test_case{test_case_no}_error_records_{timestamp}'
                    full_path = f'{error_records_folder_name}\{f_name}.csv'
                    dups_result_df.to_csv(full_path,index=False)
                    return False
                else:
                    increment_count('pass_tc_count',general_logger,error_logger)            
                    general_logger.info(f"Dups Validation IS PASSED - No Duplicates Found")
                    general_logger.info("Records for Top 5 CINs")
                    top_10_query=f"{top_75}"
                    top_10_formatted_query=top_10_query.format(project_name=project_name,dataset_id=dataset_id,table_id=table_id,process_date=process_date)
                    pass_record=client.query(top_10_formatted_query)
                    pass_record_df=pass_record.to_dataframe()
                    general_logger.info(tabulate(pass_record_df.head(5),headers='keys',tablefmt='grid',showindex=False))
                    return True
            else:
                    general_logger.info(f'No new records found in {table_id} for the latest Refresh')
        except Exception as e:
            general_logger.info(f"There is exception while running TESTCASE-{test_case_no}, check execution_log_error.log file")
            error_logger.error(f"Error executing query for TESTCASE-{test_case_no} : {e}")
            return False


def check_ddl_validation(general_logger,error_logger,json_path,src_schema_path,test_case_no):
    process_date = get_process_date(general_logger,error_logger)
    client = bq_connection(general_logger,error_logger)
    try:
        values = read_json_parameter_from_json(fr'{json_path}',f'TEST_CASE_{test_case_no}',general_logger,error_logger)
        if values is not None:
            project_name,dataset_id,table_id,query,top_75=values
        try:
            query = query[0].format(project_name=project_name,dataset_id=dataset_id,table_id=table_id,process_date=process_date)
            execute_query = client.query(query)
        except Exception as e:
            general_logger.info("There is error while executing query check execution_log.log file for more info")
            error_logger.error(f"TESTCASE - {test_case_no} : Error executing query : {e}")
            return False
        table=execute_query.to_dataframe()
        table_schema=table[['column_name','data_type']]
    except Exception as e:
        general_logger.info(f"Error while creating dataframe: check execution_log.log for more info")
        error_logger.error(f"TESTCASE - {test_case_no} : Error while creating dataframe: {e}")
        return False
    try:
        mapping_docc_schema_file=pd.read_csv(f"{src_schema_path}")
        mapping_schema=mapping_docc_schema_file[['column_name','data_type']]
        mapping_schema=mapping_schema.map(lambda x:x.lower() if isinstance(x,str) else x)
    except FileNotFoundError:
        general_logger.info("There is error while reading file check execution_log.log file for more info")
        error_logger.error(f"TESTCASE - {test_case_no} : File not found for schema validation {mapping_docc_schema_file}")
        return False
    except Exception as e:
        general_logger.info("Unexpected error occur, check execution_log.log file for more info")
        error_logger.error(f"TESTCASE - {test_case_no} : Unexpected error while reading schema: {e}")
        return False
    try:
        merged_df=pd.merge(mapping_schema,table_schema,on='column_name',how='outer',suffixes=('_source','_target'))
        mismatch_data_types = merged_df[(merged_df['data_type_source'] != merged_df['data_type_target']) & (~merged_df['data_type_target'].isna())]
        missing_columns_in_target=merged_df[merged_df['data_type_target'].isna()]
        discrepencies=pd.concat([mismatch_data_types,missing_columns_in_target])
        discrepencies['discrepancy']=discrepencies.apply(
            lambda row: f"Column : {row['column_name']}, Source DataType: {row['data_type_source']}, Target DataType: {row['data_type_target']}",axis=1
        )
        if discrepencies.shape[0] > 0:
            general_logger.info(f"DDL validation Failed - Discrepencies Found")
            general_logger.info(tabulate(discrepencies,headers='keys',tablefmt='grid',showindex=False))
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            error_records_folder_name=rf'PO\RCA{test_case_no}\error_records\TESTCASE{test_case_no}\{timestamp}'
            os.makedirs(error_records_folder_name,exist_ok=True)  
            f_name=f'rca{test_case_no}_ddl_validation_{timestamp}'
            full_path=f'{error_records_folder_name}\{f_name}.csv'
            discrepencies.to_csv(full_path,index=False)
            return False
        else:
            increment_count('pass_tc_count',general_logger,error_logger)
            general_logger.info(f"DDL VALIDATION IS PASSED - Column Name and Data Type is Matching")
            return True
    except Exception as e:
        general_logger.info(f"There is exception while running TESTCASE-{test_case_no}, check execution_log_error.log file")
        error_logger.error(f"Error executing query for TESTCASE-{test_case_no} : {e}")
        return False

def validate_data(general_logger,error_logger,json_path,query_no,supplier_type,top_75_flag,test_case_no,error_records_folder_name):
    process_date = get_process_date(general_logger,error_logger)
    client = bq_connection(general_logger,error_logger)
    '''
    it will check validate data : we need to pass below values
    general logger , error logger to log the error and information
    test_case_no : this field require as it with that testcase no it will read the json file and fetech sql
    json_path : path of respective rca
    error_records_folder_name : errror record folder name for each rca
    '''

    #query=query.format(project_name=project_name,dataset_id=dataset_id,table_id=table_id,process_date=process_date)
    if process_date != '':
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        try:
            values = read_json_parameter_from_json(fr'{json_path}',f'TEST_CASE_{test_case_no}',general_logger,error_logger)
            if values is not None:
                project_name,dataset_id,table_id,query,top_75=values
            if process_date != '':
                try:
                    q=query[query_no].format(project_name=project_name,dataset_id=dataset_id,table_id=table_id,process_date=process_date)
                    result=client.query(q)
                except Exception as e:
                    general_logger.info("There is error while executing query check execution_log.log file for more info")
                    error_logger.error(f"TESTCASE - {test_case_no} : Error executing query : {e}")
                    return False
                result_df=result.to_dataframe()
                if result_df.shape[0] > 0:
                    if not os.path.exists(error_records_folder_name):
                        os.makedirs(error_records_folder_name,exist_ok=True) 
                    if supplier_type is not None:
                        general_logger.info(f"Validation Failed for '{supplier_type}' ,{result_df.shape[0]} records, check error file and log for more details")
                        f_name=f'rca1_test_case{test_case_no}_{str(supplier_type).lower()}_error_records_{timestamp}'                                  
                    else:                     
                        general_logger.info(f"Validation Failed for ,{result_df.shape[0]} records, check error file and log for more details")
                        f_name=f'rca1_test_case{test_case_no}__error_records_{timestamp}'             
                    general_logger.info(tabulate(result_df.head(),headers='keys',tablefmt='grid',showindex=False))
                    full_path=f'{error_records_folder_name}\{f_name}.csv'
                    result_df.to_csv(full_path,index=False)
                    return False
                else:
                    if supplier_type is not None:
                        general_logger.info(f"Validation IS PASSED for  - {supplier_type}")
                    else:
                        general_logger.info(f"Validation IS PASSED")

                    if top_75_flag:
                        general_logger.info("Records for Top 5 CINs")
                        top_75_query=f"{top_75}"
                        top_75_formatted_query=top_75_query.format(project_name=project_name,dataset_id=dataset_id,table_id=table_id,process_date=process_date)
                        pass_record=client.query(top_75_formatted_query)
                        pass_record_df=pass_record.to_dataframe()
                        general_logger.info(tabulate(pass_record_df.head(5),headers='keys',tablefmt='grid',showindex=False))
                    return True
        except Exception as e:
            general_logger.info(f"There is exception while running TESTCASE-{test_case_no}, check execution_log_error.log file")
            error_logger.error(f"Error executing query for TESTCASE-{test_case_no} : {e}")
            return False
    else:        
        general_logger.info(f'No new records found in {table_id} for the latest Refresh ')
        return True


