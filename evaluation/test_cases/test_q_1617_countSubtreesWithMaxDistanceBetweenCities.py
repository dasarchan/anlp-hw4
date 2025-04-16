import pytest
from q_1617_countSubtreesWithMaxDistanceBetweenCities import Solution


@pytest.mark.parametrize(
    "n, edges, output",
    [
        (4, [[1, 2], [2, 3], [2, 4]], [3, 4, 0]),
        (2, [[1, 2]], [1]),
        (3, [[1, 2], [2, 3]], [2, 1]),
    ],
)
class TestSolution:
    def test_countSubgraphsForEachDiameter(
        self, n: int, edges: List[List[int]], output: List[int]
    ):
        sc = Solution()
        assert (
            sc.countSubgraphsForEachDiameter(
                n,
                edges,
            )
            == output
        )
