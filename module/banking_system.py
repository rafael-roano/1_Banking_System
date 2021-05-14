from datetime import date
import pandas as pd
import helpers as h
import logging
import time
start_time = time.time()

class UpdateError(Exception):
    def __init__(self, value = None):
        self.value = value

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


class User:
    '''
    Abstract class to create users in system. Parent class to Employee and Customer classes
    '''
    def __init__(self, user_info):
        '''
        Initialize User object.
              
        Args:
            user_info (list):        
                first_name (str): User's first name
                last_name (str): User's last name
                address (str): User's address
                phone (str): User's phone number
        '''
        
        user_info_ser = pd.Series(user_info)                                                                # Create Pd series from list argument
        self._first_name, self._last_name, self._address, self._phone, self._creation_date = \
            user_info_ser[0], user_info_ser[1],user_info_ser[2], user_info_ser[3], date.today()       
                                                                                                
    @property
    def first_name(self):
        '''Make attribute first_name a read-only property'''
        return self._first_name

    @property
    def last_name(self):
        '''Make attribute last_name a read-only property'''
        return self._last_name

    @property
    def address(self):
        '''Make attribute address a read-only property'''
        return self._address

    @property
    def phone(self):
        '''Make attribute phone a read-only property'''
        return self._phone
    
    @property
    def creation_date(self):
        '''Make attribute creation_date a read-only property'''
        return self._creation_date   

    @classmethod
    def evaluate_id(cls, id): 
        '''
        Evaluates if id is valid
        
        Args:
            id (int): Employee's ID to validate
        '''
        pass
        
    @classmethod
    def update_address(cls, new_address):
        '''
        Update user's address.
        
        Args:
            address (str): User's new address to assign to object.
        '''
        pass
    
    @classmethod
    def update_phone(cls, new_phone):
        '''
        Update user's phone number.
        
        Args:
            phone (str): User's new phone number to assign to object.
        '''
        pass
   

class Employee(User):
    '''
    Subclass from User class to create Employee records.
    '''
    TOTAL_EMPLOYEES = 0                                                                                 # Class Attribute to load total employees
    EMPLOYEE_ID_COUNT = 0                                                                               # Class Attribute to load employee ID count

    def __init__(self, user_info, employee_info):
        '''
        Initialize Employee object.
                
        Args:
            first_name (str): Employee's first name to assign to object.
            last_name (str): Employee's last name to assign to object.
            address (str): Employee's address to assign to object.
            phone (str): Employee's phone number to assign to object.           
            level (int): Employee's level (1=Junior, 2=Lead, 3=Senior)
            salary (int): Employee's salary
            status (bool): Employee's Status
        '''
        User.__init__(self, user_info)
        self.increase_employees()                                                                    # Increase Employee and ID counters by one
    
        employee_info_ser = pd.Series(employee_info)                                                    # Create Pd series from list argument
        self._employee_id, self._level, self._salary, self._status = \
            Employee.EMPLOYEE_ID_COUNT, employee_info_ser[0], employee_info_ser[1], True
                      
        employees = h.csv_to_df("1_Banking_System/data/Employees.csv")                                  # Helper function to open and read csv into df               
        employees = self.update_df(employees)                                                           # Update df with new Employee object info
        employees = self._convert_df_datatypes(employees)                                               # Convert df data types
        h.df_to_csv(employees, "1_Banking_System/data/Employees.csv")                                   # Helper function to save df back to csv 
        self.save_total_employees()                                                                     # Save total employees and ID count back to csv

        logger.info(f"Employee ID {self.employee_id} was added successfully")
        
    @property
    def employee_id(self):
        '''Make attribute employee_id a read-only property'''
        return self._employee_id

    @property
    def level(self):
        '''Make attribute level a read-only property'''
        return self._level

    @property
    def salary(self):
        '''Make attribute salary a read-only property'''
        return self._salary

    @property
    def status(self):
        '''Make attribute status a read-only property'''
        return self._status

    @classmethod
    def evaluate_id(cls, emp_id, status=None): 
        '''
        Evaluates if employee id is valid
        
        Args:
            emp_id (int): Employee's ID to validate
            status (bool, optional): If True, checks if employee's ID is already inactive

        Raises:            
            ValueError: Check if emp_id exists.

        '''            
        User.evaluate_id(emp_id)

        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]                             # Read employee ID count

        if (emp_id < 1) or (emp_id > Employee.EMPLOYEE_ID_COUNT):
            raise ValueError
        
        if status == True:
            employees = h.csv_to_df("1_Banking_System/data/Employees.csv")
            
            if employees[employees["employee_id"] == emp_id]["active"].bool() == False:

                raise UpdateError

    @classmethod
    def update_address(cls, emp_id, new_address):
        '''
        Update employee's address.
        
        Args:
            new_address (str): Employee's new address.
            emp_id (int): Employee's ID to update address.
        '''
        User.update_address(new_address)

        employees = h.csv_to_df("1_Banking_System/data/Employees.csv")                                  # Helper function to open and read csv into df         
        employees.at[employees.employee_id == emp_id, "address"] = new_address                          # Update address in df        
        employees = cls._convert_df_datatypes(employees)                                                # Convert df data types
        h.df_to_csv(employees, "1_Banking_System/data/Employees.csv")                                   # Helper function to save df back to csv
                
        logger.info(f"Employee ID {emp_id}'s address was updated to {new_address}")

    @classmethod
    def update_phone(cls, emp_id, new_phone):
        '''
        Update employee's address.
        
        Args:
            new_phone (str): Employee's new phone number.
            emp_id (int): Employee's ID to update phone number.
        '''
        User.update_phone(new_phone)
        
        employees = h.csv_to_df("1_Banking_System/data/Employees.csv")                                  # Helper function to open and read csv into df         
        employees.at[employees.employee_id == emp_id, "phone"] = new_phone                              # Update phone number in df        
        employees = cls._convert_df_datatypes(employees)                                                # Convert df data types
        h.df_to_csv(employees, "1_Banking_System/data/Employees.csv")                                   # Helper function to save df back to csv
                
        logger.info(f"Employee ID {emp_id}'s phone number was updated to {new_phone}")
    
    @classmethod
    def increase_employees(cls):
        '''
        Get current total employee quantity and current ID count from csv file (cls_attr.csv) and increase by 1 when initiliazing new Employee object
                       
        '''
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.TOTAL_EMPLOYEES = cls_attr_df.at["TOTAL_EMPLOYEES", 1]
        Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]
        Employee.TOTAL_EMPLOYEES += 1
        Employee.EMPLOYEE_ID_COUNT += 1
        
    def update_df(self, df):
        ''' Update Dataframe with new Employee object initialized'''

        i = Employee.EMPLOYEE_ID_COUNT - 1
        
        df.at[i, "employee_id"] = Employee.EMPLOYEE_ID_COUNT
        df.at[i, "first_name"] = self.first_name
        df.at[i, "last_name"] = self.last_name
        df.at[i, "address"] = self.address
        df.at[i, "phone"] = self.phone
        df.at[i, "level"] = self.level
        df.at[i, "salary"] = self.salary
        df.at[i, "creation_date"] = self.creation_date
        df.at[i, "active"] = self.status

        return df

    @staticmethod
    def _convert_df_datatypes(df):
        ''' Convert Dataframe Data Types'''

        df["employee_id"] = df["employee_id"].astype('int')
        df["first_name"] = df["first_name"].astype('str')
        df["last_name"] = df["last_name"].astype('str')
        df["address"] = df["address"].astype('str')
        df["phone"] = df["phone"].astype('str')
        df["level"] = df["level"].astype('int')
        df["salary"] = df["salary"].astype('int')
        df["active"] = df["active"].astype('bool')

        return df
        
    @classmethod
    def save_total_employees(cls):
        '''Save Total Employees and ID count into csv file (cls_attr.csv)'''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        cls_attr_df.at["TOTAL_EMPLOYEES", 1] = Employee.TOTAL_EMPLOYEES
        cls_attr_df.at["EMPLOYEE_ID_COUNT", 1] = Employee.EMPLOYEE_ID_COUNT
        cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
     
    @classmethod
    def inactivate_employee(cls, emp_id):
        '''
        Inactivate employee
                                
        Args:            
            emp_id (int): Employee's ID to deactivate.        
        '''
        
        employees = h.csv_to_df("1_Banking_System/data/Employees.csv")
        employees.at[employees.employee_id == emp_id, "active"] = False
        employees = cls._convert_df_datatypes(employees)
        h.df_to_csv(employees, "1_Banking_System/data/Employees.csv")
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.TOTAL_EMPLOYEES = cls_attr_df.at["TOTAL_EMPLOYEES", 1]
        Employee.TOTAL_EMPLOYEES -= 1
        cls_attr_df.at["TOTAL_EMPLOYEES", 1] = Employee.TOTAL_EMPLOYEES
        cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
        
        logger.info(f"Employee ID {emp_id} was inactivated")        
        
    @classmethod
    def get_total_employees(cls):
        '''
        Get total employees.                      
        '''
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.TOTAL_EMPLOYEES = cls_attr_df.at["TOTAL_EMPLOYEES", 1]
        Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]
                
        logger.info(f"Total Active Employees: {Employee.TOTAL_EMPLOYEES}")
        logger.info(f"Total Employee ID's: {Employee.EMPLOYEE_ID_COUNT}")

