import pytest
from q_1848_minimumDistanceToTheTargetElement import Solution


@pytest.mark.parametrize(
    "nums, target, start, output",
    [
        ([1, 2, 3, 4, 5], 5, 3, 1),
        ([1], 1, 0, 0),
        ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 1, 0, 0),
    ],
)
class TestSolution:
    def test_getMinDistance(
        self, nums: List[int], target: int, start: int, output: int
    ):
        sc = Solution()
        assert (
            sc.getMinDistance(
                nums,
                target,
                start,
            )
            == output
        )
