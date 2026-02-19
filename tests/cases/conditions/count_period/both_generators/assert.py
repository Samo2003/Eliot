from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    seq = [e.received.seq for e in stats.exchanges if e.received]
    assert seq == [4, 6, 7, 8, 14, 15, 16, 17, 18]
