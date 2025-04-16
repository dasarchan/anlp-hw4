import pytest
from q_2295_replaceElementsInAnArray import Solution


@pytest.mark.parametrize(
    "nums, operations, output",
    [
        ([1, 2, 4, 6], [[1, 3], [4, 7], [6, 1]], [3, 2, 7, 1]),
        ([1, 2], [[1, 3], [2, 1], [3, 2]], [2, 1]),
    ],
)
class TestSolution:
    def test_arrayChange(
        self, nums: List[int], operations: List[List[int]], output: List[int]
    ):
        sc = Solution()
        assert (
            sc.arrayChange(
                nums,
                operations,
            )
            == output
        )
