import pytest
from q_0215_kthLargestElementInAnArray import Solution


@pytest.mark.parametrize(
    "nums, k, output", [([3, 2, 1, 5, 6, 4], 2, 5), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4)]
)
class TestSolution:
    def test_findKthLargest(self, nums: List[int], k: int, output: int):
        sc = Solution()
        assert (
            sc.findKthLargest(
                nums,
                k,
            )
            == output
        )
