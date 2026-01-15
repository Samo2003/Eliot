from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    for i, e in enumerate(stats.exchanges):
        if i in [0, 3, 4, 5, 6, 7, 8, 11]:
            assert e.has_response
        else:
            assert not e.has_response
