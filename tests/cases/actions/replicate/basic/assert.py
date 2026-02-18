from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.received_count == 11
    expected = stats.received[0]
    for rec in stats.received:
        assert rec.raw == expected.raw
    