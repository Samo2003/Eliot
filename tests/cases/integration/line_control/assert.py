from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert all(e.has_response for e in stats.exchanges[:10])

    # Control ACTIVE packet
    assert not stats.exchanges[10].has_response

    # ACTIVE State
    assert all(e.has_response for e in stats.exchanges[11:21])

    # Control DROP packet
    assert not stats.exchanges[21].has_response

    # DROP state
    assert all(not e.has_response for e in stats.exchanges[22:32])

    # Control ACTIVE packet
    assert not stats.exchanges[32].has_response

    # ACTIVE State
    assert all(e.has_response for e in stats.exchanges[33:43])

    # Control DELAY packet
    assert not stats.exchanges[43].has_response

    # DELAY State
    assert all(e.has_response for e in stats.exchanges[44:54])
    assert all(e.rtt and e.rtt > 0.1 for e in stats.exchanges[44:54])
