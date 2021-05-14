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


def option_input_validation(menu, option, options=1, m1=None, m2=None, m3=None, m4=None, m5=None, o2=None, o3=None):

    f = False   
    
    while True:
            try:
                if option == 0 or f == True:
                    break                
                option = int(input("Enter your option: "))

            except ValueError:
                logger.error("User info inputted was not int type")
                clear()
                menu()
                logger.info("Invalid option. Please try again.")
                logger.info("")                           
                       
            else:               
                while option != 0:           
                  
                    if options == 1:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                        
                    
                    elif options == 2:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:                           
                            if o2 == None:
                                m2()
                            else:
                                m2(o2)
                            f = True
                            break
                        
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                    
                    elif options == 3:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:                           
                            if o2 == None:
                                m2()
                            else:
                                m2(o2)
                            f = True
                            break
                        if option == 3:                           
                            if o3 == None:
                                m3()
                            else:
                                m3(o3)
                            f = True
                            break        
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                    elif options == 4:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:
                            m2()
                            f = True
                            break
                        if option == 3:
                            m3()
                            f = True  
                            break
                        if option == 4:
                            m4()
                            f = True  
                            break       
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                        
                    elif options == 5:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:
                            m2()
                            f = True
                            break
                        if option == 3:
                            m3()
                            f = True  
                            break
                        if option == 4:
                            m4()
                            f = True  
                            break
                        if option == 5:
                            m5()
                            f = True  
                            break           
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break


def option_input_validation_main(menu, option, options=1, m1=None, m2=None, m3=None, m4=None, m5=None):

    f = False   
    
    while True:
            try:
                if option == 0:
                    return 0                
                option = int(input("Enter your option: "))

            except ValueError:
                logger.error("User info inputted was not int type")
                clear()
                menu()
                logger.info("Invalid option. Please try again.")
                logger.info("")                           
                       
            else:               
                while option != 0:           
                  
                    if options == 1:
                    
                        if option == 1:
                            return 1
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                        
                    
                    elif options == 2:
                    
                        if option == 1:
                            return 1
                    
                        if option == 2:
                            return 2
                                                   
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                    
                    elif options == 3:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:
                            m2()
                            f = True
                            break
                        if option == 3:
                            m3()
                            f = True  
                            break         
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                    elif options == 4:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:
                            m2()
                            f = True
                            break
                        if option == 3:
                            m3()
                            f = True  
                            break
                        if option == 4:
                            m4()
                            f = True  
                            break       
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break
                        
                    elif options == 5:
                    
                        if option == 1:
                            m1()
                            f = True
                            break
                        if option == 2:
                            m2()
                            f = True
                            break
                        if option == 3:
                            m3()
                            f = True  
                            break
                        if option == 4:
                            m4()
                            f = True  
                            break
                        if option == 5:
                            m5()
                            f = True  
                            break           
                        
                        else:
                            clear()
                            menu()
                            logger.info("Invalid option. Please try again.")
                            logger.info("")
                            
                            while True:
                                try:
                                    option = int(input("Enter your option: "))
                                    
                                except ValueError:
                                    logger.error("User info inputted was not int type")
                                    clear()
                                    menu()
                                    logger.info("Invalid option. Please try again.")
                                    logger.info("")
                                else:
                                    break

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

def validate_month(input):              
    '''Validate input is valid month'''
    if int(input) < 0 or int(input) > 12:
        raise ValueError

def validate_day(input, a2):              
    '''Validate input is valid day'''    
    if int(a2) in (1, 3, 5, 7, 8, 10, 12):        
        if int(input) < 0 or int(input) > 31:
            raise ValueError
    elif int(a2) in (4, 6, 10, 11):            
        if int(input) < 0 or int(input) > 30:
            raise ValueError
    elif int(a2) == 2:           
        if int(input) < 0 or int(input) > 28:
            raise ValueError

def validate_year(input):              
    '''Validate input is valid month'''    
    if int(input) < 1900 or int(input) > 2005:
        raise ValueError

def validate_credit_score(input):              
    '''Validate input is an acceptable credit score'''    
    if int(input) < 600 or int(input) > 800:
        raise ValueError

def validate_interest(input):              
    '''Validate input is an interest rate from 0.05% to 0.5%'''    
    if float(input) < 0.05 or float(input) > 0.5:
        raise ValueError

def validate_terms(input):              
    '''Validate input is terms: 12, 24, 36, 48 or 60 months'''    
    if not int(input) in (12, 24, 36 , 48, 60):
        raise ValueError

def catch_exception(field, message, f1=None, f2=None, a2=None, f3=None, a3=None, dtype=None, format=""):
    '''Catch exceptions on menu data inputs'''
    
    while True:
        try:
            if dtype == "int":
                x = int(input(f"Enter {field}: "))
            
            else:
                x = str(input(f"Enter {field}{format}: "))
            
            if f1:
                f1(x)
            
            if f2:
                if a2 == None:
                    f2(x)
                else:
                    f2(x, a2)
            
            if f3:
                if a3 == None:
                    f3(x)
                else:
                    f3(x, a3)
        
        except ValueError:
                logger.info(f"{field} {message}. Please try again.")
                logger.info("")
                logger.error(f"{field} {message}")
        else:
            break
    
    return x
