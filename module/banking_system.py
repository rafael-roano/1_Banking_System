from datetime import date
import pandas as pd
import helpers

import time
start_time = time.time()


class IncorrectLevel(Exception): pass
class IDInactive(Exception): pass



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
           
        
        Raises:
            TypeError: Check if series elements are string data type
        '''

        def evaluate_str_type(bool_ser_x):
            '''Evaluates if series elements are string data type'''
            
            
            if not bool_ser_x.all():                                                                    # Return True if all elements are True
                raise TypeError("User data has to be string type. Please try again.")

            else:            
                self._first_name, self._last_name, self._address, self._phone, self.creation_date = \
                    user_info_ser[0], user_info_ser[1],user_info_ser[2], user_info_ser[3],date.today()

        
        user_info_ser = pd.Series(user_info)                                                            # Create Pd ser from list argument
        bool_ser = user_info_ser.apply(lambda x: True if isinstance(x, str) else False)                 # Return boolean ser by applying lambda function to check if ser elements are str type 

        try:                                                                                            # Try-Except Block to check and handle Expcetion when arguments are not all str type
            evaluate_str_type(bool_ser)                                     

        except TypeError:
            print("User data has to be string type. Please try again.")
            raise SystemExit
            
                                                                                                        
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
    
    
    @classmethod
    def update_address(cls, address):
        '''
        Update user's address.
        
        Args:
            address (str): User's new address to assign to object.
             
        Raises:
            TypeError: Check if address is str data type.

        '''
        

        def evaluate_str_type(address):
            '''Evaluates if address is string data type'''
            
            if not isinstance(address, str):
                raise TypeError("Address has to be string type. Please try again.")
       
        try:                                                                                      
            evaluate_str_type(address)                                   

        except TypeError:
            print("Address has to be string type. Please try again.")
            raise SystemExit
            

    @classmethod
    def update_phone(cls, phone):
        '''
        Update user's phone number.
        
        Args:
            phone (str): User's new phone number to assign to object.
             
        Raises:
            TypeError: Check if phone number is str data type.

        '''
        
        def evaluate_str_type(phone):
            '''Evaluates if phone number is str data type'''
            
            if not isinstance(phone, str):
                raise TypeError("Phone number has to be string type. Please try again.")
       
        try:                                                                                      
            evaluate_str_type(phone)                                   

        except TypeError:
            print("Phone number has to be string type. Please try again.")
            raise SystemExit


    # @classmethod
    # def update_email(cls, email):
    #     '''
    #     Update user's email.
        
    #     Args:
    #         email (str): User's new email to assign to object.
             
    #     Raises:
    #         TypeError: Check if email is str data type.

    #     '''
        
    #     def evaluate_str_type(email):
    #         '''Evaluates if email is str data type'''
            
    #         if not isinstance(email, str):
    #             raise TypeError("Email has to be string type. Please try again.")
       
    #     try:                                                                                      
    #         evaluate_str_type(email)                                   

    #     except TypeError:
    #         print("Email has to be string type. Please try again.")
    #         raise SystemExit

    def compute_account_age(self):
        '''
        Compute User's account age.
        
        Returns:
            int
                  
        Raises (TBD)

        '''
        pass




