import cv2
import numpy as np
import win32api, win32con
import time
import math

from car_commands import CarCommands
from computer_vision import ComputerVision


# def plotImageLines(color_image, masked_image, lines):
#     line_image = np.zeros((masked_image.shape[0], masked_image.shape[1], 3), dtype=np.uint8)
#
#     for line in lines:
#         for x1, y1, x2, y2 in line:
#             cv2.line(line_image, (x1, y1), (x2, y2), [255, 0, 0], 20)
#
#     α = 1
#     β = 1
#     γ = 0
#
#     Image_with_lines = cv2.addWeighted(color_image, α, line_image, β, γ)
#     fig, ax = plt.subplots(1, 2, figsize=(10, 5))
#     ax[0].imshow(masked_image)
#     ax[1].imshow(Image_with_lines)
#     plt.show()


def click(x=420, y=230):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

class CompleteControl(CarCommands, ComputerVision):
    def __init__(self, x1 = 70, y1 = 150, x2 = 915, y2 = 420):
        self.screen_region = (x1, y1, x2, y2)

    def make_points(self, img, lineSI):
        slope, intercept = lineSI
        height, width = img.shape[:2]
        y1 = int(height)
        y2 = int(height * 0.5)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return [[x1, y1, x2, y2]]

    def average_slope_intercept(self, lines):
        left_fit = []
        right_fit = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                fit = np.polyfit((x1, x2), (y1, y2), 1)
                slope = fit[0]
                intercept = fit[1]

                if slope < 0:
                    left_fit.append((slope, intercept))
                elif slope >= 0:
                    right_fit.append((slope, intercept))
        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        return left_fit_average, right_fit_average

    def check_for_lanes(self, left_fit_average, right_fit_average):
        if not math.isnan(np.sum(left_fit_average)):
            left_line = self.make_points(self.img, left_fit_average)
            l_slope, l_intercept = left_fit_average
        else:
            left_line = None
            l_slope = 0.1

        if not math.isnan(np.sum(right_fit_average)):
            right_line = self.make_points(self.img, right_fit_average)
            r_slope, r_intercept = right_fit_average
        else:
            right_line = None
            r_slope = 0.9
        return l_slope, r_slope


    def get_car_steering(self, l_slope, r_slope):
        #print(lSlope, rSlope)
        threshold_l = 0.340
        threshold_r = 0.340
        if l_slope < -threshold_l:
            self.turnRight(0.05)

        if r_slope > threshold_r:
            self.turnLeft(0.05)


    def __call__(self):
        click()
        while True:
            self.take_screen_shot()
            canned_image = self.canny(self.img)
            canned_image = cv2.dilate(canned_image, np.array((3, 3), dtype=np.uint8), 3)
            my_show = self.region_of_interest(canned_image)
            hough_lines = self.Hough_lines(my_show)
            left, right = self.average_slope_intercept(hough_lines)
            left_slope, right_slope = self.check_for_lanes(left, right)
            self.get_car_steering(left_slope,right_slope)
            self.accellerate(0.1)
            avg_lines = self.average_slope_intercept(hough_lines)
            print(avg_lines)

            # Wait for 1 ms and check if the Esc key (27) is pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break

if __name__ == "__main__":
    o = CompleteControl()
    o()

# plotImageLines(image, my_show, avg_lines)
# fig, ax = plt.subplots(1,2, figsize = (10,5))
# ax[0].imshow(canned_image)
# ax[1].imshow(my_show)
# plt.show()
