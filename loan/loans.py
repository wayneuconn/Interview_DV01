"""
Purpose: This module contains loan base class
Updates: 2/23/2021   Create the module

Author:  Zhiyong Yan
Date:    2/23/2021
"""

from dataclasses import dataclass
from factors.default_rate import default_rate
import logging


@dataclass
class Loan:
    _term: int  # remaining term in month
    _rate: float  # annual gross loan rate without percentage
    _current_balance: float  # current remaining principal balance
    _loan_grade: str
    _freq: int = 1  # Payment frequency in month per payment
    _defaulted: bool = False  # whether the loan is default or not

    # convert gross rate into SMM
    @property
    def rate_monthly(self) -> float:
        return self._rate / 12 * self._freq

    @property
    def default_rate(self) -> float:
        return default_rate.rate(self._loan_grade)

    # to confirm if the loan is matured
    def matured(self, period: int) -> bool:
        if period > self._term:
            logging.info(
                'period parameter {p} months is greater than term {t} months'.format(p=period, t=self._term))
            return True

    # equal payment amortization formula
    def equal_pmt_amt(self, period: int) -> float:
        if self._defaulted or self.matured(period):
            return 0
        rate_month = self._rate / 12 * self._freq
        pmt: float = self._current_balance * rate_month * (1 + rate_month) ** self._term / (
                (1 + rate_month) ** self._term - 1)
        return pmt

    # googled remaining balance formula
    def balance(self, period: int) -> float:
        if self._defaulted or self.matured(period):
            return 0
        else:
            return self._current_balance * (1 + self.rate_monthly) ** period - self.equal_pmt_amt(period) * (
                    ((1 + self.rate_monthly) ** period - 1) / self.rate_monthly)

    def interest_due(self, period: int) -> float:
        if self._defaulted or self.matured(period):
            return 0
        return self.balance(period - 1) * self.rate_monthly

    def principal_due(self, period: int) -> float:
        if self._defaulted or self.matured(period):
            return 0
        return self.equal_pmt_amt(period) - self.interest_due(period)