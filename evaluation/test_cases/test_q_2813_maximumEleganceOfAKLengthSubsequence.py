import pytest
from q_2813_maximumEleganceOfAKLengthSubsequence import Solution


@pytest.mark.parametrize(
    "items, k, output",
    [
        ([[3, 2], [5, 1], [10, 1]], 2, 17),
        ([[3, 1], [3, 1], [2, 2], [5, 3]], 3, 19),
        ([[1, 1], [2, 1], [3, 1]], 3, 7),
    ],
)
class TestSolution:
    def test_findMaximumElegance(self, items: List[List[int]], k: int, output: int):
        sc = Solution()
        assert (
            sc.findMaximumElegance(
                items,
                k,
            )
            == output
        )
