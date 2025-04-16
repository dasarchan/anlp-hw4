import pytest
from q_2135_countWordsObtainedAfterAddingALetter import Solution


@pytest.mark.parametrize(
    "startWords, targetWords, output",
    [
        (["ant", "act", "tack"], ["tack", "act", "acti"], 2),
        (["ab", "a"], ["abc", "abcd"], 1),
    ],
)
class TestSolution:
    def test_wordCount(
        self, startWords: List[str], targetWords: List[str], output: int
    ):
        sc = Solution()
        assert (
            sc.wordCount(
                startWords,
                targetWords,
            )
            == output
        )
