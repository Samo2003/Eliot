from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    lost = sum(
        1 for e in stats.exchanges if not e.has_response
    )
    
    assert lost >= 2
    