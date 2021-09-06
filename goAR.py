import lib.ARCursor as ARCursor
import lib.ARElements as ARElements


dragThreshold = 30


# def stopwatch():
#     start = time.time()
#     elapsed = 0
#     while True:
#         elapsed = time.time() - start
#     return elapsed

def catchCursor():
    cursor, l = ARCursor.getCursor()

    for elm in ARElements.elmList:
        elm.onEnter(cursor)

    if 30 < l < 40:
        # # if stopwatch(1):
        for elm in ARElements.elmList:
            elm.onclick(cursor)
        # print(stopwatch())

    if l < dragThreshold:
        for elm in ARElements.elmList:
            elm.ondrag(cursor)
