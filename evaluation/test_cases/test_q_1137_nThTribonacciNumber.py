import pytest
from q_1137_nThTribonacciNumber import Solution


@pytest.mark.parametrize("n, output", [(4, 4), (25, 1389537)])
class TestSolution:
    def test_tribonacci(self, n: int, output: int):
        sc = Solution()
        assert (
            sc.tribonacci(
                n,
            )
            == output
        )
