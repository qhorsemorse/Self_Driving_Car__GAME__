import cv2
import numpy as np
import pyautogui as py

class ComputerVision:
    def __init__(self, x1 = 70, y1 = 150, x2 = 915, y2 = 420):
        self.screen_region = (x1, y1, x2, y2)

    def take_screen_shot(self):
        img = np.array(py.screenshot("screen.jpg", region = self.screen_region))
        self.img = img
        return img

    @staticmethod
    def region_of_interest(canny_image):
        height, width = canny_image.shape[:2]
        mask = np.zeros_like(canny_image)
        p1 = (0, 325)
        p2 = (width, 325)
        p3 = (500, 230)
        p4 = (420, 230)
        polygon = np.array([[p1, p2, p3, p4]])
        polygon_portion = cv2.fillPoly(mask, polygon, 255)
        polygon_portion_image = cv2.bitwise_and(canny_image, polygon_portion)
        return polygon_portion_image

    @staticmethod
    def canny(image):
        gray_game_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = 9
        blurred_game_img = cv2.GaussianBlur(gray_game_img, (kernel, kernel), 0)
        corroded_img = cv2.erode(blurred_game_img, np.ones((3, 3), dtype=np.uint8), iterations=1)
        canned_img = cv2.Canny(corroded_img, 50, 100)
        return canned_img

    @staticmethod
    def Hough_lines(roi_image):
        rho = 2  # distance resolution in pixels
        theta = np.pi / 180  # angular resolution in radians
        threshold = 40  # minimum number of votes
        min_line_len = 50  # minimum number of pixels making up a line
        max_line_gap = 50  # maximum gap in pixels between connectable line segments
        hough_lines = cv2.HoughLinesP(roi_image, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                                     maxLineGap=max_line_gap)
        return hough_lines

