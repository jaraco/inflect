from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction

import pytest
from typeguard import TypeCheckError

import inflect


@pytest.mark.parametrize(
    ('delta', 'expected'),
    [
        (timedelta(minutes=-30), '00:30:00 before'),
        (5, '00:00:05 after'),
        (0, 'at'),
        (0.0, 'at'),
        (-0.0, 'at'),
        (timedelta(), 'at'),
        (-5, '00:00:05 before'),
        (timedelta(seconds=5), '00:00:05 after'),
        (59, '00:00:59 after'),
        (60, '00:01:00 after'),
        (3599, '00:59:59 after'),
        (3600, '01:00:00 after'),
        (86399, '23:59:59 after'),
        (86400, '24:00:00 after'),
        (timedelta(days=-2, seconds=1), '47:59:59 before'),
        (timedelta(days=5, seconds=3723), '121:02:03 after'),
        (0.125, '00:00:00.125000 after'),
        (-0.125, '00:00:00.125000 before'),
        (timedelta(microseconds=-1), '00:00:00.000001 before'),
        (59.999999, '00:00:59.999999 after'),
        (0.0000004, 'at'),
        (-0.0000004, 'at'),
        (0.0000005, 'at'),
        (-0.0000005, 'at'),
        (0.0000006, '00:00:00.000001 after'),
        (-0.0000006, '00:00:00.000001 before'),
        (timedelta(days=100_000, microseconds=1), '2400000:00:00.000001 after'),
        (timedelta.max, '23999999999:59:59.999999 after'),
        (timedelta.min, '23999999976:00:00 before'),
    ],
)
def test_date_diff(delta, expected):
    assert inflect.engine().date_diff(delta) == expected


@pytest.mark.parametrize(
    ('delta', 'magnitude', 'direction'),
    [
        (-1800, timedelta(minutes=30), 'before'),
        (timedelta(minutes=-30), timedelta(minutes=30), 'before'),
        (5, timedelta(seconds=5), 'after'),
        (-0.125, timedelta(microseconds=125_000), 'before'),
        (timedelta.max, timedelta.max, 'after'),
        (timedelta.min, -timedelta.min, 'before'),
    ],
)
def test_formatter_receives_positive_duration_once(delta, magnitude, direction):
    received = []

    def fmt(duration):
        received.append(duration)
        return 'custom duration'

    assert inflect.engine().date_diff(delta, fmt=fmt) == f'custom duration {direction}'
    assert received == [magnitude]
    assert isinstance(received[0], timedelta)


@pytest.mark.parametrize('delta', [0, -0.0, timedelta(), 0.0000004, -0.0000005])
def test_zero_does_not_call_formatter(delta):
    def unexpected(duration):
        pytest.fail('zero must not be formatted')

    assert inflect.engine().date_diff(delta, fmt=unexpected) == 'at'


def test_natural_language_formatter():
    engine = inflect.engine()

    def nice_time(duration):
        seconds = int(duration.total_seconds())
        unit, count = (
            ('minute', seconds // 60) if seconds % 60 == 0 else ('second', seconds)
        )
        return f'{engine.number_to_words(count)} {engine.plural(unit, count)}'

    assert (
        engine.date_diff(timedelta(minutes=-30), fmt=nice_time)
        == 'thirty minutes before'
    )
    assert engine.date_diff(5, fmt=nice_time) == 'five seconds after'
    assert engine.date_diff(1, fmt=nice_time) == 'one second after'
    assert engine.date_diff(0, fmt=nice_time) == 'at'


def test_falsey_formatter():
    class Formatter:
        def __bool__(self):
            return False

        def __call__(self, duration):
            assert duration == timedelta(seconds=5)
            return 'five seconds'

    assert inflect.engine().date_diff(-5, fmt=Formatter()) == 'five seconds before'


def test_formatter_error_propagates():
    failure = ValueError('formatter failed')

    def fmt(duration):
        raise failure

    with pytest.raises(ValueError) as error:
        inflect.engine().date_diff(5, fmt=fmt)
    assert error.value is failure


def test_formatter_must_return_text():
    with pytest.raises(TypeError):
        inflect.engine().date_diff(5, fmt=lambda duration: 5)


@pytest.mark.parametrize(
    'delta', ['5', None, datetime(2020, 1, 1), Decimal(5), Fraction(1, 2)]
)
def test_invalid_duration_type(delta):
    with pytest.raises(TypeCheckError):
        inflect.engine().date_diff(delta)


@pytest.mark.parametrize(
    ('delta', 'error'),
    [
        (float('nan'), ValueError),
        (float('inf'), OverflowError),
        (-float('inf'), OverflowError),
        (86400 * 1_000_000_000, OverflowError),
        (-86400 * 1_000_000_000, OverflowError),
    ],
)
def test_numeric_conversion_errors(delta, error):
    with pytest.raises(error):
        inflect.engine().date_diff(delta)