class Customer(User):
    '''
    Subclass from User class to create Customer records.
    '''
    TOTAL_CUSTOMERS = 0                                                                                 # Class Attribute to load total customers
    CUSTOMER_ID_COUNT = 0                                                                               # Class Attribute to load customer ID count
    
    def __init__(self, user_info, customer_info):
        '''
        Initialize Customer object.
                
        Args:
            first_name (str): Customer's first name to assign to object.
            last_name (str): Customer's last name to assign to object.
            address (str): Customer's address to assign to object.
            phone (str): Customer's phone number to assign to object.
            date_birth (date): Customer's date of birth to assign to object.         
        '''
        
        User.__init__(self, user_info)
        self.increase_customers()                                                                       # Increase Customer and ID counters by one
    
        customer_info_ser = pd.Series(customer_info)                                                    # Create Pd series from list argument
        self._customer_id, self._date_birth, self._credit_score, self._active_products, self._status = \
            Customer.CUSTOMER_ID_COUNT, customer_info_ser[0], 0, 0, True
             
        customers = h.csv_to_df("1_Banking_System/data/Customers.csv")                                  # Helper function to open and read csv into df               
        customers = self.update_df(customers)                                                           # Update df with new Customer object info
        customers = self._convert_df_datatypes(customers)                                               # Convert df data types
        h.df_to_csv(customers, "1_Banking_System/data/Customers.csv")                                   # Helper function to save df back to csv 
        self.save_total_customers()                                                                     # Save total customers and ID count back to csv

        logger.info(f"Customer ID {self._customer_id} was added successfully")

    @property
    def customer_id(self):
        '''Make attribute customer_id a read-only property'''
        return self._customer_id
    
    @property
    def date_birth(self):
        '''Make attribute date_birth a read-only property'''
        return self._date_birth
    
    @property
    def credit_score(self):
        '''Make attribute credit_score a read-only property'''
        return self._credit_score

    @property
    def active_products(self):
        '''Make attribute active_products a read-only property'''
        return self._active_products
    
    @property
    def status(self):
        '''Make attribute status a read-only property'''
        return self._status
    
    @classmethod
    def evaluate_id(cls, cus_id, status=None): 
        '''
        Evaluates if customer id is valid
        
        Args:
            cus_id (int): Customer's ID to validate
            status (bool, optional): If True, checks if customer's ID is already inactive

        Raises:            
            ValueError: Check if cus_id exists.

        '''            
        User.evaluate_id(cus_id)

        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Customer.CUSTOMER_ID_COUNT = cls_attr_df.at["CUSTOMER_ID_COUNT", 1]                             # Read customer ID count

        if (cus_id < 1) or (cus_id > Customer.CUSTOMER_ID_COUNT):            
            raise ValueError
        
        if status == True:
            customers = h.csv_to_df("1_Banking_System/data/Customers.csv")
            
            if customers[customers["customer_id"] == cus_id]["active"].bool() == False:
                raise UpdateError
    
    @classmethod
    def update_address(cls, cus_id, new_address):
        '''
        Update customer's address.
        
        Args:
            new_address (str): Customer's new address.
            cus_id (int): Customer's ID to update address.
        '''
        User.update_address(new_address)

        customers = h.csv_to_df("1_Banking_System/data/Customers.csv")                                  # Helper function to open and read csv into df         
        customers.at[customers.customer_id == cus_id, "address"] = new_address                          # Update address in df        
        customers = cls._convert_df_datatypes(customers)                                                # Convert df data types
        h.df_to_csv(customers, "1_Banking_System/data/Customers.csv")                                   # Helper function to save df back to csv
                
        logger.info(f"Customer ID {cus_id}'s address was updated to {new_address}")
    
    @classmethod
    def update_phone(cls, cus_id, new_phone):
        '''
        Update customer's address.
        
        Args:
            new_phone (str): Customer's new phone number.
            cus_id (int): Customer's ID to update phone number.
        '''
        User.update_phone(new_phone)
        
        customers = h.csv_to_df("1_Banking_System/data/Customers.csv")                                  # Helper function to open and read csv into df         
        customers.at[customers.customer_id == cus_id, "phone"] = new_phone                              # Update phone number in df        
        customers = cls._convert_df_datatypes(customers)                                                # Convert df data types
        h.df_to_csv(customers, "1_Banking_System/data/Customers.csv")                                   # Helper function to save df back to csv
                
        logger.info(f"Customer ID {cus_id}'s phone number was updated to {new_phone}")
    
    @classmethod
    def update_credit_score(cls, cus_id, credit_score):
        '''
        Update customer's credit_score.
        
        Args:
            credit_score (int): Customer's credit score.
            cus_id (int): Customer's ID to update credit score.
        '''

        customers = h.csv_to_df("1_Banking_System/data/Customers.csv")                                  # Helper function to open and read csv into df         
        customers.at[customers.customer_id == cus_id, "credit_score"] = credit_score                    # Update phone number in df        
        customers = cls._convert_df_datatypes(customers)                                                # Convert df data types
        h.df_to_csv(customers, "1_Banking_System/data/Customers.csv")                                   # Helper function to save df back to csv
                
        logger.info(f"Credit Score of {credit_score} saved on Customer ID {cus_id} profile")
        input("Press Enter to continue...")
    
    @classmethod
    def increase_customers(cls):
        '''
        Get current total customer quantity and current ID count from csv file (cls_attr.csv) and increase by 1 when initiliazing new Customer object               
        '''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Customer.TOTAL_CUSTOMERS = cls_attr_df.at["TOTAL_CUSTOMERS", 1]
        Customer.CUSTOMER_ID_COUNT = cls_attr_df.at["CUSTOMER_ID_COUNT", 1]
        Customer.TOTAL_CUSTOMERS += 1
        Customer.CUSTOMER_ID_COUNT += 1

    def update_df(self, df):
        ''' Update Dataframe with new Customer object initialized'''

        i = Customer.CUSTOMER_ID_COUNT - 1
        
        df.at[i, "customer_id"] = Customer.CUSTOMER_ID_COUNT
        df.at[i, "first_name"] = self.first_name
        df.at[i, "last_name"] = self.last_name
        df.at[i, "address"] = self.address
        df.at[i, "phone"] = self.phone
        df.at[i, "date_birth"] = self.date_birth
        df.at[i, "credit_score"] = self.credit_score
        df.at[i, "active_products"] = self.active_products
        df.at[i, "creation_date"] = self.creation_date
        df.at[i, "active"] = self.status

        return df
    
    @staticmethod
    def _convert_df_datatypes(df):
        ''' Convert Dataframe Data Types'''

        df["customer_id"] = df["customer_id"].astype('int')
        df["first_name"] = df["first_name"].astype('str')
        df["last_name"] = df["last_name"].astype('str')
        df["address"] = df["address"].astype('str')
        df["phone"] = df["phone"].astype('str')
        df["credit_score"] = df["credit_score"].astype('int')
        df["active_products"] = df["active_products"].astype('int')
        df["active"] = df["active"].astype('bool')

        return df

    @classmethod
    def save_total_customers(cls):
        '''Save Total Customers and ID count into csv file (cls_attr.csv)'''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        cls_attr_df.at["TOTAL_CUSTOMERS", 1] = Customer.TOTAL_CUSTOMERS
        cls_attr_df.at["CUSTOMER_ID_COUNT", 1] = Customer.CUSTOMER_ID_COUNT
        cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
    
    @classmethod
    def inactivate_customer(cls, cus_id):
        '''
        Inactivate customer
                                
        Args:            
            cus_id (int): Customer's ID to deactivate.        
        '''      
        
        customers = h.csv_to_df("1_Banking_System/data/Customers.csv")
        customers.at[customers.customer_id == cus_id, "active"] = False
        customers.at[customers.customer_id == cus_id, "active_products"] = 0
        customers = cls._convert_df_datatypes(customers)
        h.df_to_csv(customers, "1_Banking_System/data/Customers.csv")
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Customer.TOTAL_CUSTOMERS = cls_attr_df.at["TOTAL_CUSTOMERS", 1]
        Customer.TOTAL_CUSTOMERS -= 1
        cls_attr_df.at["TOTAL_CUSTOMERS", 1] = Customer.TOTAL_CUSTOMERS
        cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
        
        logger.info(f"Customer ID {cus_id} was inactivated")
    
    @classmethod
    def get_total_customers(cls):
        '''
        Get total customers.                      
        '''
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Customer.TOTAL_CUSTOMERS = cls_attr_df.at["TOTAL_CUSTOMERS", 1]
        Customer.CUSTOMER_ID_COUNT = cls_attr_df.at["CUSTOMER_ID_COUNT", 1]
                
        logger.info(f"Total Active Customers: {Customer.TOTAL_CUSTOMERS}")
        logger.info(f"Total Customer ID's: {Customer.CUSTOMER_ID_COUNT}")

    @classmethod
    def increase_active_products(cls, cus_id):
        '''
        Increase active products on customer profile.                    
        
        Args:
            cus_id (int): Customer's ID to increase products active.
        '''
                      
        customers = h.csv_to_df("1_Banking_System/data/Customers.csv")      
        active_products = customers.loc[customers['customer_id'] == cus_id, "active_products"].iloc[0]    
        active_products += 1
        customers.at[customers.customer_id == cus_id, "active_products"] = active_products
        customers = cls._convert_df_datatypes(customers)
        h.df_to_csv(customers, "1_Banking_System/data/Customers.csv") 
    

