
# A Python and SQLite Turing Machine simulator

import sqlite3
import sys

class TuringMachine:
    def __init__(self):
         self.db=sqlite3.connect(':memory:')
         cursor=self.db.cursor()
         cursor.execute('''
             create table transitionTable (
                 state text, 
                 readSymbol varchar(1), 
                 nextState text, 
                 writeSymbol varchar(1),
                 move varchar(1)
             )''')
         cursor.execute('''
             create table trace (
                 seqNum integer primary key autoincrement, 
                 step integer, 
                 tapeData text,
                 state text,
                 headPos integer,
                 parent integer
             )''')


    def setTable(self, t):
        self.transitionTable=t
        cursor = self.db.cursor()
        for row in self.transitionTable:
            cursor.execute('insert into transitionTable values (?, ?, ?, ?, ?)', row)

    def setFinal(self, finalState):
        self.finalState = finalState

    def getAction(self, state, readSymbol):
        cursor = self.db.cursor()
        cursor.execute('''
            select 
                nextState, writeSymbol, move 
            from 
                transitionTable
            where 
                state = ? and readSymbol = ?
            ''', [state, readSymbol])
        return cursor.fetchall()

    def extend_or_trim(self, tapeData, headPos):
        newTapeData, newHeadPos = tapeData, headPos
        n = len(tapeData)
        if headPos < 0:
            newTapeData = 'B' * (-headPos) + tapeData
            newHeadPos = 0
        elif headPos >= n:
            newTapeData = tapeData + 'B' * (headPos - n + 1)
        else:
            i, j = 0, n-1
            while (i < headPos and tapeData[i] == 'B'): i+=1
            while (j > headPos and tapeData[j] == 'B'): j-=1
            newTapeData = tapeData[i:j+1]
            newHeadPos -= i
        return newTapeData, newHeadPos

    def run(self, tapeData, state, headPos=0, stepCap=200):
        cursor = self.db.cursor()
        cursor.execute('''
                insert into trace (step, tapeData, state, headPos, parent) values (0, ?, ?, ?, ?)
            ''', [tapeData, state, headPos, 'Null'])

        self.nextID = []
        for t in xrange(1, stepCap):
            cursor.execute('''
                    select 
                        seqNum, tapeData, state, headPos
                    from 
                        trace 
                    where 
                        step=? ''', [t-1])
            for seqNum, tapeData, state, headPos in cursor.fetchall():
                n = len(tapeData)
                tapeData, headPos = self.extend_or_trim(tapeData, headPos)

                readSymbol = tapeData[headPos]
                for nextState, writeSymbol, move in self.getAction(state, readSymbol):
                    newTapeData = tapeData[:headPos] + writeSymbol + tapeData[headPos+1:]
                    if move == 'L':
                        newHeadPos = headPos - 1
                    elif move == 'R':
                        newHeadPos = headPos + 1
                    else :
                        newHeadPos = headPos
                    newTapeData, newHeadPos = self.extend_or_trim(newTapeData, newHeadPos)
                    cursor.execute('''
                        insert into trace 
                            (step, tapeData, state, headPos, parent) 
                            values (?, ?, ?, ?, ?)
                        ''', [t, newTapeData, nextState, newHeadPos, seqNum]
                    )
                    # print tapeData, state, headPos, nextState, writeSymbol, move
                    # print newTapeData, nextState, newHeadPos
                    # print '->', state, readSymbol, nextState, writeSymbol, move


    def printDBTable(self, name):
        cursor = self.db.cursor()
        result = cursor.execute('select * from {}'.format(name))
        for row in result:
            print row

    def printStep(self, i):
        cursor = self.db.cursor()
        cursor.execute('select * from trace where step=?', [i])
        for row in cursor:
            print row[0], row[1], row[2], row[3], row[4], row[5]

    def printFullTrace(self, seqNum, stepCap):
        cursor = self.db.cursor()
        cursor.execute('select * from trace where seqNum=?', [seqNum])
        entry = cursor.fetchone()
        step = entry[1]
        if step <= stepCap:
            print '\t'*step, entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]
            cursor.execute('select * from trace where parent=?', [seqNum])
            for row in cursor:
                self.printFullTrace(row[0], stepCap) 

    def printFinal(self):
        cursor = self.db.cursor()
        cursor.execute('''
                select * from trace where state='?'
            ''', [self.finalState])
        for row in cursor:
            print row


if __name__=="__main__":
    print "Hello, Welcome to Duo's single-taple Turing Machine implementation"
    print "---- seqNum, tapeData, state, headPos, parent ---- \n"
    readState = False
    readStage = 0
    transitionTable=[]
    tapeData=''
    state=''
    headPos=0
    finalState='qf'
    stepCap=100
    for line in sys.stdin:
        if ('---' in line):
            if readState == True:
                readStage += 1
            readState = False
        else:
            readState = True

        if readState:
            lineList = line.split()
            if readStage == 0:
                if len(lineList) == 5:
                    transitionTable.append(lineList)
            elif readStage == 1:
                if len(lineList) == 3:
                    tapeData, state, headPos = lineList
                    headPos = int(headPos)
            elif readStage == 2:
                if len(lineList) == 1:
                    finalState = lineList[0]
            elif readStage == 3:
                if len(lineList) == 1:
                    stepCap = int(lineList[0])
                    step = min(stepCap, 1000)

    TM = TuringMachine()
    TM.setTable(transitionTable)
    TM.setFinal(finalState)
    # TM.printDBTable()
    TM.run(tapeData, state, headPos)
    # TM.printFinal()
    TM.printStep(stepCap)
    print
    TM.printFullTrace(1,stepCap)

