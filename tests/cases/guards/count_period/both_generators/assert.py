from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    seq = [e.has_response for e in stats.exchanges]
    n = len(seq)

    i = 0
    finish_phase_index = 0

    while i < n:
        drop_len = 0
        while i < n and seq[i] is False:
            drop_len += 1
            i += 1

        assert 1 <= drop_len <= 5, (
            f"Drop phase length {drop_len} not in [1,5]"
        )

        if i >= n:
            break

        finish_len = 0
        while i < n and seq[i] is True:
            finish_len += 1
            i += 1

        expected_f = 2 * (finish_phase_index + 1)

        if i < n:
            assert finish_len == expected_f, (
                f"Finish phase {finish_phase_index}: "
                f"length {finish_len}, expected {expected_f}"
            )
        else:
            assert 1 <= finish_len <= expected_f, (
                f"Finish phase {finish_phase_index}: "
                f"length {finish_len}, expected ≤ {expected_f}"
            )

        finish_phase_index += 1
