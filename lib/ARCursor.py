import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

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


cursor = Cursor()


def move(img):
    hands = detector.findHands(img, draw=False)

    if hands:
        hand1 = hands[0]
        lmList1, bbox1 = hand1["lmList"], hand1["bbox"]

        if lmList1:
            l, _ = detector.findDistance(
                lmList1[8], lmList1[12], img, draw=False)

            cursor.updatePos(lmList1[8], l)
            cv2.circle(img, cursor.pos, 20, (231, 231, 231), -1)

def getCursor():
    return cursor.getPos()
