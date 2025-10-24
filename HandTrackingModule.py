import cv2
import mediapipe as mp
import time
import math
import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode, 
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon, 
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.lmList = []

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                    self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList) if xList else 0, max(xList) if xList else 0
            ymin, ymax = min(yList) if yList else 0, max(yList) if yList else 0
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                (0, 255, 0), 2)

        return self.lmList

    def fingersUp(self):
        fingers = []
        # Thumb
        if len(self.lmList) > 0:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        else:
            fingers = [0, 0, 0, 0, 0]

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        if len(self.lmList) > 0:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]
        return 0, img, [0, 0, 0, 0, 0, 0]

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector(detectionCon=0.7, maxHands=1)  # Only track one hand
    
    # Dictionary to map finger indices to names for better output
    finger_names = {
        0: "Thumb",
        1: "Index",
        2: "Middle",
        3: "Ring",
        4: "Pinky"
    }
    
    # Counter to control how often we print (to avoid flooding the console)
    frame_count = 0
    
    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Failed to get frame from camera")
            continue
            
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        
        # Print finger status only if hand is detected
        if len(lmList) != 0:
            # Get fingers status (up or down)
            fingers = detector.fingersUp()
            
            # Only print every 10 frames to avoid console flooding
            frame_count += 1
            if frame_count % 10 == 0:
                # Clear previous output line
                print("\033[K", end='\r')
                
                # Count how many fingers are up
                total_up = sum(fingers)
                
                # Print which specific fingers are up
                up_fingers = [finger_names[i] for i, is_up in enumerate(fingers) if is_up]
                
                # Print info on the same line
                status_text = f"Fingers up: {total_up} - {', '.join(up_fingers) if up_fingers else 'None'}"
                print(status_text, end='\r')
                
                # Also display on image
                cv2.putText(img, f"Fingers: {total_up}", (10, 120), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
        (255, 0, 255), 3)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to break
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print()  # Print a newline to clean up terminal after closing

if __name__ == "__main__":
    main()