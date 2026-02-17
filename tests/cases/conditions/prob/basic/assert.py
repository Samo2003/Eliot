from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    passed = sum(e.has_response for e in stats.exchanges)
    prob = passed / 1000
    assert 0.45 <= prob <= 0.55
