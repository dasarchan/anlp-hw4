import pytest
from q_1318_minimumFlipsToMakeAOrBEqualToC import Solution


@pytest.mark.parametrize("a, b, c, output", [(2, 6, 5, 3), (4, 2, 7, 1), (1, 2, 3, 0)])
class TestSolution:
    def test_minFlips(self, a: int, b: int, c: int, output: int):
        sc = Solution()
        assert (
            sc.minFlips(
                a,
                b,
                c,
            )
            == output
        )
