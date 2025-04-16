import pytest
from q_0168_excelSheetColumnTitle import Solution


@pytest.mark.parametrize("columnNumber, output", [(1, "A"), (28, "AB"), (701, "ZY")])
class TestSolution:
    def test_convertToTitle(self, columnNumber: int, output: str):
        sc = Solution()
        assert (
            sc.convertToTitle(
                columnNumber,
            )
            == output
        )
