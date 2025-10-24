import cv2
import numpy as np
import os
import HandTrackingModule as htm

#######################
brushThickness = 25
eraserThickness = 100
########################

# Create Header folder if it doesn't exist
if not os.path.exists("Header"):
    os.makedirs("Header")
    img1 = np.ones((125, 200, 3), np.uint8) * 255
    img1[:,:] = (255, 0, 255)  # Purple
    img2 = np.ones((125, 200, 3), np.uint8) * 255
    img2[:,:] = (255, 0, 0)    # Blue
    img3 = np.ones((125, 200, 3), np.uint8) * 255
    img3[:,:] = (0, 255, 0)    # Green
    img4 = np.ones((125, 200, 3), np.uint8) * 255
    img4[:,:] = (0, 0, 0)      # Black/Eraser
    cv2.imwrite("Header/1.png", img1)
    cv2.imwrite("Header/2.png", img2)
    cv2.imwrite("Header/3.png", img3)
    cv2.imwrite("Header/4.png", img4)

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0] if overlayList else np.zeros((125, 1280, 3), np.uint8)
drawColor = (255, 0, 255)

# Use camera index 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.7, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 4), np.uint8)  # BGRA format

while True:
    # 1. Import image
    success, img = cap.read()
    if not success or img is None:
        print("Failed to get frame from camera")
        continue
    # print(f"Frame shape: {img.shape}")  # Debug: Check frame dimensions
    
    # Resize and flip image
    img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img, draw=True)  # Skip drawing landmarks
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        # 4. If Selection Mode - Two fingers are up
        if fingers[1] and fingers[2]:
            print("Selection Mode")
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0] if len(overlayList) > 0 else header
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1] if len(overlayList) > 1 else header
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2] if len(overlayList) > 2 else header
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3] if len(overlayList) > 3 else header
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            thickness = eraserThickness if drawColor == (0, 0, 0) else brushThickness
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor + (255,), thickness)

            xp, yp = x1, y1

        # Clear Canvas when all fingers are up
        if all(fingers):
            imgCanvas = np.zeros((720, 1280, 4), np.uint8)
            xp, yp = 0, 0

    # Extract BGR and alpha from canvas
    canvas_bgr = imgCanvas[:, :, :3]
    canvas_alpha = imgCanvas[:, :, 3] / 255.0  # Normalize alpha to [0, 1]

    # Blend canvas with camera feed
    for c in range(3):
        img[:, :, c] = (canvas_bgr[:, :, c] * canvas_alpha + img[:, :, c] * (1.0 - canvas_alpha)).astype(np.uint8)

    # Setting the header image
    try:
        h, w, c = header.shape
        img_output[0:h, 0:w] = header
    except:
        pass

    cv2.imshow("Image", img)  # Display camera feed with landmarks
    # cv2.imshow("Canvas", cv2.cvtColor(imgCanvas[:, :, :3], cv2.COLOR_BGR2RGB))  # Debug canvas

    key = cv2.waitKey(1)
    if key == 27:  # ESC key to break
        break

cap.release()
cv2.destroyAllWindows()