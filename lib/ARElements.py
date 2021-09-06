import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone
import asyncio
import time

elmList = []


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

