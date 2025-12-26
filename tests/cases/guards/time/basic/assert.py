from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert not stats.exchanges[0].has_response
    assert stats.exchanges[1].has_response
    assert stats.exchanges[2].has_response
