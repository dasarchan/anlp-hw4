import pytest
from q_1131_maximumOfAbsoluteValueExpression import Solution


@pytest.mark.parametrize(
    "arr1, arr2, output",
    [([1, 2, 3, 4], [-1, 4, 5, 6], 13), ([1, -2, -5, 0, 10], [0, -2, -1, -7, -4], 20)],
)
class TestSolution:
    def test_maxAbsValExpr(self, arr1: List[int], arr2: List[int], output: int):
        sc = Solution()
        assert (
            sc.maxAbsValExpr(
                arr1,
                arr2,
            )
            == output
        )
