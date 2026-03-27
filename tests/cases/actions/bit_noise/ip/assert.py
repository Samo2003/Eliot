from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses
    e_ipv4 = stats.exchanges[0]
    assert e_ipv4.received is not None
    diff = stats.bit_diff(e_ipv4.sent.raw, e_ipv4.received.raw)
    assert diff == [158, 159]
    e_ipv6 = stats.exchanges[1]
    assert e_ipv6.received is not None
    diff = stats.bit_diff(e_ipv6.sent.raw, e_ipv6.received.raw)
    assert diff == [318, 319]
    