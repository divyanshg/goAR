import cv2
from goAR import ARCursor
from goAR import ARElements
from goAR import catchCursor
import requests
import time

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 1080)

btn1 = ARElements.Rect("btn1", "Get Users", [150, 150],size=[50, 50], isDraggable=False)
btn2 = ARElements.Circle("btn2", "Draggable", [450, 150], isDraggable=True)


def getUsers(e):
    # res = requests.get("http://api.open-notify.org/astros.json")
    # print(res.json())
    print("hello")
    # time.sleep(5)

def onDragg(e):
    e.text = "Dragging"


def onNoDrag(e):
    e.text = "Draggable"

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    ARCursor.move(frame)
    catchCursor()

    btn1.draw(frame)
    btn1.onClick(getUsers)

    btn2.draw(frame)
    btn2.onDrag(onDragg)
    btn2.onDragLeave(onNoDrag)

    cv2.imshow("MAIN", frame)
    cv2.waitKey(1)

