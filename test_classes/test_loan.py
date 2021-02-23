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


def test_loan_2():
    asset_1 = Loan(
        _term=206,
        _rate=5.19406 / 100,
        _current_balance=18463762
    )
    asset_2 = Loan(
        _term=208,
        _rate=5.19406 / 100,
        _current_balance=18463762
    )
    lp_1 = Loan_pool([asset_1, asset_2])
    lp_1.get_waterfall(default_rate.to_SMM(0.05), prepayment_rate.to_SMM(0.02), 0.4).to_csv('test_classes.csv')

    lp_2 = Loan_pool()
    for i in range(3000):
        lp_2.append(
            Loan(
                _term=int(np.random.rand() * 300),
                _rate=np.random.rand() * 0.1,
                _current_balance=np.random.rand() * 100000
            )
        )
    lp_2.get_waterfall(default_rate.to_SMM(0.0001), prepayment_rate.to_SMM(0.0001), 0.4).to_csv('test_3000_loans.csv')


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
