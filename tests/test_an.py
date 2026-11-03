import inflect


def test_an():
    p = inflect.engine()

    assert p.an("cat") == "a cat"
    assert p.an("ant") == "an ant"
    assert p.an("a") == "an a"
    assert p.an("b") == "a b"
    assert p.an("honest cat") == "an honest cat"
    assert p.an("dishonest cat") == "a dishonest cat"
    assert p.an("Honolulu sunset") == "a Honolulu sunset"
    assert p.an("mpeg") == "an mpeg"
    assert p.an("onetime holiday") == "a onetime holiday"
    assert p.an("Ugandan person") == "a Ugandan person"
    assert p.an("Ukrainian person") == "a Ukrainian person"
    assert p.an("Unabomber") == "a Unabomber"
    assert p.an("unanimous decision") == "a unanimous decision"
    assert p.an("US farmer") == "a US farmer"
    assert p.an("wild PIKACHU appeared") == "a wild PIKACHU appeared"


def test_an_abbreviation():
    p = inflect.engine()

    assert p.an("YAML code block") == "a YAML code block"
    assert p.an("Core ML function") == "a Core ML function"
    assert p.an("JSON code block") == "a JSON code block"


def test_an_digits():
    p = inflect.engine()

    assert p.an("8") == "an 8"
    assert p.an("80 year old") == "an 80 year old"
    assert p.an("8th") == "an 8th"
    assert p.an("11") == "an 11"
    assert p.an("18th") == "an 18th"
    assert p.an("11,000 strong crowd") == "an 11,000 strong crowd"
    assert p.an("18000") == "an 18000"
    assert p.an("11.5") == "an 11.5"
    assert p.an("1 off") == "a 1 off"
    assert p.an("110") == "a 110"
    assert p.an("1100") == "a 1100"
    assert p.an("118") == "a 118"
    assert p.an("2") == "a 2"
