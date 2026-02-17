from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.only_first_n_have_response(5)