class BankAccount:
    '''
    Abstract class to create bank accounts in system. Parent class to SavingsAccount and CheckingAccount classes
    '''
 
    def __init__(self, customer_id):
        '''
        Initialize Bank Account object.
        Add bank account creation date.
       
        Args:
            owner_id (str): ID of bank account owner (customer)
            balance (float): Balance added when opening account
        
        Raises (TBD)

        '''
        self._customer_id, self._opening_date = customer_id, date.today()  

    @property
    def customer_id(self):
        '''Make attribute customer_id a read-only property'''
        return self._customer_id
    
    @property
    def opening_date(self):
        '''Make attribute opening_date a read-only property'''
        return self._opening_date
    
    @classmethod
    def trasaction(self, amount, transaction):
        '''
        Process amount to transact on Bank Account   
     
        Args:
            amount (int): Amount to transact
            transaction (int):
                1: deposit
                2: withdraw
        
        '''
        pass


class SavingsAccount(BankAccount):
    '''
    Subclass from BankAccount class to open a Savings Account.
    '''
    TOTAL_SAV_ACCTS = 0                                                                                 # Class Attribute to load total active savings accounts
    SAV_ID_COUNT = 0                                                                                    # Class Attribute to load savings account ID count

    def __init__(self, customer_id, balance):
        '''
        Initialize Savings Account object.
              
        Args:
            customer_id (str): ID of Savings Account owner (customer)
            balance (float): Balance added when opening account
        
        Raises (TBD)

          
        '''
        BankAccount.__init__(self, customer_id)
        
        if balance < 100:
            raise ValueError
        else:       
            self.increase_sav_accounts()                                                                    # Increase Savings Account and ID counters by one
            self._savings_acct_id, self._balance, self._status = SavingsAccount.SAV_ID_COUNT, balance, True
        
        savings_accts = h.csv_to_df("1_Banking_System/data/Savings_Accounts.csv")                           # Helper function to open and read csv into df               
        savings_accts = self.update_df(savings_accts)                                                       # Update df with new Savings Account object info
        savings_accts = self._convert_df_datatypes(savings_accts)                                           # Convert df data types
        h.df_to_csv(savings_accts, "1_Banking_System/data/Savings_Accounts.csv")                            # Helper function to save df back to csv 
        self.save_total_sav_accounts()                                                                      # Save total active savings accounts and ID count back to csv

        Customer.increase_active_products(customer_id)                                                      # Increase active products on customer by one

        logger.info(f"Savings Account #{self._savings_acct_id} with balance of ${self._balance} for Customer ID {self._customer_id} was added successfully")

    @property
    def savings_acct_id(self):
        '''Make attribute savings_acct_id a read-only property'''
        return self._savings_acct_id
    
    @property
    def balance(self):
        '''Make attribute balance a read-only property'''
        return self._balance
    
    @property
    def status(self):
        '''Make attribute status a read-only property'''
        return self._status

    @classmethod
    def evaluate_acct(cls, cus_id, condition): 
        '''
        Evaluates if customer already has a Savings Account opened
        
        Args:
            cus_id (int): Customer's ID to validate
            condition (int): Condition to check:
                1: Check if customer has an opened savings account
                2: Check if customer has no active savings account
                 
        Raises:            
            ValueError: Check if customer already has a Savings Account opened

        '''            
        
        savings_accts = h.csv_to_df("1_Banking_System/data/Savings_Accounts.csv")
        
        if condition == 1:
            if savings_accts[savings_accts["customer_id"] == cus_id]["active"].bool() == True:
                raise UpdateError
        
        if condition == 2:         
            
            if not cus_id in savings_accts.customer_id: 
                raise UpdateError
            
            if savings_accts[savings_accts["customer_id"] == cus_id]["active"].bool() == False:
                raise UpdateError

    @classmethod
    def increase_sav_accounts(cls):
        '''
        Get current total active savings accounts and current savings account ID count from csv file (cls_attr.csv) and increase by 1 when initiliazing new Savings Account object
                       
        '''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        SavingsAccount.TOTAL_SAV_ACCTS = cls_attr_df.at["TOTAL_SAV_ACCTS", 1]
        SavingsAccount.SAV_ID_COUNT = cls_attr_df.at["SAV_ID_COUNT", 1]
        SavingsAccount.TOTAL_SAV_ACCTS += 1
        SavingsAccount.SAV_ID_COUNT += 1
    
    def update_df(self, df):
        ''' Update Dataframe with new Savings Account object initialized'''

        i = SavingsAccount.SAV_ID_COUNT - 1
        
        df.at[i, "savings_acct_id"] = SavingsAccount.SAV_ID_COUNT
        df.at[i, "customer_id"] = self.customer_id
        df.at[i, "balance"] = self.balance
        df.at[i, "opening_date"] = self.opening_date
        df.at[i, "active"] = self.status

        return df

    @staticmethod
    def _convert_df_datatypes(df):
        ''' Convert Dataframe Data Types'''

        df["savings_acct_id"] = df["savings_acct_id"].astype('int')
        df["customer_id"] = df["customer_id"].astype('int')
        df["balance"] = df["balance"].astype('float')
        df["active"] = df["active"].astype('bool')

        return df

    @classmethod
    def save_total_sav_accounts(cls):
        '''Save Total Savings Accounts and ID count into csv file (cls_attr.csv)'''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        cls_attr_df.at["TOTAL_SAV_ACCTS", 1] = SavingsAccount.TOTAL_SAV_ACCTS
        cls_attr_df.at["SAV_ID_COUNT", 1] = SavingsAccount.SAV_ID_COUNT
        cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
    
    @classmethod
    def trasaction(cls, amount, transaction, cus_id):
        '''
        Process amount to transact on Savings Acount   
     
        Args:            
            amount (int): Amount to transact
            transaction (int):
                1: deposit
                2: withdraw
            cus_id (int): Owner of account
        
        '''
        BankAccount.trasaction(amount, transaction)
       
        savings_accts = h.csv_to_df("1_Banking_System/data/Savings_Accounts.csv")                      
        
        savings_acct_id = savings_accts.loc[savings_accts['customer_id'] == cus_id, "savings_acct_id"].iloc[0]
        init_balance = savings_accts.loc[savings_accts['customer_id'] == cus_id, "balance"].iloc[0]

        if transaction == 1:
            new_balance = init_balance + amount
            savings_accts.at[savings_accts.customer_id == cus_id, "balance"] = new_balance
            logger.info(f"Amount ${amount} was successfully deposited to Savings Account #{savings_acct_id}. New balance is: ${new_balance}")

        if transaction == 2:
            
            if init_balance < amount:
                raise UpdateError(init_balance)
            else:
                new_balance = init_balance - amount
                savings_accts.at[savings_accts.customer_id == cus_id, "balance"] = new_balance
                logger.info(f"Amount ${amount} was successfully withdrawn from Savings Account #{savings_acct_id}. New balance is: ${new_balance}")
        
        savings_accts = cls._convert_df_datatypes(savings_accts)
        h.df_to_csv(savings_accts, "1_Banking_System/data/Savings_Accounts.csv")
    
    @classmethod
    def close_acct(cls, cus_id):
        '''
        Close account and zero balance when customer is inactivated   
     
        Args:           
            cus_id (int): Owner of account
        
        '''       
        savings_accts = h.csv_to_df("1_Banking_System/data/Savings_Accounts.csv")
        savings_acct_id = savings_accts.loc[savings_accts['customer_id'] == cus_id, "savings_acct_id"].iloc[0]                     
        savings_accts.at[savings_accts.customer_id == cus_id, "balance"] = 0
        savings_accts.at[savings_accts.customer_id == cus_id, "active"] = False   
        savings_accts = cls._convert_df_datatypes(savings_accts)
        h.df_to_csv(savings_accts, "1_Banking_System/data/Savings_Accounts.csv")
        logger.info(f"Savings Account #{savings_acct_id} was zeroed and inactivated")
                

