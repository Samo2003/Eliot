from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    for i, e in enumerate(stats.exchanges):
        if i in (2, 4, 5):
            assert not e.has_response
        else:
            assert e.has_response