from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses

    ratios: list[float] = []
    for e in stats.exchanges:
        assert e.received is not None
        diff = stats.bit_diff(e.sent.raw, e.received.raw)
        ratios.append(len(diff) / (len(e.sent.raw) * 8))

    avg = sum(ratios) / len(ratios)
    assert 0.15 <= avg <= 0.25
    