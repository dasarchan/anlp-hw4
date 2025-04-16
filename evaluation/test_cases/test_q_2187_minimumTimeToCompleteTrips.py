import pytest
from q_2187_minimumTimeToCompleteTrips import Solution


@pytest.mark.parametrize("time, totalTrips, output", [([1, 2, 3], 5, 3), ([2], 1, 2)])
class TestSolution:
    def test_minimumTime(self, time: List[int], totalTrips: int, output: int):
        sc = Solution()
        assert (
            sc.minimumTime(
                time,
                totalTrips,
            )
            == output
        )
