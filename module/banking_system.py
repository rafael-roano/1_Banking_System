from datetime import date
import pandas as pd
import helpers as h
import logging


import time
start_time = time.time()

class UpdateError(Exception): pass

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
            user_info_ser[0], user_info_ser[1],user_info_ser[2], user_info_ser[3],date.today()       
            
                                                                                                        
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
    

class BankAccount:
    '''
    Abstract class to create bank accounts in system. Parent class to SavingsAccount and CheckingAccount classes
    '''

    def __init__(self, owner_id, balance):
        '''
        Initialize Bank Account object.
        Add bank account creation date.
       
        
        Args:
            owner_id (str): ID of bank account owner (customer)
            balance (float): Balance added when opening account
        
        Raises (TBD)

        '''
        pass

    
    def deposit(self, amount):
        '''
        Deposit amount to bank account
                     
        Raises (TBD)

        '''
        pass

    def withdraw(self, amount):
        '''
        Withdraw amount from bank account
                     
        Raises (TBD)

        '''
        pass


class SavingsAccount(BankAccount):
    '''
    Subclass from BankAccount class to open a Savings Account.
    '''

    def __init__(self, owner_id, balance, apy):
        '''
        Initialize Savings Account object.
              
        
        Args:
            owner_id (str): ID of Saving Account owner (customer)
            balance (float): Balance added when opening account
            apy (float): annual yield approved
        
        Raises (TBD)

        '''
        pass

    
    def deposit_monthly_yield(self):
        '''
        Deposit monthly yield to Saving Account
                     
        Raises (TBD)

        '''
        pass


class CheckingAccount(BankAccount):
    '''
    Subclass from BankAccount class to open a Cheking Account.
    '''

    INSUF_FUNDS_FEE=30


    def __init__(self, owner_id, balance, atm_limit):
        '''
        Initialize Checking Account object.
              
        
        Args:
            owner_id (str): ID of Checking Account owner (customer)
            balance (float): Balance added when opening account
            atm_limit (float): Maximum amount that can be withdrawn per day through an ATM
        
        Raises (TBD)

        '''
        pass


    def withdraw(self, amount):
        '''
        Withdraw amount from Checking Account, validating that daily limit is not exceeded if trasaction was done via ATM.
                     
        Raises (TBD)

        '''
        pass
   
    
    def transact(self, amount):
        '''
        Purchase through debit card associated with Checking Account
                     
        Raises (TBD)

        '''
        pass


class Service:
    '''
    Abstract class to open a service in system. Parent class to CarLoan and CreditCard classes
    '''

    def __init__(self, owner_id):
        '''
        Initialize Service object.
        Add service opening date.
       
        
        Args:
            owner_id (str): ID of bank account owner (customer)
                    
        Raises (TBD)

        '''
        pass


class CarLoan(Service):
    '''
    Subclass from Service class to open a Car Loan.
    '''

    def __init__(self, owner_id, loan_amount, interest_rate, term):
        '''
        Initialize CarLoan object.
        Add service opening date.
       
        
        Args:
            owner_id (str): ID of bank account owner (customer)
            loan_amount (float): Amount loaned
            interest_rate (float): Interest rate approved for car loan
            term (str): Loan term approved for car loan

                    
        Raises (TBD)

        '''
        pass


    def deposit_monthly_payment(self, amount):
        '''
        Deposit monthly payment to loan
                     
        Raises (TBD)

        '''
        pass


class CreditCard(Service):
    '''
    Subclass from Service class to open a Credit Card.
    '''

    def __init__(self, owner_id, approved_credit, apr, annual_fee, due_date):
        '''
        Initialize CreditCard object.
        Add service opening date.
       
        
        Args:
            owner_id (str): ID of bank account owner (customer)
            approved_credit (float): Credit approved
            apr (float): Annual rate approved
            annual_fee (float): Annual fee
            due_date (str): Payment due date

                    
        Raises (TBD)

        '''
        pass


    def transact(self, amount):
        '''
        Purchase through credit card
                     
        Raises (TBD)

        '''
        pass

    def pay_balance(self, amount):
        '''
        Pay balance of credit card
                     
        Raises (TBD)

        '''
        pass

    def compute_apr(self, amount):
        '''
        Compute Annual Percentage Rate

        Raises (TBD)

        '''
        pass


def menu():
    logger.info("      Main Menu      ")
    logger.info("---------------------")
    logger.info("[1] Employee Menu")
    logger.info("[2] Customer Menu")
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


def create_employee():
        
    h.clear()
    
    first_name = h.catch_exception("Employee's first name", "needs to be least one character long", f1 = h.validate_input)
    h.clear()
    last_name = h.catch_exception("Employee's last name", "needs to be least one character long", f1 = h.validate_input)
    h.clear()
    address = h.catch_exception("Employee's address", "needs to be least one character long", f1 = h.validate_input)
    h.clear() 
    phone = h.catch_exception("Employee's phone number", "needs to be 10 decimal character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)
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
            employee_id = h.catch_exception("Employee's ID", "needs to be a positive decimal value", f1 = h.validate_positive_n, dtype = "int")
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
            employee_id = h.catch_exception("Employee's ID", "needs to be a positive decimal value", f1 = h.validate_positive_n, dtype = "int")
            Employee.evaluate_id(employee_id)
        except ValueError:                    
            logger.info(f"Employee ID {employee_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Employee ID doesn't exist") 
        else:
            break

    h.clear()
    
    new_phone = h.catch_exception("Employee's new phone number", "needs to be 10 decimal character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)    
    Employee.update_phone(employee_id, new_phone)    
    logger.info("")
    input("Press Enter to continue...")

def remove_employee():
    back_to_mmenu = False

    h.clear()
    
    while True:
            
        try:                    
            employee_id = h.catch_exception("Employee's ID", "needs to be a positive decimal value", f1 = h.validate_positive_n, dtype = "int")
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
    phone = h.catch_exception("Customer's phone number", "needs to be 10 decimal character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)
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
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive decimal value", f1 = h.validate_positive_n, dtype = "int")
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
            customer_id = h.catch_exception("Customer's ID", "needs to be a positive decimal value", f1 = h.validate_positive_n, dtype = "int")
            Customer.evaluate_id(customer_id)
        except ValueError:                    
            logger.info(f"Customer ID {customer_id} doesn't exist. Please try again.")
            logger.info("")
            logger.error(f"Customer ID doesn't exist") 
        else:
            break

    h.clear()
    
    new_phone = h.catch_exception("Customer's new phone number", "needs to be 10 decimal character long", f1 = h.validate_decimals, f2 = h.validate_len, a2 = 10)    
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
        logger.info("")
        input("Press Enter to continue...")

def print_total_customers():
        
    h.clear()  
    Customer.get_total_customers() 
    logger.info("")
    input("Press Enter to continue...")


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

