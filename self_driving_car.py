import pyautogui as py
import matplotlib.pyplot as plt
import cv2
import numpy as np
import win32api, win32con, keyboard
import time

def click(x = 420, y = 230):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def accellerate(hold_time = 2):
    #click()
    start = time.time()
    while time.time() - start < hold_time:
        py.keyDown('w')
    py.keyUp('w')

def breaks(hold_time = 2):
    #click()
    start = time.time()
    while time.time() - start < hold_time:
        py.keyDown(' ')
    py.keyUp(' ')

def turnLeft(hold_time = 1):
    #click()
    start = time.time()
    while time.time() - start < hold_time:
        py.keyDown('a')
    py.keyUp('a')

def turnRight(hold_time = 1):
    #click()
    start = time.time()
    while time.time() - start < hold_time:
        py.keyDown('d')
    py.keyUp('d')


def imshow(image):
    cv2.imshow("something", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
def takeScreenShot():
    im = py.screenshot("screen.jpg", region=(70, 150, 915, 420)) #parameter to change
    #plt.imshow(im)
    return im

def canny(image):
    image = np.array(image)
    gray_game_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = 9
    blurred_game_img = cv2.GaussianBlur(gray_game_img, (kernel, kernel), 0)
    corroded_img = cv2.erode(blurred_game_img, np.ones((3,3), dtype = np.uint8), iterations=1)
    canned_game_img = cv2.Canny(corroded_img, 50, 100)
    return canned_game_img

def ROI(image):
    height, width = image.shape[:2]
    mask = np.zeros_like(image)
    p1 = (0, 325) #parameter to change
    p2 = (width, 325) #parameter to change
    p3 = (500, 230) #parameter to change
    p4 = (420, 230) #parameter to change
    polygon = np.array([[p1, p2, p3, p4]])
    polygon_portion = cv2.fillPoly(mask, polygon, 255)
    polygon_portion_image = cv2.bitwise_and(image, polygon_portion)
    return polygon_portion_image

def houghLines(image):
    rho = 2  # distance resolution in pixels
    theta = np.pi / 180  # angular resolution in radians
    threshold = 40  # minimum number of votes
    min_line_len = 50  # minimum number of pixels making up a line
    max_line_gap = 50  # maximum gap in pixels between connectable line segments
    houghLines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return houghLines

def plotImageLines(color_image, masked_image, lines):
    line_image = np.zeros((masked_image.shape[0], masked_image.shape[1], 3), dtype=np.uint8)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), [255, 0, 0], 20)

    α = 1
    β = 1
    γ = 0

    Image_with_lines = cv2.addWeighted(color_image, α, line_image, β, γ)
    fig, ax = plt.subplots(1,2, figsize = (10, 5))
    ax[0].imshow(masked_image)
    ax[1].imshow(Image_with_lines)
    plt.savefig('lanes_in_image.jpg')
    plt.show()

def make_points(img, lineSI):
    slope, intercept = lineSI
    height, width = img.shape[:2]
    y1 = int(height)
    y2 = int(height * 0.5)
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
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
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)

    height, width = image.shape[:2]
    center_line = [[0, int(width/2), height, int(width/2)]]
    average = [left_line, right_line]

    lSlope, lIntercept = left_fit_average
    rSlope, rIntercept = right_fit_average
    print(lSlope, rSlope)

    threshold_l = 0.340 #parameter to change
    threshold_r = 0.340 #parameter to change
    '''you can get your tresholds by looking at the output print(lSlope, rSlope)
    get a left value smaller than the one from the print and a right value larger than the one from the print
    to get the values, try to lineup the car on your lane pefectly so that it is parallel to the lane lines
    before doing that comment the next lines ...'''
    #..................................
    if lSlope < -threshold_l:
        turnRight(0.1)
        print("right")
    if rSlope > threshold_r:
        turnLeft(0.1)
        print("left")
    # ..................................
    return average

click()
# i = 0
# while i < 10:
image = takeScreenShot()
image = np.array(image)
canned_image = canny(image)
canned_image = cv2.dilate(canned_image, np.array((3,3), dtype = np.uint8), 3)
my_show = ROI(canned_image)
hough_lines = houghLines(my_show)
avg_lines = average_slope_intercept(image, hough_lines)
#accellerate(0.105)
avg_lines = average_slope_intercept(image, hough_lines)
print(avg_lines)

plotImageLines(image, my_show, avg_lines) # use this to see the average lines in a plot