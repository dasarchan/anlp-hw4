import pytest
from q_0336_palindromePairs import Solution


@pytest.mark.parametrize(
    "words, output",
    [
        (["abcd", "dcba", "lls", "s", "sssll"], [[0, 1], [1, 0], [3, 2], [2, 4]]),
        (["bat", "tab", "cat"], [[0, 1], [1, 0]]),
        (["a", ""], [[0, 1], [1, 0]]),
    ],
)
class TestSolution:
    def test_palindromePairs(self, words: List[str], output: List[List[int]]):
        sc = Solution()
        assert (
            sc.palindromePairs(
                words,
            )
            == output
        )
