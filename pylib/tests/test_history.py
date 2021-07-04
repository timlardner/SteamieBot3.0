from post_components.history import History


def test_history():
    h = History()
    text = h.get_body()
    assert text
