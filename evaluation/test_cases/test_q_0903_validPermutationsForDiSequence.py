import pytest
from q_0903_validPermutationsForDiSequence import Solution


@pytest.mark.parametrize("s, output", [("DID", 5), ("D", 1)])
class TestSolution:
    def test_numPermsDISequence(self, s: str, output: int):
        sc = Solution()
        assert (
            sc.numPermsDISequence(
                s,
            )
            == output
        )