class CarLoan():
    '''
    Class to open a Car Loan.
    '''
    TOTAL_CAR_LOANS = 0                                                                                 # Class Attribute to load total active car loans
    CAR_ID_COUNT = 0                                                                                    # Class Attribute to load car loan ID count

    def __init__(self, customer_id, loan_amount, interest_rate, terms):
        '''
        Initialize Savings Account object.
              
        Args:
            customer_id (str): ID of Car Loan owner (customer)
            loan (float): Loan granted to customer
    
        '''
           
        self.increase_car_loans()                                                                           # Increase Car Loan and ID counters by one
        self._car_loan_id, self._customer_id, self._loan_amount, self._interest_rate, self._terms, self._opening_date, self._status = \
            CarLoan.CAR_ID_COUNT, customer_id, loan_amount, interest_rate, terms, date.today(), True
        self._balance = loan_amount * (1 + interest_rate)
        
        car_loans = h.csv_to_df("1_Banking_System/data/Car_Loans.csv")                                      # Helper function to open and read csv into df               
        car_loans = self.update_df(car_loans)                                                               # Update df with new Car Loan object info
        car_loans = self._convert_df_datatypes(car_loans)                                                   # Convert df data types
        h.df_to_csv(car_loans, "1_Banking_System/data/Car_Loans.csv")                                       # Helper function to save df back to csv 
        self.save_total_car_loans()                                                                         # Save total active car loans and ID count back to csv

        Customer.increase_active_products(customer_id)                                                      # Increase active products on customer by one

        logger.info(f"Car Loan #{self._car_loan_id} with approved amount of ${self._loan_amount} for Customer ID {self._customer_id} was added successfully")

    @property
    def car_loan_id(self):
        '''Make attribute car_loan_id a read-only property'''
        return self._car_loan_id
    
    @property
    def customer_id(self):
        '''Make attribute customer_id a read-only property'''
        return self._customer_id
    
    @property
    def loan_amount(self):
        '''Make attribute loan_amount a read-only property'''
        return self._loan_amount
    
    @property
    def interest_rate(self):
        '''Make attribute interest_rate a read-only property'''
        return self._interest_rate
    
    @property
    def terms(self):
        '''Make attribute terms a read-only property'''
        return self._terms
            
    @property
    def balance(self):
        '''Make attribute balance a read-only property'''
        return self._balance
    
    @property
    def opening_date(self):
        '''Make attribute opening_date a read-only property'''
        return self._opening_date
    
    @property
    def status(self):
        '''Make attribute status a read-only property'''
        return self._status

    @classmethod
    def evaluate_loan(cls, cus_id, condition): 
        '''
        Evaluates if customer already has a Car Loan opened
        
        Args:
            cus_id (int): Customer's ID to validate
            condition (int): Condition to check:
                1: Check if customer has an opened car loan
                2: Check if customer has no active car loan
                 
        Raises:            
            ValueError: Check if customer already has a Car Loan opened

        '''            
        
        car_loans = h.csv_to_df("1_Banking_System/data/Car_Loans.csv")
        
        if condition == 1:
            if car_loans[car_loans["customer_id"] == cus_id]["active"].bool() == True:
                raise UpdateError
        
        if condition == 2:
            if not cus_id in car_loans.customer_id:                
                raise UpdateError
            
            if car_loans[car_loans["customer_id"] == cus_id]["active"].bool() == False:                
                raise UpdateError

    @classmethod
    def increase_car_loans(cls):
        '''
        Get current total active car loans and current car loan ID count from csv file (cls_attr.csv) and increase by 1 when initiliazing new Car Loan object
                       
        '''
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        CarLoan.TOTAL_CAR_LOANS = cls_attr_df.at["TOTAL_CAR_LOANS", 1]
        CarLoan.CAR_ID_COUNT = cls_attr_df.at["CAR_ID_COUNT", 1]
        CarLoan.TOTAL_CAR_LOANS += 1
        CarLoan.CAR_ID_COUNT += 1
    
    def update_df(self, df):
        ''' Update Dataframe with new Car Loan object initialized'''

        i = CarLoan.CAR_ID_COUNT - 1
        
        df.at[i, "car_loan_id"] = CarLoan.CAR_ID_COUNT
        df.at[i, "customer_id"] = self.customer_id
        df.at[i, "loan_amount"] = self.loan_amount
        df.at[i, "interest_rate"] = self.interest_rate
        df.at[i, "terms"] = self.terms
        df.at[i, "balance"] = self.balance
        df.at[i, "opening_date"] = self.opening_date
        df.at[i, "active"] = self.status

        return df

    @staticmethod
    def _convert_df_datatypes(df):
        ''' Convert Dataframe Data Types'''

        df["car_loan_id"] = df["car_loan_id"].astype('int')
        df["customer_id"] = df["customer_id"].astype('int')
        df["loan_amount"] = df["loan_amount"].astype('float')
        df["interest_rate"] = df["interest_rate"].astype('float')
        df["terms"] = df["terms"].astype('int')
        df["balance"] = df["balance"].astype('float')
        df["active"] = df["active"].astype('bool')

        return df

    @classmethod
    def save_total_car_loans(cls):
        '''Save Total Car Loans and ID count into csv file (cls_attr.csv)'''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        cls_attr_df.at["TOTAL_CAR_LOANS", 1] = CarLoan.TOTAL_CAR_LOANS
        cls_attr_df.at["CAR_ID_COUNT", 1] = CarLoan.CAR_ID_COUNT
        cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
    
     
    @classmethod
    def trasaction(cls, amount, transaction, cus_id):
        '''
        Process amount to transact on Car Loan
     
        Args:            
            amount (int): Amount to transact
            transaction (int):
                1: payment
                2: TBD
            cus_id (int): Owner of account
        
        '''       

        car_loans = h.csv_to_df("1_Banking_System/data/Car_Loans.csv")                      
        
        car_loans_id = car_loans.loc[car_loans['customer_id'] == cus_id, "car_loans_id"].iloc[0]
        init_balance = car_loans.loc[car_loans['customer_id'] == cus_id, "balance"].iloc[0]
      
        if transaction == 1:
            if init_balance < amount:
                raise UpdateError(init_balance)
            else:
                new_balance = init_balance - amount
                car_loans.at[car_loans.customer_id == cus_id, "balance"] = new_balance
                logger.info(f"Amount ${amount} was successfully paid on Car Loan #{car_loans_id}. New balance is: ${new_balance}")

        if transaction == 2:
            
           pass
        
        car_loans = cls._convert_df_datatypes(car_loans)
        h.df_to_csv(car_loans, "1_Banking_System/data/Car_Loans.csv")



