from PyQt5.QtWidgets import QDateTimeEdit, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDate, QDateTime, QTime
import datetime as dt
from ui.home import Ui_MainWindow
from modules.admin_database import AdminDatabase
from modules.query_database import QueryDatabase
from modules.draw_charts import Draw
from modules.get_data_from_Tushare import get_stock_info


class ApoloWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ApoloWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_search.clicked.connect(self.get_stock_info_dao)
        self.ui.btn_update_k_data.clicked.connect(self.update_k_data_dao)
        self.ui.btn_update_statement.clicked.connect(self.update_statement_dao)
        self.ui.btn_search_k_data.clicked.connect(self.calendar_dao)
        self.ui.btn_draw.clicked.connect(self.calendar_period_dao)

        self.ui.btn_update_sz50.clicked.connect(self.update_sz50_dao)
        self.ui.btn_update_hs300.clicked.connect(self.update_hs300_dao)
        self.ui.btn_update_zz500.clicked.connect(self.update_zz500_dao)

        self.ui.btn_update_divi_data.clicked.connect(self.update_dividend_data_dao)
        self.ui.input_stock_code.setText('000001')


    def check_input_stock_code(self):
        self.ui.input_stock_code.selectAll()
        if len(self.ui.input_stock_code.selectedText()) == 0:
            self.ui.textEdit.append("Please input stock code")
            return False
        return True

    """By Stock Code"""
    def get_stock_info_dao(self):
        if self.check_input_stock_code():
            result = get_stock_info(self.ui.input_stock_code.text())
            self.ui.textEdit.append(str(result))

    def update_k_data_dao(self):
        if self.check_input_stock_code():
            result = AdminDatabase.update_db_k_data(self.ui.input_stock_code.text())
            self.ui.textEdit.append(str(result))
            print(result)

    def calendar_dao(self):
        if self.check_input_stock_code():
            date = self.ui.input_from_date.text()
            value = QueryDatabase.get_k_value(self.ui.input_stock_code.text(), date)
            self.ui.output_close_price.setText(str(value))

    def calendar_period_dao(self):
        if self.check_input_stock_code():
            # date = self.ui.calendarWidget.selectedDate().toString(Qt.ISODate) #.toPyDate()
            data, index = QueryDatabase.get_k_value_period(self.ui.input_stock_code.text(),
                                              self.ui.input_from_date.text(), self.ui.input_to_date.text())
            Draw.draw_k_data_period(data, index)

    """Statement"""
    def update_statement_dao(self):
        if self.check_input_stock_code():
            if self.ui.rdb_bs.isChecked():
                result = AdminDatabase.update_db_consolidated_statement_data(self.ui.input_stock_code.text(), 'BS')
                self.ui.textEdit.append(result)
                print(result)
            elif self.ui.rdb_cash.isChecked():
                result = AdminDatabase.update_db_consolidated_statement_data(self.ui.input_stock_code.text(), 'Cash')
                self.ui.textEdit.append(result)
                print(result)
            elif self.ui.rdb_pl.isChecked():
                result = AdminDatabase.update_db_consolidated_statement_data(self.ui.input_stock_code.text(), 'PL')
                self.ui.textEdit.append(result)
                print(result)
            else:
                self.ui.textEdit.append("Please choose one type")

    """By Stock List"""
    def update_sz50_dao(self):
        result = AdminDatabase.update_data_sz50()
        self.ui.textEdit.append(str(result))
        print(result)

    def update_hs300_dao(self):
        result = AdminDatabase.update_data_hs300()
        self.ui.textEdit.append(str(result))
        print(result)

    def update_zz500_dao(self):
        self.ui.textEdit.append('Disabled')
        print("Disabled")
    #
    # """For All Stock"""
    def update_dividend_data_dao(self):
        result = AdminDatabase.update_db_dividend_data()
        self.ui.textEdit.append(str(result))
        print(result)
#