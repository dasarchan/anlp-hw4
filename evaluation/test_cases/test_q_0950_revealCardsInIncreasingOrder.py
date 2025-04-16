import pytest
from q_0950_revealCardsInIncreasingOrder import Solution


@pytest.mark.parametrize(
    "deck, output",
    [([17, 13, 11, 2, 3, 5, 7], [2, 13, 3, 11, 5, 17, 7]), ([1, 1000], [1, 1000])],
)
class TestSolution:
    def test_deckRevealedIncreasing(self, deck: List[int], output: List[int]):
        sc = Solution()
        assert (
            sc.deckRevealedIncreasing(
                deck,
            )
            == output
        )
