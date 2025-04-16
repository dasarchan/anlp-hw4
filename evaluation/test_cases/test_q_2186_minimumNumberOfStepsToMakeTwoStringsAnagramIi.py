import pytest
from q_2186_minimumNumberOfStepsToMakeTwoStringsAnagramIi import Solution


@pytest.mark.parametrize(
    "s, t, output", [("**lee**tco**de**", "co**a**t**s**", 7), ("night", "thing", 0)]
)
class TestSolution:
    def test_minSteps(self, s: str, t: str, output: int):
        sc = Solution()
        assert (
            sc.minSteps(
                s,
                t,
            )
            == output
        )
