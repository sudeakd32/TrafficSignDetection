import os
import cv2
import pytesseract

DATASET_PATH = "/app/data/images"
CLASS_NAMES = [
    "Green Light",
    "Red Light",
    "Speed Limit 10",
    "Speed Limit 100",
    "Speed Limit 110",
    "Speed Limit 120",
    "Speed Limit 20",
    "Speed Limit 30",
    "Speed Limit 40",
    "Speed Limit 50",
    "Speed Limit 60",
    "Speed Limit 70",
    "Speed Limit 80",
    "Speed Limit 90",
    "Stop"
]

def loadImages():
    for fname in os.listdir(DATASET_PATH):
            path = os.path.join(DATASET_PATH, fname)
            img = cv2.imread(path)
            if img is None:
                print("Could not load:", path)
                exit(1)

def loadYoloLabel(labelPath):
    with open(labelPath, "r") as f:
        line = f.readline().strip().split()

        if len(line) < 5:
            print("ERROR: Broken label file →", labelPath)
            return None

        class_id = int(line[0])
        cx, cy, w, h = map(float, line[1:])
        return class_id, cx, cy, w, h

def cropImage(img, label):
    class_id, cx, cy, w, h = label

    H, W = img.shape[:2]

    x1 = int((cx - w/2) * W)
    y1 = int((cy - h/2) * H)
    x2 = int((cx + w/2) * W)
    y2 = int((cy + h/2) * H)

    crop = img[y1:y2, x1:x2]

    return crop, class_id

def readSpeedNumber(img):

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # applying a threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    config = "--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(thresh, config=config)

    text = ''.join(filter(str.isdigit, text))

    return text

def sharpen(img):
    blur = cv2.GaussianBlur(img, (0,0), 3)
    sharp = cv2.addWeighted(img, 1.8, blur, -0.8, 0)
    return sharp

def process(imagePath, labelPath):

    img = cv2.imread(imagePath)

    # read label
    label = loadYoloLabel(labelPath)
    if label is None:
        return

    # crop sign
    crop, class_id = cropImage(img, label)

    # sharp image
    sharp = sharpen(crop)

    labelName = CLASS_NAMES[class_id]
    if "Speed Limit" in labelName:
        ocrNumber = readSpeedNumber(sharp)
        if ocrNumber is None or ocrNumber.strip() == "":
            print("OCR cant find a number → sign:", labelName)
            return
        allertDriver(ocrNumber)
    else:
        print("Traffic sign:", labelName)

def allertDriver(ocrNumber):
    speedLimit = int(ocrNumber)
    if speedLimit <= 50:
        print("Speed Limit:", ocrNumber, ", please drive really slowly")
    elif speedLimit >= 100:
        print("Speed Limit:", ocrNumber, ", you can drive fastly in this area")
    else:
        print("Speed Limit:", ocrNumber, ", please drive in normal speed in this area")

def processDataset():
    IMG_DIR = "/app/data/images"
    LABEL_DIR = "/app/data/labels"

    print("Dataset scanning:", IMG_DIR)

    for fname in sorted(os.listdir(IMG_DIR)):

        imgPath = os.path.join(IMG_DIR, fname)

        labelName = os.path.splitext(fname)[0] + ".txt"
        labelPath = os.path.join(LABEL_DIR, labelName)

        if not os.path.exists(labelPath):
            continue

        process(imgPath, labelPath)

if __name__ == "__main__":
    loadImages()
    processDataset()





