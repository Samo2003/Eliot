from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses()
    for e in stats.exchanges:
        assert e.received is not None
        diff = stats.bit_diff(e.sent.raw, e.received.raw)
        assert 0 < len(diff) <= 5
    