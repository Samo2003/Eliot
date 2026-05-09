from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses
    assert all(e.rtt and e.rtt >= 0.07 and e.rtt <= 0.13 for e in stats.exchanges)

    # No reordering
    sequences = [recv.seq for recv in stats.received if recv.seq]
    assert sequences == sorted(sequences)
    