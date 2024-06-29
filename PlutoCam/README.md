# Pluto Camera Live Stream Setup Guide

## Prerequisites

Before setting up the Pluto camera live stream, ensure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/downloads/) (if not installed already)
- [FFmpeg](https://ffmpeg.org/download.html) (for your operating system)

## Installation Steps

### Step 1: Download FFmpeg

Download FFmpeg from one of the following sources:
- [Official FFmpeg Website](https://ffmpeg.org/download.html)
- [FFmpeg Builds on GitHub](https://github.com/BtbN/FFmpeg-Builds/releases)

### Step 2: Install FFmpeg

Follow the installation instructions based on your operating system:
- **Windows:** [FFmpeg Installation Guide for Windows](https://phoenixnap.com/kb/ffmpeg-windows)
- **Linux:** [Install FFmpeg on Ubuntu](https://phoenixnap.com/kb/install-ffmpeg-ubuntu)
- **Mac:** [FFmpeg Installation Guide for Mac](https://phoenixnap.com/kb/ffmpeg-mac)

### Step 3: Install Python

If Python is not installed on your system, download and install it from the [official Python website](https://www.python.org/downloads/).

### Step 4: Install plutocam

Install the `plutocam` library using pip:
```bash
pip install plutocam
```

## Streaming Setup
### Step 5: Connect to Pluto Camera
Ensure you are connected to the Pluto camera before proceeding.

### Step 6: Start the Stream
Open a terminal and run the following command:

```bash
plutocam stream start --out-file - | ffplay -i -fflags nobuffer -flags low_delay -probesize 32 -sync ext -
```
This command initiates the live stream from the Pluto camera using plutocam and FFmpeg.

### Additional Resources
For more information and advanced usage, refer to the [Pylwdrone GitHub repository](https://github.com/meekworth/pylwdrone).

## Now, you are ready to enjoy live streaming from your Pluto camera!
