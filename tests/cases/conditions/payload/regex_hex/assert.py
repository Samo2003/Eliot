from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    print([e.has_response for e in stats.exchanges])
    assert stats.only_first_n_have_response(2)
