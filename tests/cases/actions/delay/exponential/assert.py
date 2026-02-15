from tests.stats import ExchangeStats
import statistics

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses()

    rtts = [e.rtt for e in stats.exchanges if e.rtt is not None]

    avg = statistics.mean(rtts)

    assert 0.08 <= avg <= 0.2, avg
