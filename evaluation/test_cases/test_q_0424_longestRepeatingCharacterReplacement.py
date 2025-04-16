import pytest
from q_0424_longestRepeatingCharacterReplacement import Solution


@pytest.mark.parametrize("s, k, output", [("ABAB", 2, 4), ("AABABBA", 1, 4)])
class TestSolution:
    def test_characterReplacement(self, s: str, k: int, output: int):
        sc = Solution()
        assert (
            sc.characterReplacement(
                s,
                k,
            )
            == output
        )
