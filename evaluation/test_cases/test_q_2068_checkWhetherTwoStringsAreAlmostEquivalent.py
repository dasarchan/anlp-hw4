import pytest
from q_2068_checkWhetherTwoStringsAreAlmostEquivalent import Solution


@pytest.mark.parametrize(
    "word1, word2, output",
    [
        ("aaaa", "bccb", False),
        ("abcdeef", "abaaacc", True),
        ("cccddabba", "babababab", True),
    ],
)
class TestSolution:
    def test_checkAlmostEquivalent(self, word1: str, word2: str, output: bool):
        sc = Solution()
        assert (
            sc.checkAlmostEquivalent(
                word1,
                word2,
            )
            == output
        )
