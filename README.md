# Underwater Camera: Remote Measurement of Defects

A computer vision system for **measuring underwater objects and defects** (holes, breaches, protrusions) at distances of **10–100 m**, built as a team project during a professional development programme.

> This is a copy of the team repository [meeporen/underwater_camera](https://github.com/meeporen/underwater_camera), kept with its full commit history.

## Problem

Divers and ROV operators need to estimate the size of damage on underwater structures without physical contact. The system uses an RGB-D camera and lets an operator place virtual **rulers** on the live image to measure real-world distances.

## How it works

1. **Capture**: an Intel RealSense camera streams aligned RGB and depth frames.
2. **Boundary detection**: the frame is denoised (median blur) and edges are extracted with Canny; contours of the object's boundaries are found with OpenCV.
3. **Auto-snapping (auto-point)**: when the operator clicks near an edge, the point is automatically snapped to the nearest detected contour, so measurements start and end exactly on the boundary.
4. **Ruler & distance**: a line is drawn between two points; their 3D coordinates are recovered from the depth map and the real-world distance is computed.
5. **Interface**: a Streamlit app shows the camera stream with a depth overlay and lets the operator create, view and save measurements.

## Project structure

```
board_defect/
  autopoint.py               – edge detection and auto-snapping of points to contours
  main_code_board_defect.py  – frame processing for defect detection
main_code_interface.py       – Streamlit operator interface
realsense2.py                – Intel RealSense RGB-D capture
gui.py, gui2.py              – RGB + depth visualisation
utils.py                     – 3D distance calculation helpers
```

## Quick start

Requires an Intel RealSense camera.

```bash
pip install streamlit streamlit-image-coordinates opencv-python numpy pillow pyrealsense2
streamlit run main_code_interface.py
```

## Tech stack

Python · OpenCV · Intel RealSense (pyrealsense2) · NumPy · Streamlit

## Team

**My role (Mark Bulgarov, [@MP4-Player](https://github.com/MP4-Player))**: I developed the underwater boundary detection algorithm with auto-snapping of measurement points (`board_defect/autopoint.py`) and took part in the team work on drawing measurement lines and computing distances.
