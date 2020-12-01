import sys
from PyQt5.QtWidgets import QLabel, QToolButton, \
    QApplication, QCalendarWidget, QLineEdit, QWidget, QTableWidget, QTableWidgetItem, QComboBox, QAbstractItemView
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import *

from coloredCal import coloredCal
from manageData import addAndDel

class calenDiary(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()                             #initUI생성
        self.showTable()                          #기록된 할일들 테이블에 출력
        self.showWorkItems()                      #기록된 할일들 콤보박스에 출력
        self.getcolor()                           #기록된 할일들을 토대로 달력에 색상입히기


    def initUI(self):

        self.cal = QCalendarWidget(self)
        self.cal.setGeometry(10, 10, 200, 150)
        self.cal.setGridVisible(True)                               #날마다 칸으로 나뉘게끔
        self.cal.setVerticalHeaderFormat(False)                     #몇주차인지 보이지 않게
        self.cal.selectionChanged.connect(self.showDate)
        self.cal.selectionChanged.connect(self.showTable)
        self.cal.selectionChanged.connect(self.showWorkItems)


        dateLabel = QLabel("날짜")                                   #선택한 날짜를 나타내는 layout
        self.dateLine = QLineEdit()
        self.dateLine.setReadOnly(True)
        self.showDate()

        deadlineLabel = QLabel("마감날짜")                            #할일에 대한 정보들을 입력하는 layout
        self.dueDate = QLineEdit()
        dateInfoLabel = QLabel("ㄴ YYYY.MM.DD 형식으로 입력해주세요")
        deadLineTimeLabel = QLabel("마감시간")
        self.dueTime = QLineEdit()
        timeInfoLabel = QLabel("ㄴ hour:minute 형식으로 입력해주세요")
        toDoLabel = QLabel("해야할 일 ")
        self.content = QLineEdit()
        self.addToDoBtn = QToolButton()
        self.addToDoBtn.setText("추가")
        self.addToDoBtn.clicked.connect(self.addClicked)
        self.warningLabel = QLabel("")
        self.warningLabel.setStyleSheet("Color: red")


        self.toDoTable = QTableWidget()                               #기록된 할일들을 table의 형태로 출력
        self.toDoTable.setRowCount(0)
        self.toDoTable.setColumnCount(3)
        self.toDoTable.setColumnWidth(0, self.width() * 1 / 7)
        self.toDoTable.setColumnWidth(1, self.width() * 1 / 7)
        self.toDoTable.setColumnWidth(2, self.width() * 5 / 7)
        self.toDoTable.setHorizontalHeaderLabels(["마감날짜",
                                                  "마감시간",
                                                  "해야할 일"])
        self.toDoTable.setEditTriggers(QAbstractItemView.NoEditTriggers)        #table을 수정할 수 없게(=readonly)



        calLayout = QGridLayout()                                   #gridlayout의 layout들에 위의 위젯들을 추가
        calLayout.addWidget(self.cal, 0, 0)

        dateLayout = QGridLayout()
        dateLayout.addWidget(dateLabel, 0, 0)
        dateLayout.addWidget(self.dateLine, 0, 1, 1, 1)

        inputLayout = QGridLayout()
        inputLayout.addWidget(deadlineLabel, 0, 0)
        inputLayout.addWidget(self.dueDate, 0, 1)
        inputLayout.addWidget(deadLineTimeLabel, 0, 2)
        inputLayout.addWidget(self.dueTime, 0, 3)
        inputLayout.addWidget(dateInfoLabel, 1, 1)
        inputLayout.addWidget(timeInfoLabel, 1, 3)
        inputLayout.addWidget(toDoLabel, 2, 0)
        inputLayout.addWidget(self.content, 2, 1)
        inputLayout.addWidget(self.addToDoBtn, 2, 2)
        inputLayout.addWidget(self.warningLabel, 2, 3)

        tableLayout = QGridLayout()
        tableLayout.addWidget(self.toDoTable)


        txtLayout = QGridLayout()
        txtLayout.addLayout(dateLayout, 0, 0)
        txtLayout.addLayout(inputLayout, 1, 0)
        txtLayout.addLayout(tableLayout, 2, 0)

        delLayout = QGridLayout()

        self.workItems = QComboBox()
        delLayout.addWidget(self.workItems, 0, 0)

        self.delBtn = QToolButton()
        self.delBtn.setText("제거")
        delLayout.addWidget(self.delBtn, 0, 1)
        self.delBtn.clicked.connect(self.delClicked)


        mainLayout = QGridLayout()

        mainLayout.addLayout(calLayout, 0, 0)
        mainLayout.addLayout(txtLayout, 0, 1)
        mainLayout.addLayout(delLayout, 1, 1)

        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 2)


        self.setLayout(mainLayout)
        self.setWindowTitle('CanlenDiary')
        self.setGeometry(300, 300, 1020, 350)
        self.show()


    def showDate(self):                                     #우측 상단에 선택된 날짜를 보여주는 함수
        date = self.cal.selectedDate()
        dateStr = date.toString('yyyy.MM.dd')
        self.dateLine.setText(dateStr)


    def showTable(self):                                    #날짜가 변경되면 그에 반응해 실행될 함수
        date = self.cal.selectedDate()                      #테이블에 선택된 날짜의 할일들을 출력
        dateInt = int(date.toString('yyyyMMdd'))

        aad = addAndDel()
        aad.readData()
        workList = aad.sortWorksList(dateInt)

        if len(workList) != 0:
            rows = 0
            for workInTime in workList:
                time = workInTime[0]
                time = time[:2] + "시 " + time[2:] + "분"
                for work in workInTime[1]:
                    self.toDoTable.setRowCount(rows+1)
                    self.toDoTable.setItem(rows, 0, QTableWidgetItem(str(dateInt)))
                    self.toDoTable.setItem(rows, 1, QTableWidgetItem(time))
                    self.toDoTable.setItem(rows, 2, QTableWidgetItem(work))
                    rows += 1
        else:
            self.toDoTable.setRowCount(0)
        

    def addClicked(self):                                       #추가 버튼이 클릭되면 입력된 정보들을 manageData를 거쳐
        aad = addAndDel()                                       #toDoList에 입력
        aad.readData()
        try:                                                    #정해진 형식에 맞게 입력됬는지 예외처리
            yyyy, mm, dd = self.dueDate.text().split('.')
            if len(mm) == 1:                                    #데이터안에서 코드화를 통해 관리하도록 빈 공백에 0을 추가
                mm = "0" + mm
            if len(dd) == 1:
                dd = "0" + dd
            y, m, d = int(yyyy), int(mm), int(dd)
            if((y%4 == 0 and y%100!=0) or y%400==0):            #존재하지 않는 월일에 대한 예외처리를 하는 조건문
                if(1<= m <= 12):
                    if(m in [1,3,5,7,8,10,12]):
                        if (1<= d <= 31):
                            yyyymmdd = int(yyyy + mm + dd)
                        else:
                            self.warningLabel.setText("오류!: 유효하지 않은 DD값입니다")
                            return
                    elif(m == 2):
                        if (1 <= d <= 28):
                            yyyymmdd = int(yyyy + mm + dd)
                        else:
                            self.warningLabel.setText("오류!: 유효하지 않은 DD값입니다")
                            return
                    else:
                        if (1<= d <=30):
                            yyyymmdd = int(yyyy + mm + dd)
                        else:
                            self.warningLabel.setText("오류!: 유효하지 않은 DD값입니다")
                            return
                else:
                    self.warningLabel.setText("오류!: 유효하지 않은 MM값입니다")
                    return
            elif (y>0):
                if (1 <= m <= 12):
                    if (m in [1, 3, 5, 7, 8, 10, 12]):
                        if (1 <= d <= 31):
                            yyyymmdd = int(yyyy + mm + dd)
                        else:
                            self.warningLabel.setText("오류!: 유효하지 않은 DD값입니다")
                            return
                    elif (m == 2):
                        if (1 <= d <= 29):
                            yyyymmdd = int(yyyy + mm + dd)
                        else:
                            self.warningLabel.setText("오류!: 유효하지 않은 DD값입니다")
                            return
                    else:
                        if (1 <= d <= 30):
                            yyyymmdd = int(yyyy + mm + dd)
                        else:
                            self.warningLabel.setText("오류!: 유효하지 않은 DD값입니다")
                            return
                else:
                    self.warningLabel.setText("오류!: 유효하지 않은 MM값입니다")
                    return
            else:
                self.warningLabel.setText("오류!: 유효하지 않은 YYYY값입니다")
                return
        except:
            self.warningLabel.setText("오류!: YYYY.MM.DD형식에 맞게 입력해주세요")
            self.dueDate.setText("")
            self.dueTime.setText("")
            self.content.setText("")
            return
        try:                                                    #올바른 형식으로 입력됐는지 예외처리
            hh, mm = self.dueTime.text().split(':')
            h, m = int(hh), int(mm)
            if not (0<= h <24):                                 #존재하지않는 시각에 대한 예외처리를 하는 조건문
                self.warningLabel.setText("오류!: 유효하지 않은 hour값입니다")
                return
            elif not(0<=m<60):
                self.warningLabel.setText(("오류!: 유효하지 않은 minute값입니다"))
                return
            if len(hh) == 1:
                hh = '0' + hh
            if len(mm) == 1:
                mm = '0' + mm
            hhmm = hh+mm
            ct = self.content.text()
            aad.addWork(yyyymmdd, hhmm, ct)
        except:
            self.warningLabel.setText("오류!: hour:minute 형식에 맞게 입력해주세요")
            self.dueDate.setText("")
            self.dueTime.setText("")
            self.content.setText("")
            return
        self.warningLabel.setText("")                       #정상적인 입력을 마치면 다음 입력을 위해 공백으로 초기화
        self.showTable()
        self.showWorkItems()
        self.coloring(yyyymmdd)
        self.dueDate.setText("")
        self.dueTime.setText("")
        self.content.setText("")

    def delClicked(self):                                   #combobox를 통해 할일들을 제거
        try:
            itemIdx = self.workItems.currentIndex()
            date = self.toDoTable.item(itemIdx, 0).text()
            date = int(date)
            time = self.toDoTable.item(itemIdx, 1).text()
            time = time[0:2] + time[4:6]
            work = self.toDoTable.item(itemIdx, 2).text()
            aad = addAndDel()
            aad.delWork(date, time, work)
        except:
            return
        self.showTable()
        self.showWorkItems()
        self.coloring(date)


    def showWorkItems(self):                                #combobox를 통해 해당 날짜의 할일들을 보여줌
        self.workItems.clear()
        rowCount = self.toDoTable.rowCount()
        for row in range(rowCount):
            work = self.toDoTable.item(row, 2).text()
            self.workItems.addItem(work)


    def getcolor(self):                                     #프로그램을 실행시키면 이전의 입려되었던 데이터를 기반으로 색칠
        aad = addAndDel()
        aad.readData()
        cc = coloredCal()
        for date in aad.works:
            workCount = 0
            for time in aad.works[date]:
                workCount += len(aad.works[date][time])
                date2 = QDate.fromString(str(date), "yyyyMMdd")
                self.cal.setDateTextFormat(date2, cc.colored(workCount))

    def coloring(self, date):                               #추가나 제거버튼의 클릭에 반응하여 색상을 변경
        aad = addAndDel()
        aad.readData()
        workCount=0
        cc = coloredCal()
        if date in aad.works:
            for time in aad.works[date]:
                workCount += len(aad.works[date][time])
                date2 = QDate.fromString(str(date), "yyyyMMdd")
                self.cal.setDateTextFormat(date2, cc.colored(workCount))
        else:
            date2 = QDate.fromString(str(date), "yyyyMMdd")
            self.cal.setDateTextFormat(date2, cc.colored(workCount))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = calenDiary()
    mainWindow.show()
    sys.exit(app.exec_())