class Employee(User):
    '''
    Subclass from User class to create Employee records.
    '''

    TOTAL_EMPLOYEES = 0                                                                                     # Class Attribute to load total employees
    EMPLOYEE_ID_COUNT = 0                                                                                   # Class Attribute to load employee ID count

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

        
        Raises (TBD)

        '''
        User.__init__(self, user_info)
        self.increase_total_employees()
        self.increase_employee_id()

        employee_info_ser = pd.Series(employee_info)                                                        # Create Pd ser from list argument
        bool_ser = employee_info_ser.apply(lambda x: True if isinstance(x, int) else False)                 # Return boolean ser by applying lambda function to check if ser elements are int type 
        
        if not pd.Series(bool_ser).all():                                                                   # Return True if all elements are True
            
            raise TypeError("Employee data has to be an integer!!")

        elif not employee_info_ser[0] in (1,2,3):
            raise IncorrectLevel("Level must be: 1, 2 or 3")
        
        elif employee_info_ser[1] < 0:
            raise ValueError("Employee salary has to be non-negative!!")

        else:            
            self.employee_id, self.level, self.salary, self.status = \
                Employee.EMPLOYEE_ID_COUNT, employee_info_ser[0], employee_info_ser[1], True
               
        
        employees = helpers.csv_to_df("1_Banking_System/data/Employees.csv")                                # Call helper function to open and read csv into df               
        employees = self.update_df(employees)
        employees = self._convert_df_datatypes(employees)
        helpers.df_to_csv(employees, "1_Banking_System/data/Employees.csv")                                 # Call helper function to save df back to csv 
        self.save_total_employees()                                                                         # Save total employees and ID count back to csv

        print(f"Employee ID {self.employee_id} was added successfully")
        print(employees.head(10))
        print(f"Total Employees: {Employee.TOTAL_EMPLOYEES}")
        print(f"Total ID's: {Employee.EMPLOYEE_ID_COUNT}")   
        # print(employees.dtypes)     


    @classmethod
    def update_address(cls, address, employee_id):
        '''
        Update employee's address.
        
        Args:
            address (str): Employee's new address.
            employee_id (int): Employee's ID to update address.

             
        Raises:
            TypeError: Check if employee_id is Int.
            ValueError: Check if employee_id exists.

        '''

        User.update_address(address)

        def evaluate_id(idx, address): 
            '''Evaluates if Employee_id is valid'''

            employees = helpers.csv_to_df("1_Banking_System/data/Employees.csv")
            cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
            Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]

            if isinstance(idx, bool):
                raise TypeError("ID must be an integer")
            
            if not isinstance(idx, int):
                raise TypeError("ID must be an integer")

            if (idx < 1) or (idx > Employee.EMPLOYEE_ID_COUNT):
                raise ValueError("Employee ID doesn't exist. Please try again.")
            
            else:
                
                employees.at[employees.employee_id == idx, "address"] = address
                employees = cls._convert_df_datatypes(employees)
                helpers.df_to_csv(employees, "1_Banking_System/data/Employees.csv")
                        
                print(f"Employee ID {idx}'s address was updated to {address}")
                print(employees.head(10)) 
                   

        try:
            evaluate_id(employee_id, address)

        except TypeError:
            print("ID must be an integer")
        except ValueError:
            print(f"Employee ID {employee_id} doesn't exist. Please try again.")

    
    @classmethod
    def update_phone(cls, phone, employee_id):
        '''
        Update employee's phone number.
        
        Args:
            phone (str): Employee's new phone number.
            employee_id (int): Employee's ID to update phone number.

             
        Raises:
            TypeError: Check if employee_id is Int.
            ValueError: Check if employee_id exists.

        '''

        User.update_phone(phone)

        def evaluate_id(idx, phone): 
            '''Evaluates if Employee_id is valid'''

            employees = helpers.csv_to_df("1_Banking_System/data/Employees.csv")
            cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
            Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]

            if isinstance(idx, bool):
                raise TypeError("ID must be an integer")
            
            if not isinstance(idx, int):
                raise TypeError("ID must be an integer")

            if (idx < 1) or (idx > Employee.EMPLOYEE_ID_COUNT):
                raise ValueError("Employee ID doesn't exist. Please try again.")
            
            else:
                
                employees.at[employees.employee_id == idx, "phone"] = phone
                employees = cls._convert_df_datatypes(employees)
                helpers.df_to_csv(employees, "1_Banking_System/data/Employees.csv")
                        
                print(f"Employee ID {idx}'s phone number was updated to {phone}")
                print(employees.head(10)) 
                   

        try:
            evaluate_id(employee_id, phone)

        except TypeError:
            print("ID must be an integer")
        except ValueError:
            print(f"Employee ID {employee_id} doesn't exist. Please try again.")


    # @classmethod
    # def update_email(cls, email, employee_id):
    #     '''
    #     Update employee's email.
        
    #     Args:
    #         email (str): Employee's new email.
    #         employee_id (int): Employee's ID to update email.

             
    #     Raises:
    #         TypeError: Check if employee_id is Int.
    #         ValueError: Check if employee_id exists.

    #     '''

    #     User.update_email(email)

    #     def evaluate_id(idx, email): 
    #         '''Evaluates if Employee_id is valid'''

    #         employees = helpers.csv_to_df("1_Banking_System/data/Employees.csv")
    #         cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
    #         Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]

    #         if isinstance(idx, bool):
    #             raise TypeError("ID must be an integer")
            
    #         if not isinstance(idx, int):
    #             raise TypeError("ID must be an integer")

    #         if (idx < 1) or (idx > Employee.EMPLOYEE_ID_COUNT):
    #             raise ValueError("Employee ID doesn't exist. Please try again.")
            
    #         else:
                
    #             employees.at[employees.employee_id == idx, "email"] = email
    #             employees = cls._convert_df_datatypes(employees)
    #             helpers.df_to_csv(employees, "1_Banking_System/data/Employees.csv")
                        
    #             print(f"Employee ID {idx}'s phone number was updated to {email}")
    #             print(employees.head(10)) 
                   

    #     try:
    #         evaluate_id(employee_id, email)

    #     except TypeError:
    #         print("ID must be an integer")
    #     except ValueError:
    #         print(f"Employee ID {employee_id} doesn't exist. Please try again.")


    @classmethod
    def increase_total_employees(cls):
        '''
        Get current total employees quantity from csv file (cls_attr.csv) and increase by 1 when initiliazing new Employee object
                       
        '''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.TOTAL_EMPLOYEES = cls_attr_df.at["TOTAL_EMPLOYEES", 1]
        Employee.TOTAL_EMPLOYEES += 1
        

    @classmethod
    def increase_employee_id(cls):
        '''
        Get current ID count from csv file (cls_attr.csv) and increase by 1 when initiliazing new Employee object

        Returns:
            int
        
        '''
        
        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]
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
        df["phone"] = df["phone"].astype('str')
        df["salary"] = df["salary"].astype('int')
        df["level"] = df["level"].astype('int')
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
    def inactivate_employee(cls, id):
        '''
        Inactivate employee
                                
        Raises (TBD)

        '''
        
        def evaluate_exception(idx):              
            employees = helpers.csv_to_df("1_Banking_System/data/Employees.csv")
            cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
            Employee.TOTAL_EMPLOYEES = cls_attr_df.at["TOTAL_EMPLOYEES", 1]
            Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]


            if isinstance(idx, bool):
                raise TypeError("ID must be an integer")
            
            if not isinstance(idx, int):
                raise TypeError("ID must be an integer")

            if (idx < 1) or (idx > Employee.EMPLOYEE_ID_COUNT):
                raise ValueError("Employee ID doesn't exist. Please try again.")
            
            if employees[employees["employee_id"] == idx]["active"].bool() == False:

                raise IDInactive("Employee is already inactive")

            else:
                employees.at[employees.employee_id == idx, "active"] = False
                
                employees = cls._convert_df_datatypes(employees)
                helpers.df_to_csv(employees, "1_Banking_System/data/Employees.csv")
                                         
                Employee.TOTAL_EMPLOYEES -= 1
                cls_attr_df.at["TOTAL_EMPLOYEES", 1] = Employee.TOTAL_EMPLOYEES
                cls_attr_df.to_csv("1_Banking_System/data/cls_attr.csv", header=False)
        
                print(f"Employee ID {idx} was inactivated")
                print(employees.head(10)) 
                print(f"Total Employees: {Employee.TOTAL_EMPLOYEES}")
                print(f"Total ID's: {Employee.EMPLOYEE_ID_COUNT}")       

        try:
            evaluate_exception(id)

        except TypeError:
            print("ID must be an integer")
        except ValueError:
            print(f"Employee ID {id} doesn't exist. Please try again.")
        except IDInactive:
            print(f"Employee ID {id} is already inactive")


    @classmethod
    def get_total_employees(cls):
        '''
        Get total employees.
        
        Returns:
            str
                  
        '''

        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.TOTAL_EMPLOYEES = cls_attr_df.at["TOTAL_EMPLOYEES", 1]
                
        return f"Total Employees: {Employee.TOTAL_EMPLOYEES}"

    @classmethod
    def get_total_ids(cls):
        '''
        Get total IDs.
        
        Returns:
            str
                  
        '''

        cls_attr_df = pd.read_csv("1_Banking_System/data/cls_attr.csv", header=None, index_col=0)
        Employee.EMPLOYEE_ID_COUNT = cls_attr_df.at["EMPLOYEE_ID_COUNT", 1]
                
        return f"Total ID's: {Employee.EMPLOYEE_ID_COUNT}"


    

