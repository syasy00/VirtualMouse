import cv2 #STEP 1: Open Video Camera // for computer vision
import mediapipe as mp # for hand tracking
import pyautogui #control mouse

cap = cv2.VideoCapture(0) #initialize video capture (0) to access default camera
hand_detector = mp.solutions.hands.Hands() #create instances of mediapipe class for hand tracking
drawing_utils = mp.solutions.drawing_utils # for drawing utilities
screen_width, screen_height = pyautogui.size() #to get screen dimension using pyautogui
thumb_y = 0

while True:  #starts with infinite loop
    _, frame = cap.read() #continuously capture the frame from camera
    frame = cv2.flip(frame, 1) #the frame is flip horizontally
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # and the frame need to convert to rgb format as media pipe requires input in this format

    output = hand_detector.process(rgb_frame) #process the rgb frame using the mediapipe hand detector
    hands = output.multi_hand_landmarks #the detected landmark are stored in the hands variable

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)

                if id == 0: #palm finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0,255,255))
                    palm_x = screen_width/frame_width*x
                    palm_y = screen_height/frame_height*y
                    pyautogui.moveTo(palm_x, palm_y) #controlling the cursor

                if id == 4:  # thumb finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                if id == 12: #middle finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0,255,255))
                    middle_x = screen_width/frame_width*x
                    middle_y = screen_height/frame_height*y
                    if abs(middle_y - thumb_y) < 40: # distance of middle and thumb is <20px
                        print('Performing scroll-up')
                        pyautogui.scroll(90) #to scroll up website
                        pyautogui.sleep(1)

                if id == 16: #ring
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0,255,255))
                    ring_x = screen_width/frame_width*x
                    ring_y = screen_height/frame_height*y
                    if abs(ring_y - thumb_y) < 40: # distance of ring and thumb is <20px
                        print('Performing scroll-down')
                        pyautogui.scroll(-90) # to scrol down a website
                        pyautogui.sleep(1)

                if id == 8: #index finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0,255,255))
                    index_y = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    if abs(index_y - thumb_y) < 40: # distance of index and thumb is <20px
                        print('Performing left-click')
                        pyautogui.click() #to perform left hand click
                        pyautogui.sleep(1)

                if id == 20: #pinky finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    pinky_x = screen_width / frame_width * x
                    pinky_y = screen_height / frame_height * y
                    if abs(pinky_y - thumb_y) < 40: # distance of pinky and thumb is <20px
                        print('Performing right-click')
                        pyautogui.rightClick() #to perform right hand click
                        pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)