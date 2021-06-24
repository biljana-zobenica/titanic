# -*- coding: utf-8 -*-
import os
from dotenv import find_dotenv, load_dotenv
from requests import session
import logging

# payload for login to kaggle
payload = {
    'action': 'login',
    'username': os.environ.get("KAGGLE_USERNAME"),
    'password': os.environ.get("KAGGLE_PASSWORD")
}

def extract_data(url, file_path):
    """
    method to extract data
    """
    # setup session
    with session() as c:
        c.post('https://www.kaggle.com/account/login', data=payload)
        # open file to write
        with open(file_path, 'w') as handle:
            response = c.get(url, stream=True)
            for block in response.iter_content(1024):
                handle.write(str(block))
                
def main(project_dir):
    """
    main method
    """
    # get logger -> creating project instance with getLogger method
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
    
    # urls
    train_url = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/train.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1620293448&Signature=m4SIvoFVztFrHR%2F5nhuO%2B%2BmRy%2FkJeSSnGN95AQtr7hMVuCdFVGH5OEsqzd1%2BdjP0paxwyiyDMFrzX43HFjNoLzNWVMeILFtURrtQ9YmlJcrJRz%2Bit2cJO5nYP0VEMf3NnxJxG%2Bwdx%2BXENpmZRQn7HzviV5E0Nu6Kt7qCI9QW%2Fo3Tl6DSmaBtjNQpr%2BeH1zAC9cjaiEl0qDs2idjbsMfih7Q%2FTznLqdlR9LmdNkycMikwcDLH1bmRAJhilXbq7hPM%2BNz8wkcj3rs3NEQ38n34RggseVHziROTc1FdY8xuBXoWQevOTqlVOOCCD8zhMV%2F9tKixOuoxMKw7r97rjq22ZA%3D%3D&response-content-disposition=attachment%3B+filename%3Dtrain.csv'
    test_url = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/test.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1620295049&Signature=eDkjZ%2FJUbY%2BnlZMa1rhCPvwNqkNUICW15Qb%2BIRO5aQJbEjABPslaJ3qc5b2%2FpUIt0Uhy%2FNohBlhqaOmCwVGzXkLaFgmF7ZL%2BdHWBQTLcc61m2bCBsxJbmvlAtU8glNnIZrIG1YSQZzk1C7U4C8aPAWme7qDNjIfzOgYLNzptkgXDyWLADQbAdqCgjBHiD42sST82%2FSrVqLeeebCPIRhROqA3kz8VCKASpdPU7sUQRysWIFm2oT%2BnVVBsxpOhLP%2F7RKo6zeF6YyJM%2FH88%2FpwddiAxa6poTqMbEjZGvLaWFIAalnj3LlySXVSGpD3QMvoQKgIBc5dHyiCuCDuqVI609Q%3D%3D&response-content-disposition=attachment%3B+filename%3Dtest.csv'

    # file paths
    raw_data_path = os.path.join(project_dir, 'data', 'raw')
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')

    # extract data -> using extract_data method to download the files
    extract_data (train_url, train_data_path)
    extract_data (test_url, test_data_path)
    logger.info('downloaded raw training and test data')
    
if __name__ == '__main__':
    #getting root directory -> script file is two levels down from the root folder
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    # find .env automatically by walking up directories until it's found
    dotenv_path = find_dotenv()
    # load up the entries as environment variables
    load_dotenv(dotenv_path)
    
    # call the main
    main(project_dir)
      
