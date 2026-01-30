import cv2
import numpy as np
import calibration as cali

# finds biggest 2 object
# input: capture obj
# output: tuple (image with bound rects, binary frame, biggest obj xyzwh, second biggest obj xyzwh)
def find_objects(cap, hue_range=25):
    # capture frame-by-frame
    ret, img = cap.read()

    # convert to HSV
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # filter by target HSV range
    lower_bound = np.array([cali.obj_hsv[0] - hue_range, 1, 200])
    upper_bound = np.array([cali.obj_hsv[0] + hue_range, 25, 255])
    frame = cv2.inRange(frame, lower_bound, upper_bound)

    # dilate to improve edge detection
    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=3)
    # frame = cv2.erode(frame, kernel, iterations=1)

    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max0 = (1, 1, 1) # x, y, area (biggest)
    max1 = (0, 0, 0) # x, y, area (second biggist)
    for cnt in contours:
        # calculate the bounding rectangle
        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h
        if area > max1[2]:
            if area > max0[2]:
                max1 = max0
                max0 = (x + w // 2, y + h // 2, area) # center x and y instead of right corner
            else:
                max1 = (x + w // 2, y + h // 2, area)
        
        # draw the rectangle on the original image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2) # red with thickness 2

    return img, frame, max0, max1


# get position of right most object based on left most object as origin
# TODO: in final version take loop out of fuction and place in main. also remove imshow, waitkey, and test prints
def get_x_y_relative(cap):
    while True:
        img, frame, max0, max1 = find_objects(cap)

        leftMost = None
        rightMost = None
        
        if max0[0] >= max1[0]:
            rightMost = max0
            leftMost = max1
        else:
            rightMost = max1
            leftMost = max0

        x = (leftMost[0] - rightMost[0]) * cali.in_per_px
        y = -(leftMost[1] - rightMost[1]) * cali.in_per_px # flip sign since y points down in image coord while traditional 2d coord points up

        height, width = img.shape[:2]
        cv2.line(img, (rightMost[0], 0), (rightMost[0], height), (255, 0, 0), 2)
        cv2.line(img, (leftMost[0], 0), (leftMost[0], height), (0, 255, 0), 2)

        cv2.line(img, (0, rightMost[1]), (width, rightMost[1]), (255, 0, 0), 2)
        cv2.line(img, (0, leftMost[1]), (width, leftMost[1]), (0, 255, 0), 2)

        cv2.imshow('Processed Frame', frame)
        cv2.imshow('Original Frame' , img)

        print(f"x, y (in): {x:.1f}, {y:.1f}")

        print(f"Left x: {leftMost}")
        print(f"Right x: {rightMost}")

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    get_x_y_relative(cap)

    cap.release()
    cv2.destroyAllWindows()