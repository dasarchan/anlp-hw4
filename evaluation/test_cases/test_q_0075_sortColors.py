import pytest
from q_0075_sortColors import Solution


@pytest.mark.parametrize(
    "nums, output", [([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]), ([2, 0, 1], [0, 1, 2])]
)
class TestSolution:
    def test_sortColors(self, nums: List[int], output: None):
        sc = Solution()
        assert (
            sc.sortColors(
                nums,
            )
            == output
        )
