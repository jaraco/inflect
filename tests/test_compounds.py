from nose.tools import eq_

import inflect

p = inflect.engine()


def test_compound_1():
    eq_(p.singular_noun("hello-out-there"), "hello-out-there")


def test_compound_2():
    eq_(p.singular_noun("hello out there"), "hello out there")


def test_compound_3():
    eq_(p.singular_noun("continue-to-operate"), "continue-to-operate")


def test_compound_4():
    eq_(p.singular_noun("case of diapers"), "case of diapers")


def test_unit_handling_degree():
    test_cases = {
        "degree celsius": "degrees celsius",
        # 'degree Celsius': 'degrees Celsius',
        "degree fahrenheit": "degrees fahrenheit",
        "degree rankine": "degrees rankine",
        "degree fahrenheit second": "degree fahrenheit seconds",
    }
    for singular, plural in test_cases.items():
        eq_(p.plural(singular), plural)


def test_unit_handling_fractional():
    test_cases = {
        "pound per square inch": "pounds per square inch",
        "metre per second": "metres per second",
        "kilometre per hour": "kilometres per hour",
        "cubic metre per second": "cubic metres per second",
        "dollar a year": "dollars a year",
        # Correct pluralization of denominator
        "foot per square second": "feet per square second",
        "mother-in-law per lifetime": "mothers-in-law per lifetime",
        "pound-force per square inch": "pounds-force per square inch",
    }
    for singular, plural in test_cases.items():
        eq_(p.plural(singular), plural)


def test_unit_handling_combined():
    test_cases = {
        # Heat transfer coefficient unit
        "watt per square meter degree celsius": "watts per square meter degree celsius",
        "degree celsius per hour": "degrees celsius per hour",
        "degree fahrenheit hour square foot per btuit inch": (
            "degree fahrenheit hour square feet per btuit inch"
        ),
        # 'degree Celsius per hour': 'degrees Celsius per hour',
        # 'degree Fahrenheit hour square foot per BtuIT inch':
        #   'degree Fahrenheit hour square feet per BtuIT inch'
    }
    for singular, plural in test_cases.items():
        eq_(p.plural(singular), plural)
