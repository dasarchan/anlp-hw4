import pytest
from q_2290_minimumObstacleRemovalToReachCorner import Solution


@pytest.mark.parametrize(
    "grid, output",
    [
        ([[0, 1, 1], [1, 1, 0], [1, 1, 0]], 2),
        ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0),
    ],
)
class TestSolution:
    def test_minimumObstacles(self, grid: List[List[int]], output: int):
        sc = Solution()
        assert (
            sc.minimumObstacles(
                grid,
            )
            == output
        )
