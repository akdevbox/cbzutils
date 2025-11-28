import cbzutils


def test_numname_sep():
    fn = cbzutils.sort_keys._split_into_str_num_components
    assert fn("abc") == ["abc"]
    assert fn("abc1234") == ["abc", 1234.0]
    assert fn("00123") == ["", 123.0]
    assert fn("134rf123qq") == ["", 134.0, "rf", 123.0, "qq"]


def test_namenum_sort():
    fn = cbzutils.sort_keys.key_namenum

    t1 = [
        "Abc Vol 1: New beginnings.cbz",
        "Abc Vol 2: Later.cbz",
        "Abc Vol 2.1.cbz",
        "Abc Vol 2.2: Fine evening.cbz",
        "Abc Vol 3.cbz",
        "Abc Vol 4.cbz",
        "Abc Vol 4.1 : Extra special.cbz",
        "Abc Vol 4.2.cbz",
    ]

    assert t1 == list(sorted(t1, key=fn))

    t2 = [
        "Abc Chap 0001.0.0.cbz",
        "Abc Chap 0002.cbz",
        "Abc Chap 0002.1.cbz",
        "Abc Chap 0002.1.0.cbz",
        "Abc Chap 0002.1.1.cbz",
        "Abc Chap 0002.2.cbz",
    ]

    assert t2 == list(sorted(t2, key=fn))
