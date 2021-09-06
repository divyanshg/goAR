import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import urllib.request
import numpy as np

cap = cv2.VideoCapture(0)  # 'rtsp://10.1.1.100:8080/h264_ulaw.sdp'
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

clickThreshold = 30

# cx, cy, w, h = 100, 100, 200, 200

class Rect():
    def __init__(self, id, posCenter, size=[200, 200], isDraggable=True, isClickable=True, color=(246, 203, 128), focusColor=(239, 179, 75)) -> None:
        self.id = id
        self.posCenter = posCenter
        self.size = size

        self.isDraggable = isDraggable
        self.isClickable = isClickable

        self.color = color
        self.focusColor = focusColor
        self.oldColor = color

    def onClick(self, cursor, callback):
        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # self.posCenter = cursor
            if self.isClickable:
                callback(self.id)
                print("clicked : " + str(self.id))  

    def onEnter(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # self.posCenter = cursor
            self.color = self.focusColor
        else: 
            self.color = self.oldColor

    def onDrag(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size


        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            if self.isDraggable:
                self.posCenter = cursor

rectList = []
for x in range(4):
    rectList.append(Rect(x, [x*250+150, 150]))

btn1 = Rect("fixed", [150, 150], color=(75, 148, 239), isDraggable=False, focusColor=(43, 130, 238))


def sayHello(id):
    print("helloo from : " + str(id))

while True:
    success, img = cap.read()

    hands, img = detector.findHands(img, draw=True)

    # lmList1, lmList2 = "", ""

    if hands:
        hand1 = hands[0]
        lmList1, bbox1 = hand1["lmList"], hand1["bbox"]

        # if len(hands) > 1:
        #     hand2 = hands[1]
        #     lmList2, bbox2 = hand2["lmList"], hand2["bbox"]

        # if lmList1 and lmList2:
        #     l, _, _ = detector.findDistance(
        #         lmList1[8] and lmList2[8], lmList1[12] and lmList2[12], img)
        #     cursor = lmList1[8] and lmList2[8]

        if lmList1:
            l, _, _ = detector.findDistance(
                lmList1[8], lmList1[12], img)
            
            cursor = lmList1[8]

            for rect in rectList:
                rect.onEnter(cursor)

            if 30 < l < 40:
                # btn1.onClick(cursor, sayHello)
                for rect in rectList:
                    rect.onClick(cursor)
            
            if l < clickThreshold:
                for rect in rectList:
                    rect.onDrag(cursor)

    #Draw with transparency

    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        
        cv2.rectangle(imgNew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), rect.color , cv2.FILLED)
        cv2.putText(imgNew, str(rect.id), (cx-w//2, cy-h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2 )
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0, colorR=rect.color)

    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    #Draw solid rectangle
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size

    #     cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR , cv2.FILLED)
    #     cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0, colorR=colorR)


    cv2.imshow("Camera", out)
    cv2.waitKey(1)
