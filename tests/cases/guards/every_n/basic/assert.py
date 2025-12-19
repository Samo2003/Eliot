from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    lost = sum(
        1 for e in stats.exchanges if not e.has_response
    )

    expected = stats.sent_count // 3

    assert lost == expected, (
        f"Unexpected packet loss\n"
        f"sent={stats.sent_count}\n"
        f"lost={lost}\n"
        f"expected={expected}\n"
    )
    