def menu():
    logger.info("      Main Menu      ")
    logger.info("---------------------")
    logger.info("[1] Employee Menu")
    logger.info("[2] Customer Menu")
    logger.info("[3] Services")
    logger.info("")
    logger.info("[0] Exit the Program")
    logger.info("")

def employee_menu():
    logger.info("   Employee Menu   ")
    logger.info('-------------------')
    logger.info("[1] Create Employee")
    logger.info("[2] Update Employee's Address")
    logger.info("[3] Update Employee's Phone Number")
    logger.info("[4] Remove Employee (inactivate)")
    logger.info("[5] Get Total Employess")
    logger.info("")
    logger.info("[0] Return to Main Menu")
    logger.info("")

def customer_menu():
    logger.info("   Customer Menu   ")
    logger.info('-------------------')
    logger.info("[1] Create Customer")
    logger.info("[2] Update Customer's Address")
    logger.info("[3] Update Customer's Phone Number")
    logger.info("[4] Remove Customer (inactivate)")
    logger.info("[5] Get Total Customers")
    logger.info("")
    logger.info("[0] Return to Main Menu")
    logger.info("")

def services_menu():
    logger.info("   Services Menu   ")
    logger.info('-------------------')
    logger.info("[1] Savings Accounts")
    logger.info("[2] Car Loans")
    logger.info("")
    logger.info("[0] Return to Main Menu")
    logger.info("")

