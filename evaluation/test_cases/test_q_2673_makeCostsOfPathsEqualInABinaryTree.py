import pytest
from q_2673_makeCostsOfPathsEqualInABinaryTree import Solution


@pytest.mark.parametrize(
    "n, cost, output", [(7, [1, 5, 2, 2, 3, 3, 1], 6), (3, [5, 3, 3], 0)]
)
class TestSolution:
    def test_minIncrements(self, n: int, cost: List[int], output: int):
        sc = Solution()
        assert (
            sc.minIncrements(
                n,
                cost,
            )
            == output
        )
