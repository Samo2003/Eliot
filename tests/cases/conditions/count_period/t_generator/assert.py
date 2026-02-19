from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    seq = [e.received.seq for e in stats.exchanges if e.received]
    assert seq == [4, 5, 6, 8, 9, 10]