from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses
    assert all(e.rtt and 0.97 <= e.rtt <= 1.03 for e in stats.exchanges)
    