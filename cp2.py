import cv2
import mediapipe as mp


video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils

while True:
    check, img = video.read()
    imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRgb)
    handsPoints = results.multi_hand_landmarks

    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points,hand.HAND_CONNECTIONS)

    cv2.imshow("Imagem", img)
    cv2.waitKey(1)