import pytest
from q_1662_checkIfTwoStringArraysAreEquivalent import Solution


@pytest.mark.parametrize(
    "word1, word2, output",
    [
        (["ab", "c"], ["a", "bc"], True),
        (["a", "cb"], ["ab", "c"], False),
        (["abc", "d", "defg"], ["abcddefg"], True),
    ],
)
class TestSolution:
    def test_arrayStringsAreEqual(
        self, word1: List[str], word2: List[str], output: bool
    ):
        sc = Solution()
        assert (
            sc.arrayStringsAreEqual(
                word1,
                word2,
            )
            == output
        )
