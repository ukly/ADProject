from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtCore import Qt


class coloredCal():                             #색상을 결정하고 반환해줌
    def colored(self, worksCount):
        fm = QTextCharFormat()
        if worksCount == 0:
            fm.setBackground(Qt.white)
            return fm
        if 1 <= worksCount < 4:
            fm.setBackground(Qt.green)
            return fm
        elif 4<= worksCount < 7:
            fm.setBackground(Qt.yellow)
            return fm
        elif 7<= worksCount:
            fm.setForeground(Qt.black)
            fm.setBackground(Qt.red)
            return fm
