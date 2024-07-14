# Pluto Camera Live Stream Link Setup Guide

The purpose of this project is to demonstrate how to integrate drone video capture with web streaming, allowing for real-time monitoring and processing of video feeds from a drone.

## Requirements
The following dependencies are required to set up and run the project:

- Python packages: opencv-python, flask, numpy 
- FFmpeg installed and added to your system's PATH
- Plutocam library for video capture


### Step 1: Install required packages

Install the libraries using pip:
```bash
pip install opencv-python flask numpy
```

### Step 2: Connect to Pluto Camera
Ensure you are connected to the Pluto camera before proceeding.

### Step 3: Start the Server
Open a terminal and locate your file run the following command:

```bash
python app.py
```
This command initiates the live stream from the Pluto camera using plutocam and FFmpeg.

### Now, you are ready to enjoy live streaming from your Pluto camera! 
### The video feed from the drone can be accessed via the following URL:
```bash
http://127.0.0.1:5000/video_feed
```

## Additional Information
Stopping the Server: Press Ctrl+C in the terminal where the Flask server is running to stop the server.
Stopping Video Capture: The video capture process will terminate when the Flask server is stopped.
