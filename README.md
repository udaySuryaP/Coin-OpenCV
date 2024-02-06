# Coin Counting and Serial Communication System

## Description

This Python script utilizes OpenCV and computer vision techniques to detect and count coins in a video stream. It then communicates the total count to an Arduino board via serial communication.

## Dependencies

- Python 3.x
- OpenCV (cv2)
- cvzone
- NumPy (np)
- Serial library

## Installation

Install required libraries: `pip install opencv-python cvzone numpy pyserial`

## Usage

1. Connect your Arduino board to your computer.
2. Adjust the serial port in the script (ser = serial.Serial('COM4', 9600)) to match your Arduino's port.
3. Run the script: `python main.py`

## Code Structure

Key Functions:

- preProcessing(img): Applies image processing techniques to enhance coin visibility.
- findContours(img, imgPre, minArea): Detects contours of potential coins in the image.
- update(imgCrop, hsvVals): Uses color segmentation to refine coin detection.

Main Loop:

1. Captures video frames from the webcam.
2. Preprocesses each frame.
3. Finds contours and identifies coins based on area and color.
4. Calculates the total money value based on counted coins.
5. Displays the processed image with detected coins and total count.
6. Sends the total money value to the Arduino via serial communication.

## Additional Notes

- The Settings window and trackbars are currently unused.
- The script assumes a specific color range for coins (hsvVals). Adjust this if needed.
- Consider adding error handling and optimization for real-world use cases.
