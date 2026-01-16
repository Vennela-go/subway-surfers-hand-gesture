import cv2
import time
import pyautogui
from gesture_recognition import handDetector

pyautogui.FAILSAFE = False

def detectGesture(fingers):
    if fingers == [0, 1, 0, 0, 0]:
        pyautogui.press('up')
        return "Jump"

    elif fingers == [1, 1, 0, 0, 0]:
        pyautogui.press('down')
        return "Roll"

    elif fingers == [0, 1, 1, 0, 0]:
        pyautogui.press('right')
        return "Move Right"

    elif fingers == [1, 0, 0, 0, 0]:
        pyautogui.press('left')
        return "Move Left"

    elif fingers == [1, 1, 1, 1, 1]:
        pyautogui.press('space')
        return "Hoverboard"

    return "No Action"


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    pTime = 0
    lastGestureTime = 0
    cooldown = 0.6
    gesture = ""

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        currentTime = time.time()
        if lmList and (currentTime - lastGestureTime) > cooldown:
            fingers = detector.fingersUp()
            gesture = detectGesture(fingers)
            print("Gesture:", gesture)
            lastGestureTime = currentTime

        # FPS
        cTime = time.time()
        fps = int(1 / (cTime - pTime)) if cTime != pTime else 0
        pTime = cTime

        cv2.putText(img, f'FPS: {fps}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(img, f'Gesture: {gesture}', (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Subway Surfers Hand Gesture Control", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
