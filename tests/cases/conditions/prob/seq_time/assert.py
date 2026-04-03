from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    responses = [e.has_response for e in stats.exchanges]

    n = len(responses) // 2
    start = responses[:n]
    end = responses[n:]

    start_ok = sum(start)
    end_ok = sum(end)

    assert start_ok < end_ok
