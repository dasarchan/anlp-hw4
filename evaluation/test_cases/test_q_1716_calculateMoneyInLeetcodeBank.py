import pytest
from q_1716_calculateMoneyInLeetcodeBank import Solution


@pytest.mark.parametrize("n, output", [(4, 10), (10, 37), (20, 96)])
class TestSolution:
    def test_totalMoney(self, n: int, output: int):
        sc = Solution()
        assert (
            sc.totalMoney(
                n,
            )
            == output
        )
