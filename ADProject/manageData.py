import pickle


class addAndDel:                    #입력된 데이터들을 추가되고 제거되는 데이터들을 저장

    def __init__(self):
        self.dbfilename = 'toDoList'
        self.works = dict()


    def readData(self):            #입력되어서 toDoList.dat에 딕셔너리 형태로 저장되어있던 데이터들을 불러옴
        self.works = dict()
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.works = dict()
            return
        try:
            self.works = pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()

    def writeData(self):                    #추가나 제거를 통해 변경된 점을 저장
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.works, fH)
        self.works = dict()
        fH.close()


    def addWork(self, dateCode, timeCode, content):             #마감기간과 마감시간, 할일들 인자로 받고 이를 데이터에 저장
        self.readData()
        if dateCode in self.works:
            if timeCode in self.works[dateCode]:
                self.works[dateCode][timeCode].append(content)
            else:
                self.works[dateCode][timeCode] = [content]
        else:
            self.works[dateCode] = {timeCode: [content]}
        self.writeData()



    def delWork(self, dateCode, timeCode, content):             #특정 마감기간과 마감시간 할일에 해당하는 데이터를 삭제
        self.readData()
        for idx in range(len(self.works[dateCode][timeCode])-1, -1, -1):
            if self.works[dateCode][timeCode][idx] == content:
                del self.works[dateCode][timeCode][idx]
                if len(self.works[dateCode][timeCode]) == 0:
                    del self.works[dateCode][timeCode]
                    if len(self.works[dateCode]) == 0:
                        del self.works[dateCode]
                        break
                    else:
                        break
        self.writeData()


    def sortWorksList(self, yyyymmdd):       #시간별로 table에 출력하기 위해 특정 날짜의 할일들을 마감시간순으로 정렬한 리스트를 반환
        self.readData()
        if yyyymmdd in self.works:
            sortedWorkList = sorted(self.works[yyyymmdd].items(), key=lambda x:x[0])
            return sortedWorkList
        else:
            return []














