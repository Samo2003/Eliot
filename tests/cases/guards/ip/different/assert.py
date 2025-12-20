from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    for i, e in enumerate(stats.exchanges):
        if i == 0:
            assert not e.has_response
        else:
            assert e.has_response
