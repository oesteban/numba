from .support import testcase, main
import numbapro as numba
from numbapro import *
import numpy as np

def test(func, expect):
    N = 10
    A = np.empty(N, dtype=np.float32)
    A[...] = 2.5
    func(A)
    assert np.allclose(A, expect)

@testcase
def test_prange():
    @autojit
    def forward1(A):
        for i in numba.prange(10):
            A[i] = i

    @autojit
    def forward2(A):
        for i in numba.prange(1, 5):
            A[i] = i

    @autojit
    def forward3(A):
        for i in numba.prange(1, 8, 3):
            A[i] = i

    @autojit
    def backward1(A):
        for i in numba.prange(9, 2, -3):
            A[i] = i

    @autojit
    def backward2(A):
        for i in numba.prange(1, 5, -1):
            A[i] = i

    @autojit
    def empty_assign():
        i = 14
        for i in numba.prange(10, 4):
            pass
        return i

    @autojit
    def last_value():
        for i in numba.prange(10):
            pass
        return i

    test(forward1,
         [ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9.])
    test(forward2,
         [ 2.5,  1.,   2.,   3.,   4.,   2.5,  2.5,  2.5,  2.5,  2.5])
    test(forward3,
         [ 2.5,  1.,   2.5,  2.5,  4.,   2.5,  2.5,  7.,   2.5,  2.5])
    test(backward1,
         [ 2.5,  2.5,  2.5,  3.,   2.5,  2.5,  6.,   2.5,  2.5,  9. ])
    test(backward2,
         [ 2.5,  2.5,  2.5,  2.5,  2.5,  2.5,  2.5,  2.5,  2.5,  2.5])

    assert empty_assign() == 14
    assert last_value() == 9

if __name__ == '__main__':
    main()
