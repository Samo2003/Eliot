from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses()
    
    total_time = stats.received[-1].recv_time - stats.sent[0].send_time
    total_bytes = sum(len(r.raw) for r in stats.received)
    assert total_bytes / total_time <= 1050