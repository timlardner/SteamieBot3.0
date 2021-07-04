from post_components.travel import TravelInfo


def test_travel():
    ti = TravelInfo()
    text = ti.get_body()
    assert text
