import pytest
from q_2562_findTheArrayConcatenationValue import Solution


@pytest.mark.parametrize(
    "nums, output", [([7, 52, 2, 4], 596), ([5, 14, 13, 8, 12], 673)]
)
class TestSolution:
    def test_findTheArrayConcVal(self, nums: List[int], output: int):
        sc = Solution()
        assert (
            sc.findTheArrayConcVal(
                nums,
            )
            == output
        )
