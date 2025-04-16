import pytest
from q_2528_maximizeTheMinimumPoweredCity import Solution


@pytest.mark.parametrize(
    "stations, r, k, output", [([1, 2, 4, 5, 0], 1, 2, 5), ([4, 4, 4, 4], 0, 3, 4)]
)
class TestSolution:
    def test_maxPower(self, stations: List[int], r: int, k: int, output: int):
        sc = Solution()
        assert (
            sc.maxPower(
                stations,
                r,
                k,
            )
            == output
        )
