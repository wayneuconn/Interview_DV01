"""
Purpose: This module contains default rate class
Updates: 2/23/2021   Create the module

Author:  Zhiyong Yan
Date:    2/23/2021
"""

from dataclasses import dataclass


@dataclass
class default_rate:
    _CDR: float

    @staticmethod
    def to_SMM(CDR: float) -> float:
        return 1 - (1 - CDR) ** (1 / 12)

    @staticmethod
    def rate(rating: str) -> float:
        if rating == "LC-A":
            return 0.0001

        elif rating == "LC-B":
            return 0.0002

        elif rating == "LC-C":
            return 0.0003

        elif rating == "LC-D":
            return 0.0004

        elif rating == "LC-E":
            return 0.0005

        elif rating == "LC-F":
            return 0.0006

        elif rating == "LC-G":
            return 0.0007
