import pytest
from q_2543_checkIfPointIsReachable import Solution


@pytest.mark.parametrize("targetX, targetY, output", [(6, 9, False), (4, 7, True)])
class TestSolution:
    def test_isReachable(self, targetX: int, targetY: int, output: bool):
        sc = Solution()
        assert (
            sc.isReachable(
                targetX,
                targetY,
            )
            == output
        )
