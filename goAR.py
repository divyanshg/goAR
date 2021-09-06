import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone
import asyncio
import time

elmList = []

detector = HandDetector(detectionCon=0.8)
clickThreshold = 30

class Cursor:
    def __init__(self) -> None:
        self.pos = (0, 0)
        self.l = 0

    def updatePos(self, pos, l):
        self.pos = pos
        self.l = l

    def getPos(self):
        return self.pos, self.l

    def move(self, img):
        hands = detector.findHands(img, draw=False)

        if hands:
            hand1 = hands[0]
            lmList1, bbox1 = hand1["lmList"], hand1["bbox"]

            if lmList1:
                l, _ = detector.findDistance(
                    lmList1[8], lmList1[12], img, draw=False)

                self.updatePos(lmList1[8], l)
                cv2.circle(img, cursor.pos, 20, (231, 231, 231), -1)


cursor = Cursor()


def getCursor():
    return cursor.getPos()

class Rect():
    def __init__(self, id, text, posCenter, size=[200, 200], isDraggable=True, isClickable=True, color=(246, 203, 128), focusColor=(239, 179, 75)) -> None:
        self.id = id
        self.posCenter = posCenter
        self.size = size

        self.isDraggable = isDraggable
        self.isClickable = isClickable

        self.callback = None
        self.dragCallback = None
        self.dragLeaveCallb = None

        self.text = text

        self.color = color
        self.focusColor = focusColor
        self.oldColor = color

        elmList.append(self)

    def draw(self, img):
        cx, cy = self.posCenter
        w, h = self.size

        cv2.rectangle(img, (cx-w//2, cy-h//2),
                      (cx+w//2, cy+h//2), self.color, cv2.FILLED)
        cv2.putText(img, str(self.text), (cx+(w//2) // 2, cy-(h//2) // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        cvzone.cornerRect(img, (cx - w // 2, cy - h // 2,
                                w, h), 20, t=2, rt=0, colorR=self.color)

    def onClick(self, callback=None):
        self.callback = callback

    def onclick(self, cursor, callback=None):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # self.posCenter = cursor
            if self.isClickable:
                if self.callback is not None:
                    self.callback(self)

    def onEnter(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # self.posCenter = cursor
            self.color = self.focusColor
        else:
            self.color = self.oldColor

    def onDrag(self, dragCallback=None):
        self.dragCallback = dragCallback
    def onDragLeave(self, callback=None):
        self.dragLeaveCallb = callback

    def ondrag(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            if self.isDraggable:
                if self.dragCallback is not None:
                    self.dragCallback(self)
                self.posCenter = cursor
        else: 
            if self.dragLeaveCallb is not None:
                self.dragLeaveCallb(self)


class Circle():
    def __init__(self, id, text, posCenter, radius=100, thickness=-1, isDraggable=True, isClickable=True, color=(246, 203, 128), focusColor=(239, 179, 75)) -> None:
        self.id = id
        self.posCenter = posCenter
        self.radius = radius
        self.size = [radius*2, radius*2]

        self.isDraggable = isDraggable
        self.isClickable = isClickable

        self.callback = None
        self.dragCallback = None
        self.dragLeaveCallb = None

        self.text = text

        self.color = color
        self.focusColor = focusColor
        self.oldColor = color

        elmList.append(self)

    def draw(self, img):
        cx, cy = self.posCenter

        cv2.circle(img, (cx, cy),
                      self.radius, self.color, cv2.FILLED)
        cv2.putText(img, str(self.text), (cx - 50, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        # cvzone.cornerRect(img, (cx - w // 2, cy - h // 2,
        #                         w, h), 20, t=2, rt=0, colorR=self.color)

    def onClick(self, callback=None):
        self.callback = callback

    def onclick(self, cursor, callback=None):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # self.posCenter = cursor
            if self.isClickable:
                if self.callback is not None:
                    self.callback(self)

    def onEnter(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # self.posCenter = cursor
            self.color = self.focusColor
        else:
            self.color = self.oldColor

    def onDrag(self, dragCallback=None):
        self.dragCallback = dragCallback

    def onDragLeave(self, callback=None):
        self.dragLeaveCallb = callback

    def ondrag(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            if self.isDraggable:
                if self.dragCallback is not None:
                    self.dragCallback(self)
                self.posCenter = cursor
        else:
            if self.dragLeaveCallb is not None:
                self.dragLeaveCallb(self)


dragThreshold = 30


def stopwatch():
    start = time.time()
    elapsed = 0
    while True:
        elapsed = time.time() - start
    return elapsed

def catchCursor():
    cursor, l = getCursor()

    for elm in elmList:
        elm.onEnter(cursor)

    if 30 < l < 40:
        # # if stopwatch(1):
        for elm in elmList:
            elm.onclick(cursor)
        # print(stopwatch())
    
    if l < dragThreshold:
        for elm in elmList:
            elm.ondrag(cursor)
