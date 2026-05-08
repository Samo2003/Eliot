from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    passed = sum(e.has_response for e in stats.exchanges)
    prob = passed / 100
    assert 0.4 <= prob <= 0.6
