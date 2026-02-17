from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    for i, e in enumerate(stats.exchanges):
        in_drop_phase = ((i // 3) % 2) == 0
        if in_drop_phase:
            assert not e.has_response
        else:
            assert e.has_response  