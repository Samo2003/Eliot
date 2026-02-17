from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    seq = [e.has_response for e in stats.exchanges]

    i = 0
    n = len(seq)

    while i < n:
        drop_len = 0
        while i < n and seq[i] is False:
            drop_len += 1
            i += 1

        assert 1 <= drop_len <= 5, f"Drop phase length {drop_len} not in [1,5]"

        if i >= n:
            break

        finish_len = 0
        while i < n and seq[i] is True:
            finish_len += 1
            i += 1

        if i < n:
            assert finish_len == 3, f"Finish phase length {finish_len}, expected 3"
        else:
            assert 1 <= finish_len <= 3
