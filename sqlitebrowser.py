import os
import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets 
from modules.sqlite import sqlite

QtWidgets
class InputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QtWidgets.QLineEdit(self)
        self.second = QtWidgets.QLineEdit(self)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self);

        layout = QtWidgets.QFormLayout(self)
        layout.addRow('Column number', self.first)
        layout.addRow('Search query', self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())



class Ui_menu_window(QtWidgets.QWidget):
    def __init__(self,menu_window):
        super().__init__()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.fileName = ''
        self.filePath = ''
        self.menu_window = menu_window
    def setupUi(self):
        self.menu_window.setObjectName("menu_window")
        self.menu_window.setFixedSize(800, 605)
        self.menu_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.path + "/res/database-settings-icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.menu_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self.menu_window)
        self.centralwidget.setObjectName("centralwidget")
        self.img_menu = QtWidgets.QLabel(self.centralwidget)
        self.img_menu.setGeometry(QtCore.QRect(230, 10, 341, 331))
        self.img_menu.setText("")
        self.img_menu.setPixmap(QtGui.QPixmap(self.path + "/res/database-settings-icon.gif"))
        self.img_menu.setScaledContents(True)
        self.img_menu.setObjectName("img_menu")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(270, 360, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(14)
        self.btn_open.setFont(font)
        self.btn_open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_open.setObjectName("btn_open")
        self.btn_create = QtWidgets.QPushButton(self.centralwidget)
        self.btn_create.setGeometry(QtCore.QRect(270, 420, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(14)
        self.btn_create.setFont(font)
        self.btn_create.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_create.setObjectName("btn_create")
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit.setGeometry(QtCore.QRect(270, 480, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(14)
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_exit.setObjectName("btn_exit")
        self.menu_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.menu_window)
        QtCore.QMetaObject.connectSlotsByName(self.menu_window)

        self.btn_open.clicked.connect(self.open_btn)
        self.btn_create.clicked.connect(self.create_btn)
        self.btn_exit.clicked.connect(self.exit_btn)

    def retranslateUi(self, menu_window):
        _translate = QtCore.QCoreApplication.translate
        menu_window.setWindowTitle(_translate("menu_window", "SQLite Browser"))
        self.btn_open.setText(_translate("menu_window", "Open Database..."))
        self.btn_create.setText(_translate("menu_window", "Create New Database"))
        self.btn_exit.setText(_translate("menu_window", "Exit"))
    
    def open_btn(self):
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select the database file", "","All Files (*.sqlite3)")
        if self.fileName:
            self.change_window(self.fileName)

    def create_btn(self):
        name = self.getText()
        if name != '':
            self.filePath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory',self.path)
            if self.filePath:
                self.change_window(self.filePath + f'/{name}.sqlite3')
        

    def exit_btn(self):
        sys.exit()

    
    def getText(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self.menu_window, "Setup","Database name:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
        else:
            return '' 

    def change_window(self,path):
        self.menu_window.hide()
        self.tool_window = QtWidgets.QMainWindow()
        self.ui = Ui_tool_window(path)
        self.ui.setupUi(self.tool_window)
        self.tool_window.show()
        

class Ui_tool_window(object):
    def get_tables(self,database):
        tables = database.show_tables()
        result = []
        for table_t in tables:
            for table_l in table_t:
                if table_l not in result:
                    result.append(table_l)

        return result

    def __init__(self,path):


        self._translate = QtCore.QCoreApplication.translate
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.path = path
        self.db = sqlite(path)
        self.tables = self.get_tables(self.db)

    def setupUi(self, tool_window):
        tool_window.setObjectName("tool_window")
        tool_window.setFixedSize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.script_path + "/res/database-settings-icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        tool_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(tool_window)
        self.centralwidget.setObjectName("centralwidget")
        self.txt_tool = QtWidgets.QLabel(self.centralwidget)
        self.txt_tool.setGeometry(QtCore.QRect(30, 20, 541, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(16)
        self.txt_tool.setFont(font)
        self.txt_tool.setObjectName("txt_tool")
        self.cbb_tables = QtWidgets.QComboBox(self.centralwidget)
        self.cbb_tables.setGeometry(QtCore.QRect(580, 20, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        self.cbb_tables.setFont(font)
        self.cbb_tables.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cbb_tables.setObjectName("cbb_tables")
        self.tw_display = QtWidgets.QTableWidget(self.centralwidget)
        self.tw_display.setGeometry(QtCore.QRect(30, 70, 731, 401))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        self.tw_display.setFont(font)
        self.edt_command = QtWidgets.QLineEdit(self.centralwidget)
        self.edt_command.setGeometry(QtCore.QRect(30, 490, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        self.edt_command.setFont(font)
        self.edt_command.setObjectName("edt_command")
        self.btn_execute = QtWidgets.QPushButton(self.centralwidget)
        self.btn_execute.setGeometry(QtCore.QRect(550, 490, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(10)
        self.btn_execute.setFont(font)
        self.btn_execute.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_execute.setObjectName("btn_execute")
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(670, 490, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(10)
        self.btn_clear.setFont(font)
        self.btn_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear.setObjectName("btn_clear")
        self.btn_browse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_browse.setGeometry(QtCore.QRect(200, 540, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(10)
        self.btn_browse.setFont(font)
        self.btn_browse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_browse.setObjectName("btn_browse")

        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(670, 540, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(10)
        self.btn_search.setFont(font)
        self.btn_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search.setObjectName("btn_search")

        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit.setGeometry(QtCore.QRect(410, 540, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(10)
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_exit.setObjectName("btn_exit")
        tool_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(tool_window)
        self.statusbar.setObjectName("statusbar")
        tool_window.setStatusBar(self.statusbar)

        self.btn_browse.clicked.connect(self.browse_btn)
        self.btn_exit.clicked.connect(self.exit_btn)
        self.btn_execute.clicked.connect(self.execute_btn)
        self.btn_clear.clicked.connect(self.clear_btn)
        self.btn_search.clicked.connect(self.search_btn)

        self.retranslateUi(tool_window)
        QtCore.QMetaObject.connectSlotsByName(tool_window)

    def retranslateUi(self, tool_window):
        
        tool_window.setWindowTitle(self._translate("tool_window", "SQLite Browser"))
        self.txt_tool.setText(self._translate("tool_window", "choose the table that you want to browse :"))
        __sortingEnabled = self.tw_display.isSortingEnabled()
        self.tw_display.setSortingEnabled(False)
        self.combobox()
        self.tw_display.setSortingEnabled(__sortingEnabled)
        self.btn_execute.setText(self._translate("tool_window", "Execute"))
        self.btn_clear.setText(self._translate("tool_window", "Clear"))
        self.btn_browse.setText(self._translate("tool_window", "Browse"))
        self.btn_search.setText(self._translate("tool_window", "Search"))
        self.btn_exit.setText(self._translate("tool_window", "Exit"))
    
    def search_btn(self):
        def not_found(inp):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon(self.script_path + "/res/database-settings-icon.ico"))
            msg.setWindowTitle(f'No record found !')
            msg.setText(f'No record with query {inp[1]} in column {inp[0]}')
            msg.exec_()
        
        def empty_filed():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(QtGui.QIcon(self.script_path + "/res/database-settings-icon.ico"))
                msg.setWindowTitle(f'Requirement fields are empty !')
                msg.setText('Fill requirement fields and try again !')
                msg.exec_()

        def get_columns(database,tbname):
            return database.selectAll(tbname)
        if len(self.tables) != 0:
            dialog = InputDialog()
            dialog.setWindowTitle(self._translate("menu_window", "SQLite Browser"))
            dialog.setWindowIcon(QtGui.QIcon(self.script_path + "/res/database-settings-icon.ico"))
            if dialog.exec():
                inp = dialog.getInputs()
                if (inp[0] == '' and inp[1] == '') or (inp[0] == '' and inp[1] != '') or (inp[0] != '' and inp[1] == ''):
                    empty_filed()
                else:
                    try:
                        table = self.cbb_tables.currentText()
                        if table != '':
                            columns =  get_columns(self.db,table)
                            column_name = self.db.get_columns(table)
                            items = []
                            for column in columns:
                                if str(inp[1]).upper() in str(column[int(inp[0])-1]).upper():
                                    items.append(column)
                                    self.tw_display.setRowCount(len(items) + 1)
                                    self.tw_display.setColumnCount(len(column))
                            if len(items) != 0:
                                self.tw_display.setRowCount(len(items) + 1)
                                self.tw_display.setColumnCount(len(column))
                            else:
                                not_found(inp)
                            for index,name in enumerate(column_name):
                                self.tw_display.setItem(0,index,QtWidgets.QTableWidgetItem(str(name[1])))
                            for idr,item in enumerate(items):
                                for idc,query in enumerate(item):
                                    self.tw_display.setItem(idr + 1,idc,QtWidgets.QTableWidgetItem(str(query)))
                    except:
                        not_found(inp)
                                    

            

    def combobox(self):
        if len(self.tables) != 0:
            for idx , table in enumerate(self.tables):
                self.cbb_tables.addItem(table)
                self.cbb_tables.setItemText(idx , self._translate("tool_window", table))
    
    def browse_btn(self):
        def get_row(database,tbname):
            return database.get_rows(tbname)[0]
        
        def get_columns(database,tbname):
            return database.selectAll(tbname)

        table = self.cbb_tables.currentText()
        if table != '':
            row_count = get_row(self.db,table)[0]
            columns =  get_columns(self.db,table)
            column_name = self.db.get_columns(table)
            if columns == []:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(QtGui.QIcon(self.script_path + "/res/database-settings-icon.ico"))
                msg.setWindowTitle(f'Table ({table}) is empty !')
                msg.setText('Choose another table and try again!')
                msg.exec_()
            else:
                column_count = len(columns[0])
                self.tw_display.setRowCount(row_count + 1)
                self.tw_display.setColumnCount(column_count)
                for index,name in enumerate(column_name):
                    self.tw_display.setItem(0,index,QtWidgets.QTableWidgetItem(str(name[1])))
                for idr,item in enumerate(columns):
                    for idc,column in enumerate(item):
                        self.tw_display.setItem(idr + 1,idc,QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon(self.script_path + "/res/database-settings-icon.ico"))
            msg.setWindowTitle(f'Database is empty !')
            msg.setText('Create a table and try again !')
            msg.exec_()

        
    def execute_btn(self):
        command = self.edt_command.text()
        msg =  QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowIcon(QtGui.QIcon(self.script_path + "/res/database-settings-icon.ico"))
        if command == '':
            msg.setWindowTitle('the input is empty !')
            msg.setText('please fill the input box and try again')
            msg.exec_()
        try:
            self.db.execute_manuall(command)
        except sqlite3.Error as error:
            msg.setWindowTitle('Wrong Command')
            msg.setText(f'wrong command executed try again !\nerror info : {error}')
            msg.exec_()
        
        self.tables = self.get_tables(self.db)
        self.cbb_tables.clear()
        self.combobox()

    def exit_btn(self):
        sys.exit()

    def clear_btn(self):
        self.edt_command.setText('')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    menu_window = QtWidgets.QMainWindow()
    ui = Ui_menu_window(menu_window)
    ui.setupUi()
    menu_window.show()
    sys.exit(app.exec_())
