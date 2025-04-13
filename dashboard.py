from debt_repayment.GUI import DebtAPP
from debt_repayment.tools.logger_utils import my_log
from debt_repayment.amortization_table.table import AmortizationTable


if __name__=="__main__":
    DebtAPP(AmortizationTable)