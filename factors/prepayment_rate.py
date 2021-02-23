"""
Purpose: This module contains prepayment rate class
Updates: 2/23/2021   Create the module

Author:  Zhiyong Yan
Date:    2/23/2021
"""

from dataclasses import dataclass


@dataclass
class prepayment_rate:
    _CPR:float

    @staticmethod
    def to_SMM(CPR:float)->float:
        return 1 - (1 - CPR) ** (1 / 12)

    @property
    def SMM(self):
        return self.to_SMM(self._CPR)

    @staticmethod
    def rate():
        return 0.00002