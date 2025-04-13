from .constants import TABLES_PATH
from ..tools.logger_utils import my_log
import os
import numpy as np
import pandas as pd


class AmortizationTable:
    """
    Defines an amortization table for a loan as well as methods
    to find when half of the payments have been made or when more
    of the mothly payments go towards principal instead of interes.

    Attributes:
    ---------------------------------------------------
        loan_type (str): title of the loan, i.e. Student loans, Car, Medical...
        loan_balance (float): amount borrowed
        interest_rate (float): annual interest rate
        num_months (int): duration of the loan in months
        monthly_payment (float): amount owed every pay month

    Methods:
    ---------------------------------------------------
        __init__: Constructor that creates attribute of interest for this
        application. Creates pd.DataFrame to create amortization table

        create_table: populates the amortization table with the payment number, 
        due date, Payment_amount, Principal_paid, Interest_paid and remaining
        balance fields.

        _payment_split: #Calculate the principal, interest and loan balance for 
        each payment

        save_table: checks if the folder reserved for amortization tables exist,
        creates it if needed. Saves the moartization table into csv file using the
        loan_type, loan_amount nd monthly_payment as the name of the file.

        more_principal: checks the amortization table for the number of months
        it will take for the monthly payment to contribute to the principal
        amount more so than for the interest

        halfway: checks the amortization table for the number of months
        it will take to pay off half of the amount borrowed

        update_payments: updates the amortization table if given a lump sum payment
        or an increase in the monthly payment
    """
    def __init__(self, loan_type:str, loan_balance:float, interest_rate:float, \
                num_months:int, monthly_payments:float) -> None:

        self.loan_type = loan_type
        self.loan_balance = float(loan_balance)
        self.interest_rate = float(interest_rate)
        self.num_months = int(num_months)
        self.monthly_payments = float(monthly_payments)
        self.amortization_df = pd.DataFrame()

        #Log new amortization table:
        self._log_amortization_table()

        self.create_table()


    def create_table(self):
        """Creates amortization table."""
        self.amortization_df["Pmt #"] = pd.Series(range(1, self.num_months+1))
        self.amortization_df["Due date"] = pd.Series(pd.date_range(pd.Timestamp.now().date(), freq='MS', \
                                periods=self.num_months, tz='US/Mountain', name="Due date"))
        self.amortization_df["Payment_amount"] = pd.Series(self.monthly_payments, \
                                                        index=np.arange(self.num_months))
        
        #Calculate the principal, interest and loan balance for each payment
        if "Principal_paid" not in self.amortization_df.columns:
            principal, interest, loan = self._payment_split()

            self.amortization_df["Principal_paid"] = pd.Series(principal,
                                                            index=np.arange(self.num_months))
            self.amortization_df["Interest_paid"] = pd.Series(interest,
                                                            index=np.arange(self.num_months))
            self.amortization_df["Remaining_balance"] = pd.Series(loan,
                                                            index=np.arange(self.num_months))
        
        try:
            #Update last payment:
            self.amortization_df.loc[-1, "Payment_amount"] = self.amortization_df.loc[-1, "Principal_paid"]
        except IndexError:
            pass
        except KeyError:
            pass

        #Save amortization table:
        self.save_table(self.amortization_df)
        
    
    def _payment_split(self):
        """Calculate the interest to be paid and the total amount to be paid."""
        #Data structures to store results:
        principal_list = []
        interest_list = []
        loan_list = []
        loan = self.loan_balance
        
        #Calculate principal, interest and loan balance for each payment
        while loan > self.monthly_payments:
            interest_list.append(round(loan*(self.interest_rate/1200),2))
            principal_list.append(round(self.monthly_payments - interest_list[-1], 2))
            loan = round(loan - principal_list[-1],2)
            loan_list.append(loan)
        
        #Calculate last payment
        interest_list.append(round(loan_list[-1] * (self.interest_rate/1200),2))
        principal_list.append(loan_list[-1] + interest_list[-1])
        loan_list.append(0)
        
        return principal_list, interest_list, loan_list


    def save_table(self, amort_table):
        """Saves amortization table."""
        if not os.path.exists(TABLES_PATH):
            os.makedirs(TABLES_PATH)

        self.amortization_df.to_csv(index=False,path_or_buf=\
            f"{TABLES_PATH}{self.loan_type}-{self.loan_balance}-{self.monthly_payments}.csv")
        
        return


    def more_principal(self):
        """
        Calculates the number of months it takes for monthly payments to contribute more
        torwards principal than interest
        """
        return self.amortization_df[self.amortization_df['Principal_paid'].\
                                gt(self.monthly_payments/2)].index[0] + 1


    def halfway(self):
        """Calculates the number of months it takes to pay half of the loan amount."""
        return self.amortization_df[self.amortization_df['Remaining_balance'].\
                                lt(self.loan_balance/2)].index[0] + 1


    def update_payments(self, lump_sum, extra_payment):
        """
        Updates the loan term, interest paid and total payment amount given a lump sum payment 
        and/or an increased monthly payment.
        """
        #Update loan_balance and monthly payments. Disregard exceptions with amounts given.
        try:
            self.loan_balance =  self.loan_balance - lump_sum
        except:
            pass

        try:
            self.monthly_payments = self.monthly_payments + extra_payment
        except:
            pass
        
        #Log updated amortization table:
        self._log_amortization_table("Updated ")
        
        #Calculate the number of months required to pay off debt:
        principal, interest, loan = self._payment_split()

        #Update num_months:
        self.num_months = len(principal)

        self.amortization_df["Principal_paid"] = pd.Series(principal,
                                                            index=np.arange(self.num_months))
        self.amortization_df["Interest_paid"] = pd.Series(interest,
                                                        index=np.arange(self.num_months))
        self.amortization_df["Remaining_balance"] = pd.Series(loan,
                                                        index=np.arange(self.num_months))

        #Reset the amortization dataframe:
        self.amortization_df = pd.DataFrame()
        #Recreate amortization dataframe with new payment strategy:
        self.create_table()

    def _log_amortization_table(self, update_text=""):
        """Logs creation of a new or updated amortization table."""
        my_log.info(f"{update_text}{self.loan_type} - Balance: {self.loan_balance} - " +\
                    f"Interest rate: {self.interest_rate} - Duration: {self.num_months} - " +\
                    f"Monthly Payments: {self.monthly_payments}")

