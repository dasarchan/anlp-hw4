import pytest
from q_0292_nimGame import Solution


@pytest.mark.parametrize("n, output", [(4, False), (1, True), (2, True)])
class TestSolution:
    def test_canWinNim(self, n: int, output: bool):
        sc = Solution()
        assert (
            sc.canWinNim(
                n,
            )
            == output
        )
