from tracemalloc import start
from bot import *
from reach15_game import *

startState = State("p1",1)
trace = obtainTrace(
    evaluator=evaluator,
    nextStates=nextStates,
    player="p1",
    state=startState)
printTrace(statePrinter=statePrinter, level=1,trace=trace)