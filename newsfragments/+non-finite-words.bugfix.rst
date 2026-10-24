``number_to_words`` now raises ``BadNumValueError`` for non-finite numbers such as ``float("inf")`` and ``float("nan")`` instead of returning "zero".
