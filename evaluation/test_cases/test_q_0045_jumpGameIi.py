import pytest
from q_0045_jumpGameIi import Solution


@pytest.mark.parametrize("nums, output", [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2)])
class TestSolution:
    def test_jump(self, nums: List[int], output: int):
        sc = Solution()
        assert (
            sc.jump(
                nums,
            )
            == output
        )
