import pytest
from q_2369_checkIfThereIsAValidPartitionForTheArray import Solution


@pytest.mark.parametrize(
    "nums, output", [([4, 4, 4, 5, 6], True), ([1, 1, 1, 2], False)]
)
class TestSolution:
    def test_validPartition(self, nums: List[int], output: bool):
        sc = Solution()
        assert (
            sc.validPartition(
                nums,
            )
            == output
        )
