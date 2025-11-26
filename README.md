# Traffic Sign Detection Project 🚦

This project implements an end-to-end traffic sign processing pipeline.
Given a dataset of road images and YOLO label files, the application will:

	1.	Load each image from the dataset.
	2.	Parse its YOLO label file (class ID and normalized bounding box).
	3.	Crop the traffic sign from the image.
	4.	Preprocess the crop (resizing, sharpening, thresholding).
	5.	If the sign is a Speed Limit sign, extract the numeric value using OCR.
	6.	If the sign is Stop, Red Light, or Green Light, interpret it directly from the class label.
	7.	Print a driving instruction such as:

	•	Speed Limit: 40, please drive really slowly
	•	Speed Limit: 100, you can drive fastly in this area
	•	Traffic sign: Red Light
	•	Traffic sign: Stop

The system is fully containerized and designed for reproducibility, making it easy to run on any machine without manual environment configuration.

# Key Features 🎉

### Accurate YOLO Label Parsing

Parses YOLO-formatted text files and extracts:

	•	Class ID
	•	Center coordinates (cx, cy)
	•	Width and height (w, h)

Broken or malformed label files are automatically skipped and reported.

### Automated Traffic Sign Cropping

Each bounding box is mapped to absolute pixel coordinates and used to crop the sign directly from the image.

### OCR-Powered Speed Limit Recognition

Speed limit signs are:

	•	Upscaled
	•	Denoised
	•	Sharpened
	•	Converted to binary form

The processed region is sent to Tesseract OCR, and the extracted digits are converted to an integer speed value.

### Docker-Based Environment

A complete runtime environment is provided via Docker.
No local dependency installation is required.

### Screenshot 📱
![Alt text](https://github.com/sudeakd32/TrafficSignDetection/blob/main/screenshot.png)
