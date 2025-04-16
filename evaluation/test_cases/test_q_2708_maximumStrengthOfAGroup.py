import pytest
from q_2708_maximumStrengthOfAGroup import Solution


@pytest.mark.parametrize(
    "nums, output", [([3, -1, -5, 2, 5, -9], 1350), ([-4, -5, -4], 20)]
)
class TestSolution:
    def test_maxStrength(self, nums: List[int], output: int):
        sc = Solution()
        assert (
            sc.maxStrength(
                nums,
            )
            == output
        )
