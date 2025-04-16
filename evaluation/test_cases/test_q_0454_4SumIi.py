import pytest
from q_0454_4SumIi import Solution


@pytest.mark.parametrize(
    "nums1, nums2, nums3, nums4, output",
    [([1, 2], [-2, -1], [-1, 2], [0, 2], 2), ([0], [0], [0], [0], 1)],
)
class TestSolution:
    def test_fourSumCount(
        self,
        nums1: List[int],
        nums2: List[int],
        nums3: List[int],
        nums4: List[int],
        output: int,
    ):
        sc = Solution()
        assert (
            sc.fourSumCount(
                nums1,
                nums2,
                nums3,
                nums4,
            )
            == output
        )
