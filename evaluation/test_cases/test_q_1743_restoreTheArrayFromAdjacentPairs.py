import pytest
from q_1743_restoreTheArrayFromAdjacentPairs import Solution


@pytest.mark.parametrize(
    "adjacentPairs, output",
    [
        ([[2, 1], [3, 4], [3, 2]], [1, 2, 3, 4]),
        ([[4, -2], [1, 4], [-3, 1]], [-2, 4, 1, -3]),
        ([[100000, -100000]], [100000, -100000]),
    ],
)
class TestSolution:
    def test_restoreArray(self, adjacentPairs: List[List[int]], output: List[int]):
        sc = Solution()
        assert (
            sc.restoreArray(
                adjacentPairs,
            )
            == output
        )
