from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    # Before after
    assert all(not e.has_response for e in stats.exchanges[:4])

    # True phase
    assert all(e.has_response for e in stats.exchanges[4:6])

    # After duration phase
    assert all(not e.has_response for e in stats.exchanges[6:])
