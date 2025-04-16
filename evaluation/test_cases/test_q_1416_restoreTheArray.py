import pytest
from q_1416_restoreTheArray import Solution


@pytest.mark.parametrize(
    "s, k, output", [("1000", 10000, 1), ("1000", 10, 0), ("1317", 2000, 8)]
)
class TestSolution:
    def test_numberOfArrays(self, s: str, k: int, output: int):
        sc = Solution()
        assert (
            sc.numberOfArrays(
                s,
                k,
            )
            == output
        )
