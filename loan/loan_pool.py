"""
Purpose: This module contains loan_pool base class
Updates: 2/23/2021   Create the module

Author:  Zhiyong Yan
Date:    2/23/2021
"""

from dataclasses import dataclass
from typing import List
from loan.loans import Loan
from factors.prepayment_rate import prepayment_rate
import numpy as np
import pandas as pd


@dataclass
class Loan_pool:
    _loan_list: List[Loan]  # list of loan

    def __init__(self, loan_list=None):
        self._loan_list = loan_list

    @property
    def max_term(self):
        return max(loan._term for loan in self._loan_list)

    def append(self, loan: Loan):
        if self._loan_list == None:
            self._loan_list = []
        self._loan_list.append(loan)

    def get_waterfall(self, recovery_rate: float):
        """
        A double loop function, through period and loans
        generate random number to decide if loan is defaulted/prepaid or not
        if default:
            loan._isdefault = True
            balance(t) = 0
            cash_flow += balance(t-1) * recovery_rate
            defaulted_cash_flow += balance(t-1) * (1- recovery_rate)
        if prepaid:
            loan._isdefault = True
            balance(t) = 0
            cash_flow += balanc(t-1) + payment

        :param recovery_rate: assume fixed recovery rate, immediate recovery
        :param default_rate: assume fixed default rate
        :param prepay_rate: assume fixed prepayment rate, full amount prepay
        :return: a pandas dataframe
        """
        output = []
        # for period in range(1, self.max_term + 1):
        for period in range(1, 5):
            print(period)
            cash_flow_t = 0
            default_amount_t = 0
            prepaid_amount_t = 0
            interest_due_t = 0
            principal_due_t = 0
            balance_t = 0

            for loan in self._loan_list:
                default_amount_i = 0
                prepaid_amount_i = 0
                interest_due_t += loan.interest_due(period)
                principal_due_t += loan.principal_due(period)
                if loan._defaulted:
                    continue

                payment_t = loan.equal_pmt_amt(period)
                cash_flow_i = payment_t

                # check default:
                if np.random.rand() < loan.default_rate:
                    cash_flow_i += loan.balance(period) * recovery_rate
                    default_amount_i = loan.balance(period) * (1 - recovery_rate)
                    interest_due_t -= loan.interest_due(period) * (1 - recovery_rate)
                    principal_due_t -= loan.principal_due(period) * (1 - recovery_rate)
                    loan._defaulted = True

                # check prepayment
                elif np.random.rand() < prepayment_rate.rate():
                    cash_flow_i += loan.balance(period) + payment_t
                    prepaid_amount_i = loan.balance(period) + payment_t
                    loan._defaulted = True

                cash_flow_t += cash_flow_i
                default_amount_t += default_amount_i
                prepaid_amount_t += prepaid_amount_i
                balance_t += loan.balance(period)
            output.append([cash_flow_t, default_amount_t, prepaid_amount_t, interest_due_t, principal_due_t, balance_t])
        res = pd.DataFrame(output)
        res.columns = ["Cash Flow", "Default Amount", "Prepaid Amount", "Interest_Due", "Principal Due", "EOP Balance"]
        return res
