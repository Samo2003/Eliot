from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert not stats.exchanges[0].has_response
    assert all(s.has_response for s in stats.exchanges[1:4])
    assert all(not s.has_response for s in stats.exchanges[4:])
