from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.only_first_n_have_response(9)
    received = [recv.seq for recv in stats.received]
    assert received == [1, 0, 4, 3, 2, 8, 7, 6, 5]
    