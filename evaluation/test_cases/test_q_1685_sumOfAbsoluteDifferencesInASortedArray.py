import pytest
from q_1685_sumOfAbsoluteDifferencesInASortedArray import Solution


@pytest.mark.parametrize(
    "nums, output", [([2, 3, 5], [4, 3, 5]), ([1, 4, 6, 8, 10], [24, 15, 13, 15, 21])]
)
class TestSolution:
    def test_getSumAbsoluteDifferences(self, nums: List[int], output: List[int]):
        sc = Solution()
        assert (
            sc.getSumAbsoluteDifferences(
                nums,
            )
            == output
        )
