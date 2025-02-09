# Self-Driving Car Project in a Game
---
game: https://www.crazygames.com/game/3d-car-simulator
---

This project serves as a repository for the video __[Self-Driving Car in a Game](https://www.youtube.com/watch?v=OzPakNSU0gU)__. The code from the video is somewhat incomplete and primarily serves as a proof of concept. If you want to get the code from the video (slightly tweaked with some new functions), take the first version of `app.py`. Here are instructions on how to use the first version. Otherwise, keep scrolling to version 2 and beyond.

### V1 `app.py`:

This version is a copy of the code from the video, with an additional `plotImageLines(color_image, masked_image, lines)` function to plot the lane lines.

If you want to use this code, make sure to change the following:

- `im = py.screenshot("screen.jpg", region=(70, 150, 915, 420))`
    - Located in the `takeScreenShot()` module.
    - More about it on [Watch this video at 2:30](https://www.youtube.com/watch?v=OzPakNSU0gU)

- Region of interest points:
    ```python
    p1 = (0, 325) # parameter to change
    p2 = (width, 325) # parameter to change
    p3 = (500, 230) # parameter to change   
    p4 = (420, 230) # parameter to change
    ```
    - Located in the `ROI(image)` module.
    - More about it on [Watch this video at 15:00](https://www.youtube.com/watch?v=OzPakNSU0gU)

- `threshold_l`, `threshold_r`:
    ```python
    threshold_l = 0.340 # parameter to change
    threshold_r = 0.340 # parameter to change

    if lSlope < -threshold_l:
        turnRight(0.1)
        print("right")
    if rSlope > threshold_r:
        turnLeft(0.1)
        print("left")
    ```
    - Located in the `average_slope_intercept(image, lines)` module.
    - More about it on [Watch this video at 8:00](https://www.youtube.com/watch?v=J3SqAEKu-xQ)

Keep in mind, this version is quite far from being automatic, and it requires some tinkering before it can work
- **Limitations of V1 `app.py`:**
    - This version is quite bad and requires some tinkering before it can work 😁.
    - The code will work only at speeds of around 5 km/h.
    - It won't work if there is a missing lane or if the lane is outside the region of interest (simply put: out of car view).
    - This code is supposed to work only with certain cars in 1st person driving (police car and rally car).

### V2: ...ongoing...
