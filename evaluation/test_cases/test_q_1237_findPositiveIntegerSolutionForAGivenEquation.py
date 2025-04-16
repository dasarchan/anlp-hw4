import pytest
from q_1237_findPositiveIntegerSolutionForAGivenEquation import Solution


@pytest.mark.parametrize(
    "function_id, z, output",
    [(1, 5, [[1, 4], [2, 3], [3, 2], [4, 1]]), (2, 5, [[1, 5], [5, 1]])],
)
class TestSolution:
    def test_findSolution(
        self, customfunction: "CustomFunction", z: int, output: List[List[int]]
    ):
        sc = Solution()
        assert (
            sc.findSolution(
                function_id,
                z,
            )
            == output
        )
