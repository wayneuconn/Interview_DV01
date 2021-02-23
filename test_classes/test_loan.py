"""
Purpose: This module contains loan test_classes
Updates: 2/23/2021   Create the module

Author:  Zhiyong Yan
Date:    2/23/2021
"""

import csv
import numpy as np
from loan.loans import Loan
from loan.loan_pool import Loan_pool
from factors.default_rate import default_rate
from factors.prepayment_rate import prepayment_rate


def test_loan():
    lp1 = Loan_pool()
    with open('loan_data.csv', 'r') as fp:
        reader = csv.reader(fp, delimiter=',')
        header = next(reader, None)  # skip first row
        for row in reader:
            loan_temp = Loan(
                _term=(int(row[2]) - int(row[0])) * 12,  # convert to month
                _rate=float(row[1]),
                _current_balance=float(row[5]),
                _loan_grade=row[3]
            )
            lp1.append(loan_temp)

    lp1.get_waterfall(0.4).to_csv('test_cash_schedule.csv')
