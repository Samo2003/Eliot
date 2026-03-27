from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses
    e = stats.exchanges[0]
    assert e.received is not None
    diff = stats.bit_diff(e.sent.raw, e.received.raw)
    bit_len = len(e.sent.raw) * 8
    assert diff == [bit_len - 34, bit_len - 33]
    