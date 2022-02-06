from bot import *
from tictactoe import *

startBoard = []
for i in range(3):
    startBoard.append([""]*3)  

startState = State("p1",startBoard)
trace = obtainTrace(
    evaluator=evaluator,
    nextStates=nextStates,
    player="p1",
    state=startState)
printTrace(statePrinter=statePrinter, level=0,trace=trace)