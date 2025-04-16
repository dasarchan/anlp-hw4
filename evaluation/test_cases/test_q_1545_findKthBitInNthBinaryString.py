import pytest
from q_1545_findKthBitInNthBinaryString import Solution


@pytest.mark.parametrize("n, k, output", [(3, 1, "0"), (4, 11, "1")])
class TestSolution:
    def test_findKthBit(self, n: int, k: int, output: str):
        sc = Solution()
        assert (
            sc.findKthBit(
                n,
                k,
            )
            == output
        )
