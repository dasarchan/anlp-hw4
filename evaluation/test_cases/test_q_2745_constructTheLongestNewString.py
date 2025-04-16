import pytest
from q_2745_constructTheLongestNewString import Solution


@pytest.mark.parametrize("x, y, z, output", [(2, 5, 1, 12), (3, 2, 2, 14)])
class TestSolution:
    def test_longestString(self, x: int, y: int, z: int, output: int):
        sc = Solution()
        assert (
            sc.longestString(
                x,
                y,
                z,
            )
            == output
        )
