import pytest
from q_0496_nextGreaterElementI import Solution


@pytest.mark.parametrize(
    "nums1, nums2, output",
    [([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]), ([2, 4], [1, 2, 3, 4], [3, -1])],
)
class TestSolution:
    def test_nextGreaterElement(
        self, nums1: List[int], nums2: List[int], output: List[int]
    ):
        sc = Solution()
        assert (
            sc.nextGreaterElement(
                nums1,
                nums2,
            )
            == output
        )
