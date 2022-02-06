#IMPROVEMENTS
#depth-search limit
#search heuristics
#hash-table of considered states to avoid redoing work


#datatype trace: state -> (next state -> trace) map

class Trace:
    def __init__(self,state,traceMap):
        self.state = state
        self.traceMap = traceMap
        #minValue

def obtainTrace(evaluator,nextStates,player,state):
    trace = None
    #is it our turn
    if state.player == player:#yes
        next_states = nextStates(state)
        #did we reach the end-state?
        if next_states != []: #no
            #process first possibility
            nextState,*tail = next_states
            maxminTrace = obtainTrace(evaluator,nextStates,player,nextState)
            #process other possibilities
            for nextState in tail:
                #get trace resulting from this move
                nextTrace = obtainTrace(evaluator,nextStates,player,nextState)
                #is worst case scenario better than the other best possibility?
                if nextTrace.minValue > maxminTrace.minValue:
                    maxminTrace = nextTrace
            trace = Trace(state,{maxminTrace.state : maxminTrace})
            trace.minValue = maxminTrace.minValue
        else: #yes
            trace = Trace(state,{})
            trace.minValue = evaluator(state)
    else:#no
        next_states = nextStates(state)
        #did we reach the end-state?
        if next_states != []: #no
            #process first possibility
            nextState,*tail = next_states
            nextTrace = obtainTrace(evaluator,nextStates,player,nextState)
            traceMap = {nextState:nextTrace}
            minValue = nextTrace.minValue
            #process other possibilities
            for nextState in next_states:
                #get trace resulting from this move
                nextTrace = obtainTrace(evaluator,nextStates,player,nextState)
                #add to map of possible opponent moves
                traceMap[nextState] = nextTrace
                #is this worst case scenario?
                if nextTrace.minValue < minValue:
                    minValue = nextTrace.minValue
            trace = Trace(state,traceMap)
            trace.minValue = minValue
        else:#yes
            trace = Trace(state,{})
            trace.minValue = evaluator(state)
    return trace

def printTrace(statePrinter,level,trace):
    statePrinter(trace.state)
    for k in trace.traceMap:
        printTrace(statePrinter,level + 1,trace.traceMap[k])
        print("-" * level)
