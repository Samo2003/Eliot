from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses
    rtts = [e.rtt for e in stats.exchanges if e.rtt is not None]
    
    # Variable delays
    assert max(rtts) > min(rtts)

    # must be in range (approx)
    assert max(rtts) - min(rtts) > 0.02
