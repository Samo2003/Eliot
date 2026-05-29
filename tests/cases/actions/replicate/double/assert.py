from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.received_count == 72, stats.received_count
    