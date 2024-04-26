import cv2
import mediapipe as mp

def detect_hand_landmarks(image, Hand, w, h):
    imgRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRgb)
    handsPoints = results.multi_hand_landmarks
    pontos = []
    if handsPoints:
        for points in handsPoints:
            for cord in points.landmark:
                cx, cy = int(cord.x * w), int(cord.y * h)
                pontos.append((cx, cy))
    return pontos

def print_finger_status(prev_status, current_status, finger_name):
    if prev_status != current_status:
        print(f'{finger_name}: {"tecla solta" if current_status else "apertado"}')
    return current_status

def main():
    video = cv2.VideoCapture(0)
    hand = mp.solutions.hands
    Hand = hand.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    prev_finger_status = [False] * 5  # Assuming all fingers are initially pressed
    while True:
        check, img = video.read()
        h, w, _ = img.shape

        pontos = detect_hand_landmarks(img, Hand, w, h)

        if pontos:
            # Checking finger status
            current_finger_status = [
                pontos[4][0] > pontos[1][0],
                pontos[6][1] > pontos[8][1],
                pontos[10][1] > pontos[12][1],
                pontos[14][1] > pontos[16][1],
                pontos[18][1] > pontos[20][1],

            ]

            # Printing finger status only if there's a change
            for i, status in enumerate(current_finger_status):
                prev_finger_status[i] = print_finger_status(prev_finger_status[i], status, f'dedo {i+1}')

        cv2.imshow("Imagem", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
