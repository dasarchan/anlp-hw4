import pytest
from q_1317_convertIntegerToTheSumOfTwoNoZeroIntegers import Solution


@pytest.mark.parametrize("n, output", [(2, [1, 1]), (11, [2, 9])])
class TestSolution:
    def test_getNoZeroIntegers(self, n: int, output: List[int]):
        sc = Solution()
        assert (
            sc.getNoZeroIntegers(
                n,
            )
            == output
        )
