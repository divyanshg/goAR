import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

detector = HandDetector(detectionCon=0.8)
clickThreshold = 30


