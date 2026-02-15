import math
from typing import Tuple, List

# Source: https://www.jstatsoft.org/article/view/v005i08

N = 128

def generate_ziggurat_tables() -> Tuple[List[int], List[float], List[float]]:
    m1 = 2147483648.0
    dn = 3.442619855899
    tn = dn
    vn = 9.91256303526217e-3

    kn = [0] * N
    wn = [0.0] * N
    fn = [0.0] * N

    q = vn / math.exp(-0.5 * dn * dn)

    kn[0] = int((dn / q) * m1)
    kn[1] = 0

    wn[0] = q / m1
    wn[N - 1] = dn / m1

    fn[0] = 1.0
    fn[N - 1] = math.exp(-0.5 * dn * dn)

    for i in range(N - 2, 0, -1):
        dn = math.sqrt(-2.0 * math.log(vn / dn + math.exp(-0.5 * dn * dn)))
        kn[i + 1] = int((dn / tn) * m1)
        tn = dn
        fn[i] = math.exp(-0.5 * dn * dn)
        wn[i] = dn / m1

    return kn, wn, fn
