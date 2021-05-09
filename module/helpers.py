import pandas as pd
import logging
from os import system, name

class HandlerFilter():
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno == self.__level

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

console_handler = logging.StreamHandler()
console_handler.addFilter(HandlerFilter(logging.INFO))

file_handler = logging.FileHandler('1_Banking_System/logs/banking_system.log')
file_handler.setFormatter(formatter)
file_handler.addFilter(HandlerFilter(logging.ERROR))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def csv_to_df(path):
    '''
    Read csv file into dataframe

    Returns:
        dataframe
         
    '''
    df = pd.read_csv(path)
        
    return df


 
def df_to_csv(df, path):
    ''' Save modifications in csv file from dataframe'''
        
    df.to_csv(path, index=False)



def clear():
    if name == "nt":
        s = system("cls")
  
    else:
        s = system("clear")


def validate_input(input):
    '''Validate that user entered some input'''
    if not input or input.isspace():
        raise ValueError

def validate_decimals(input):
    '''Validate input is decimal'''
    if not input.isdecimal():     
        raise ValueError

def validate_len(input, length):
    '''Validate input is a specific length'''
    if len(input) != length:     
        raise ValueError

def validate_option(input, options):
    '''Validate input is a valid option'''
    if not input in options:     
        raise ValueError

def validate_positive_n(input):              
    '''Validate input is positive'''    
    if input < 0:
        raise ValueError


def catch_exception(field, message, f1=None, f2=None, a2=None, dtype=None):
    
    while True:
        try:
            if dtype == "int":
                x = int(input(f"Enter {field}: "))
            
            else:
                x = str(input(f"Enter {field}: "))
            
            if f1:
                f1(x)
            
            if f2:
                f2(x, a2)
        
        except ValueError:
                logger.info(f"{field} {message}. Please try again.")
                logger.info("")
                logger.error(f"{field} {message}")
        else:
            break
    
    return x
