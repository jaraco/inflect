"""
Number-to-words data: ordinals, units, tens, and magnitude names.
"""

from __future__ import annotations

import re


# NUMERICAL INFLECTIONS

nth = {
    0: "th",
    1: "st",
    2: "nd",
    3: "rd",
    4: "th",
    5: "th",
    6: "th",
    7: "th",
    8: "th",
    9: "th",
    11: "th",
    12: "th",
    13: "th",
}
nth_suff = set(nth.values())

ordinal = dict(
    ty="tieth",
    one="first",
    two="second",
    three="third",
    five="fifth",
    eight="eighth",
    nine="ninth",
    twelve="twelfth",
)

ordinal_suff = re.compile(rf"({'|'.join(ordinal)})\Z")


# NUMBERS

unit = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
teen = [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
ten = [
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]
mill = [
    " ",
    " thousand",
    " million",
    " billion",
    " trillion",
    " quadrillion",
    " quintillion",
    " sextillion",
    " septillion",
    " octillion",
    " nonillion",
    " decillion",
]