def savings_menu():
    logger.info("   Savings Menu   ")
    logger.info('------------------')
    logger.info("[1] Open Savings Account")
    logger.info("[2] Deposit")
    logger.info("[3] Withdraw")
    logger.info("")
    logger.info("[0] Return to Main Menu")
    logger.info("")

def car_menu():
    logger.info("   Car Loans Menu   ")
    logger.info('--------------------')
    logger.info("[1] Open Car Loan")
    logger.info("[2] Payment")
    logger.info("")
    logger.info("[0] Return to Main Menu")
    logger.info("")
    



def create_employee():
        
    h.clear()
    
    first_name = h.catch_exception("Employee's first name", "needs to be least one character long", f1 = h.validate_input)
    h.clear()
    last_name = h.catch_exception("Employee's last name", "needs to be least one character long", f1 = h.validate_input)
    h.clear()
    address = h.catch_exception("Employee's address", "needs to be least one character long", f1 = h.validate_input)
    h.clear() 
    phone = h.catch_exception("Employee's phone number", "needs to be 10 number character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)
    h.clear()
    level = h.catch_exception("Employee's level", "is not valid. Valid employee levels are 1, 2, 3", f2 = h.validate_option, a2 = [1, 2, 3], dtype = "int")
    h.clear()                
    salary = h.catch_exception("Employee's salary", "must be a non-negative amount", f1 = h.validate_positive_n, dtype = "int")
    h.clear()
    
    new_employee = Employee([first_name, last_name, address, phone], [level, salary])   
    logger.info("")
    input("Press Enter to continue...")

def update_employee_address():
        
    h.clear()
    
    while True:
            
        try:                    
            employee_id = h.catch_exception("Employee's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Employee.evaluate_id(employee_id)
        except ValueError:                    
            logger.info(f"Employee ID {employee_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Employee ID doesn't exist")
        
        else:
            
            break

    h.clear()
    
    new_address = h.catch_exception("Employee's new address", "needs to be least one character long", f1 = h.validate_input)    
    Employee.update_address(employee_id, new_address)    
    logger.info("")
    input("Press Enter to continue...")

def update_employee_phone():
        
    h.clear()
    
    while True:
            
        try:                    
            employee_id = h.catch_exception("Employee's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Employee.evaluate_id(employee_id)
        except ValueError:                    
            logger.info(f"Employee ID {employee_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Employee ID doesn't exist") 
        else:
            break

    h.clear()
    
    new_phone = h.catch_exception("Employee's new phone number", "needs to be 10 number character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)    
    Employee.update_phone(employee_id, new_phone)    
    logger.info("")
    input("Press Enter to continue...")

def remove_employee():
    back_to_mmenu = False

    h.clear()
    
    while True:
            
        try:                    
            employee_id = h.catch_exception("Employee's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Employee.evaluate_id(employee_id, status=True)
        except ValueError:                    
            logger.info(f"Employee ID {employee_id} doesn't exist.")
            logger.info("")
            logger.error(f"Employee ID doesn't exist")
            input("Press Enter to go back to Main Menu...")
            back_to_mmenu= True
            break
        except UpdateError:                    
            logger.info(f"Employee ID {employee_id} is already inactive.")
            logger.info("")
            logger.error(f"Employee ID is already inactive")
            input("Press Enter to go back to Main Menu...")
            back_to_mmenu= True
            break
        else:
            break

    h.clear()
    
    if back_to_mmenu == False:
        Employee.inactivate_employee(employee_id)   
        logger.info("")
        input("Press Enter to continue...")

def print_total_employees():
        
    h.clear()  
    Employee.get_total_employees() 
    logger.info("")
    input("Press Enter to continue...")


def create_customer():
        
    h.clear()
    
    first_name = h.catch_exception("Customer's first name", "needs to be least one character long", f1 = h.validate_input)
    h.clear()
    last_name = h.catch_exception("Customer's last name", "needs to be least one character long", f1 = h.validate_input)
    h.clear()
    address = h.catch_exception("Customer's address", "needs to be least one character long", f1 = h.validate_input)
    h.clear() 
    phone = h.catch_exception("Customer's phone number", "needs to be 10 number character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)
    h.clear()
    
    month = h.catch_exception("Customer's birth month", "is not valid. Use format MM, with values between 01 and 12.", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 2, f3 = h.validate_month, format = " in MM format" )
    h.clear() 
    day = h.catch_exception("Customer's birth day", "is not valid. Use format DD, with a valid day for the corresponding month.", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 2, f3 = h.validate_day, a3 = month, format = " in DD format" )
    h.clear()
    year = h.catch_exception("Customer's birth year", "is not valid. Use format YYYY, with values between 1900 and 2005.", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 4, f3 = h.validate_year, format = " in YYYY format" )
    h.clear()
    date_birth = date(int(year), int(month), int(day))
    h.clear()
                    
    new_customer = Customer([first_name, last_name, address, phone], [date_birth])   
    logger.info("")
    input("Press Enter to continue...")

def update_customer_address():
        
    h.clear()
    
    while True:
            
        try:                    
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist")
        
        else:
            
            break

    h.clear()
    
    new_address = h.catch_exception("Customer's new address", "needs to be least one character long", f1 = h.validate_input)    
    Customer.update_address(customer_id, new_address)    
    logger.info("")
    input("Press Enter to continue...")

def update_customer_phone():
        
    h.clear()
    
    while True:
            
        try:                    
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist") 
        else:
            break

    h.clear()
    
    
    
    
    new_phone = h.catch_exception("Customer's new phone number", "needs to be 10 number character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)    
    Customer.update_phone(customer_id, new_phone)    
    logger.info("")
    input("Press Enter to continue...")

def remove_customer():
    back_to_mmenu = False
    h.clear()
    
    while True:
            
        try:                    
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive decimal value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id, status=True)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist")
            input("Press Enter to go back to Main Menu...")
            back_to_mmenu= True
            break
        except UpdateError:                    
            logger.info(f"Customer ID {customer_id} is already inactive.")
            logger.info("")
            logger.error(f"Customer ID is already inactive")
            input("Press Enter to go back to Main Menu...")
            back_to_mmenu= True
            break
        else:
            break

    h.clear()
    
    if back_to_mmenu == False:
        Customer.inactivate_customer(customer_id)
        SavingsAccount.close_acct(customer_id)
        logger.info("")
        input("Press Enter to continue...")

def print_total_customers():
        
    h.clear()  
    Customer.get_total_customers() 
    logger.info("")
    input("Press Enter to continue...")


def open_sav_acct():
    back_to_smenu = False
    f = False   
   
    h.clear()
    
    while True:
            
        try:                    
            if f == True:
                break
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id, status = True)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
        except UpdateError:                    
            logger.info(f"Customer ID {customer_id} is Inactive. Please try again.")
            logger.info("")
            logger.error(f"Customer ID is Inactive")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
      
        else:
            while True:
                
                try:                  
                    SavingsAccount.evaluate_acct(customer_id, 1)
                except ValueError:
                    f = True                    
                    break
                except UpdateError:                    
                    logger.info(f"Customer ID {customer_id} already has a Savings Account.")
                    logger.info("")
                    logger.error(f"Customer ID already has a Savings Account")
                    input("Press Enter to go back to Services Menu...")
                    back_to_smenu= True
                    f = True  
                    break
                else:
                    f = True 
                    break   

          
            
    if back_to_smenu == False:
        while True:
            
            try:                    
                balance = h.catch_exception("Opening Balance", "needs to be a positive amount", f1 = h.validate_decimals)
                SavingsAccount(customer_id, float(balance)) 
            except ValueError:                    
                logger.info(f"Minimum Balance is $100. Please try again.")
                logger.info("")
                logger.error(f"Minimum Balance is $100") 
            else:
                break    
        
        logger.info("")
        input("Press Enter to continue...")

def transaction_sav_acct(transaction):
    back_to_smenu = False
    f = False   
    
    if transaction == 1:
        message = 'Amount to deposit'
    if transaction == 2:
        message = 'Amount to withdraw'    
    
    h.clear()
    
    while True:
            
        try:                    
            if f == True:
                break
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id, status = True)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
        except UpdateError:                    
            logger.info(f"Customer ID {customer_id} is Inactive. Please try again.")
            logger.info("")
            logger.error(f"Customer ID is Inactive")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
      
        else:
            while True:
                
                try:                  
                    SavingsAccount.evaluate_acct(customer_id, 2)
                except ValueError:
                    f = True                    
                    break
                except UpdateError:                    
                    logger.info(f"Customer ID {customer_id} has no active Savings Account.")
                    logger.info("")
                    logger.error(f"Customer ID has no active Savings Account")
                    input("Press Enter to go back to Services Menu...")
                    back_to_smenu= True
                    f = True  
                    break
                else:
                    f = True 
                    break   

          
            
    if back_to_smenu == False:
        while True:
            try:              
                                   
                amount = h.catch_exception(message, "needs to be a positive amount", f1 = h.validate_decimals)
                SavingsAccount.trasaction(float(amount), transaction, customer_id)
            except UpdateError as e:
                    print()                    
                    logger.info(f"Amount to withdraw exceeds current balance: ${e.value}. Please try again.")
                    logger.info("")
                    logger.error(f"Amount to withdraw exceeds current balance") 
            else:
                break 

        logger.info("")
        input("Press Enter to continue...")


def open_car_loan():
    back_to_smenu = False
    f = False 
       
    h.clear()
    
    while True:
            
        try:                    
            if f == True:
                break
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id, status = True)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
        except UpdateError:                    
            logger.info(f"Customer ID {customer_id} is Inactive. Please try again.")
            logger.info("")
            logger.error(f"Customer ID is Inactive")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
      
        else:
            while True:
                
                try:                  
                    CarLoan.evaluate_loan(customer_id, 1)
                except ValueError:
                    f = True                    
                    break
                except UpdateError:                    
                    logger.info(f"Customer ID {customer_id} already has a Car Loan.")
                    logger.info("")
                    logger.error(f"Customer ID already has a Car Loan")
                    input("Press Enter to go back to Services Menu...")
                    back_to_smenu= True
                    f = True  
                    break
                else:
                    f = True 
                    break   
    
    if back_to_smenu == False:       
                              
        credit_score = h.catch_exception("Customer's credit score", "needs to between 600 and 800", f1 = h.validate_credit_score)
        Customer.update_credit_score(customer_id, credit_score)
        h.clear()
        loan_amount = h.catch_exception("Car loan amount", "needs to be a positive amount", f1 = h.validate_decimals)
        h.clear()
        interest_rate = h.catch_exception("Interest rate", "needs to be a decimal number from 0.05 to 0.5", f1 = h.validate_interest)
        h.clear()
        terms = h.catch_exception("Terms", "needs to be in months (12, 24, 48 or 60).", f1 = h.validate_terms, format = " in months (12, 24, 48 or 60)")
        CarLoan(customer_id, float(loan_amount), float(interest_rate), terms)             
        
        logger.info("")
        input("Press Enter to continue...")



def car_loan_payment(transaction):
    back_to_smenu = False
    f = False

    if transaction == 1:
        message = 'Amount to pay'
    if transaction == 2:
        pass  
       
    h.clear()
    
    while True:
            
        try:                    
            if f == True:
                break
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive number value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id, status = True)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
        except UpdateError:                    
            logger.info(f"Customer ID {customer_id} is Inactive. Please try again.")
            logger.info("")
            logger.error(f"Customer ID is Inactive")
            input("Press Enter to go back to Services Menu...")
            back_to_smenu= True
            break
      
        else:
            while True:
                
                try:                  
                    CarLoan.evaluate_loan(customer_id, 2)
                except ValueError:
                    f = True                    
                    break
                except UpdateError:                    
                    logger.info(f"Customer ID {customer_id} has no active Car Loan.")
                    logger.info("")
                    logger.error(f"Customer ID has no active Car Loan")
                    input("Press Enter to go back to Services Menu...")
                    back_to_smenu= True
                    f = True  
                    break
                else:
                    f = True 
                    break   

    if back_to_smenu == False:
        while True:
            try:              
                                   
                amount = h.catch_exception(message, "needs to be a positive amount", f1 = h.validate_decimals)
                CarLoan.trasaction(float(amount), transaction, customer_id)
            except UpdateError as e:
                    print()                    
                    logger.info(f"Amount to pay exceeds current balance: ${e.value}. Please try again.")
                    logger.info("")
                    logger.error(f"Amount to pay exceeds current balance") 
            else:
                break 

        logger.info("")
        input("Press Enter to continue...")

    h.clear()    


h.clear()
menu()
option = int(input("Enter your option: "))

while option != 0:
    
    if option == 1:
        h.clear()
        employee_menu()
        h.option_input_validation(employee_menu, option, options=5, m1=create_employee, m2=update_employee_address, m3=update_employee_phone, m4=remove_employee, m5=print_total_employees)             
              
    elif option == 2:
        h.clear()
        customer_menu()
        h.option_input_validation(customer_menu, option, options=5, m1=create_customer, m2=update_customer_address, m3=update_customer_phone, m4=remove_customer, m5=print_total_customers)

    elif option == 3:
        h.clear()
        services_menu()
        option = h.option_input_validation_main(services_menu, option, options=2, m1=savings_menu, m2=car_menu) 

        while option != 0:
        
            if option == 1:
                h.clear()
                savings_menu()
                h.option_input_validation(savings_menu, option, options=3, m1=open_sav_acct, m2=transaction_sav_acct, o2=1, m3=transaction_sav_acct, o3=2)
            
            if option == 2:
                h.clear()
                car_menu()
                h.option_input_validation(savings_menu, option, options=2, m1=open_car_loan, m2=car_loan_payment, o2=1)
            
            
            h.clear()
            services_menu()
            option = h.option_input_validation_main(services_menu, option, options=2, m1=savings_menu, m2=car_menu)    
    
    else:
        logger.info("Invalid option.")
    
    h.clear()
    menu()
    option = int(input("Enter your option: "))

h.clear()
logger.info("Thanks for using this program.")
logger.info("")


# script_time = round(time.time() - start_time, 2)              # Take time of execution
# print(f"Script took {script_time} seconds")