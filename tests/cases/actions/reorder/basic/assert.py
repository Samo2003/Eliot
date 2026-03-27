from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses
    received = [recv.seq for recv in stats.received]
    sent = [sent.seq for sent in stats.sent]
    assert sent == list(reversed(received))
    