# Employee.update_email('@', 10)

# for i in range(100):

#     e0 = Employee(['Rafael', 'Roano', 'Cataratas Niagara 163', '5564735'], [1, 10])



# e0 = Employee(['Rafael', 'Roano', '7777 15 St, SD', '7'], ['t', 10])
# e1 = Employee(['Raquel', 'Martinez', '2569 Bancroft St, SD, CA, 92104', '5564735'], [1, 15])
# e2 = Employee(['Elliot', 'Roano', 'Cataratas Niagara 163', '5564735'], [2, 100000])
# e4 = Employee(['Santino', 'Mertinez', 'Los Pinos', '202002'], [3, 1000000])

# Employee.inactivate_employee()

# print(e0.first_name)
# e0.first_name = 'Jack'
# print(e0.first_name)



# def menu():
#     print("[1] Create User")
#     print("[0] Exit the program")

# menu()
# option = int(input("Enter your option: "))

# while option != 0:
#     if option == 1:
#         print("Option 1 Selected.")
    
#     else:
#         print("Invalid option.")
    
#     print()
#     menu()
#     option = int(input("Enter your option: "))

# print("Thanks for using this program. Bye!!")



class Customer(User):
    '''
    Subclass from User class to create Customer records.
    '''

    TOTAL_CUSTOMERS = 0

    def __init__(self, first_name, last_name, address, phone, date_birth, credit_score=None):
        '''
        Initialize Customer object.
                
        Args:
            first_name (str): Customer's first name to assign to object.
            last_name (str): Customer's last name to assign to object.
            address (str): Customer's address to assign to object.
            phone (str): Customer's phone number to assign to object.
            date_birth (str): Customer's date of birth to assign to object.
            credit_score (int, optional): Customer's credit score. Default=None
            

        
        Raises (TBD)

        '''
        
        # User.__init__(self, first_name, last_name, address, phone, date_birth)
        # self.customer_id
        # self.credit_score = credit_score
        # self.active_products = active_products
        # increase TOTAL_CUSTOMERS by one

        pass


    def __del__(self):
        '''
        Deletes customer record
                                
        Raises (TBD)

        '''
        # TOTAL_CUSTOMERS -= 1
        # print("was deleted...")

        pass


    @classmethod
    def get_total_customers(cls):
        '''
        Get total customers.
        
        Returns:
            int
                  
        Raises (TBD)

        '''
        pass



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

script_time = round(time.time() - start_time, 2)
print(f"Script took {script_time} seconds")

       