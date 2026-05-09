from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    for i, e in enumerate(stats.exchanges):
        if i % 2 == 0:
            assert e.has_response
        else:
            assert not e.has_response

    total_time = stats.received[-1].recv_time - stats.sent[0].send_time
    total_bytes = sum(len(r.raw) for r in stats.received)
    assert total_bytes / total_time <= 500
