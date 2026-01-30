import cv2
import observe_positions
import numpy as np

obj_len = 5.3 # in
obj_len_px = 201 # px
obj_hsv = [71, 3, 255]

in_per_px = obj_len / obj_len_px

# calibrate in_per_px var
# 1) Get object with known length (y)
# 2) Run and stop script. Look for smallest "y px" value
# 3) Record new obj_len_px with the observed "y px"
# 4) Run script and verify obj_len matches "y in"
def calibrate_x_y_scale(cap):
    while True:

        img, frame, max0, max1 = observe_positions.find_objects(cap)

        _, y, _ = max0

        cv2.imshow('Frame' , img)

        print(f"y px {y}")
        print(f"y in  {y * in_per_px}")

        if cv2.waitKey(1) == ord('q'):
            break


# calibrate in_per_px var
# 1) Run script and move object to center
# 2) revord HSV valeus in obj_hsv as (h, s, v)
def calibrate_obj_hsv(cap, square_size=20):

    # The values will be in OpenCV's default ranges:
    # H: [0, 179], S: [0, 255], V: [0, 255]

    while True:

        ret, img = cap.read()

        half_side = square_size // 2
        
        height, width = img.shape[:2]
        y_start = height // 2 - half_side
        y_end = height // 2 + half_side
        x_start = width // 2 - half_side
        x_end = width // 2 + half_side

        roi_bgr = img[y_start:y_end, x_start:x_end]
        hsv_image = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)
        mean_hsv = cv2.mean(hsv_image)

        cv2.line(img, (0, height // 2), (width, height // 2), (255, 0, 0), 2)
        cv2.line(img, (width // 2,0), (width // 2, height), (255, 0, 0), 2)

        print(f"H, S, V: {mean_hsv[0]:.1f}, {mean_hsv[1]:.1f}, {mean_hsv[2]:.1f}")

        cv2.imshow('Frame' , img)

        if cv2.waitKey(1) == ord('q'):
                break


# select which calibration process to run
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    # calibrate_x_y_scale(cap)

    calibrate_obj_hsv(cap)

    cap.release()
    cv2.destroyAllWindows()