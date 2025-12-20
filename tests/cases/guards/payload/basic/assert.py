from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert all(e.has_response for e in stats.exchanges[:4])

    assert all(not e.has_response for e in stats.exchanges[4:])
