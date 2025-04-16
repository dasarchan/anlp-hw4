import pytest
from q_0728_selfDividingNumbers import Solution


@pytest.mark.parametrize(
    "left, right, output",
    [(1, 22, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]), (47, 85, [48, 55, 66, 77])],
)
class TestSolution:
    def test_selfDividingNumbers(self, left: int, right: int, output: List[int]):
        sc = Solution()
        assert (
            sc.selfDividingNumbers(
                left,
                right,
            )
            == output
        )
