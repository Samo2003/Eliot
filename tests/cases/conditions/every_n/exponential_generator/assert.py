from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    intervals: list[int] = []
    last_drop = 0
    counter = 0

    for e in stats.exchanges:
        counter += 1
        if not e.has_response:
            intervals.append(counter - last_drop)
            last_drop = counter
    
    assert intervals.count(2) > intervals.count(6)

    avg_interval = sum(intervals) / len(intervals)
    assert 3.0 <= avg_interval <= 5.0