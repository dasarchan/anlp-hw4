import pytest
from q_2607_makeKSubarraySumsEqual import Solution


@pytest.mark.parametrize("arr, k, output", [([1, 4, 1, 3], 2, 1), ([2, 5, 5, 7], 3, 5)])
class TestSolution:
    def test_makeSubKSumEqual(self, arr: List[int], k: int, output: int):
        sc = Solution()
        assert (
            sc.makeSubKSumEqual(
                arr,
                k,
            )
            == output
        )
