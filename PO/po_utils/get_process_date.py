def get_process_date(general_logger,error_logger):
    '''
    this will return tha max process date on which the data is refreshed
    '''
    process_date=''
    path=r"PO\config\timestamp.properties"
    try:
        with open(path,"r") as config_file:
            lines=config_file.readlines()
            for line in lines:
                line=line.strip()
                if line.startswith('process_date'):
                    process_date=line.split('=')[1]
                    return process_date
    except FileNotFoundError:
        error_logger.error(f"Error: JSON file not found at {path}")


