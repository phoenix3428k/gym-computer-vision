# Plank Form Checker & Hold Timer


## Overview

This project is an **AI-powered Plank Form Checker & Hold Timer** that uses real-time pose analysis to evaluate your plank exercise form, detect injury risks, and track your hold time. It leverages the YOLOv8 pose model and computer vision to provide instant feedback and visual overlays on your plank performance.

- **Real-Time Pose Analysis**
- **Body Alignment & Injury Risk Detection**
- **Hold Timer with Milestones**
- **Visual Feedback & HUD**

---

## Demo

GitHub:
https://github.com/phoenix3428k

---

## Features
- Detects plank form and provides feedback on body alignment, hip sag, neck position, and elbow angles
- Tracks hold time and resets timer on poor form
- Visual overlays for skeleton, angles, and warnings
- Generates annotated video output and screenshots

---

## How to Fork & Run

1. **Fork this repository**
   - Click the `Fork` button at the top right of [the GitHub repo](https://github.com/phoenix3428k/ai-plank-form-checker) to create your own copy.
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-plank-form-checker.git
   cd ai-plank-form-checker
   ```
3. **Add your video**
   - Place your plank video (e.g., `plank_video.mp4`) in the project folder.
4. **Run the script**
   ```bash
   python main.py plank_video.mp4
   ```
   - The script will auto-install dependencies if needed.
   - Output video and screenshots will be saved in `output_plank/` and `screenshots_plank/`.

---

## Requirements
- Python 3.8+
- [YOLOv8n-pose.pt](https://github.com/ultralytics/ultralytics) model file (included)
- See `main.py` for auto-installing dependencies

---

## Wikipedia Links
- [Plank (exercise)](https://en.wikipedia.org/wiki/Plank_(exercise))
- [Computer Vision](https://en.wikipedia.org/wiki/Computer_vision)
- [Pose Estimation](https://en.wikipedia.org/wiki/Pose_estimation)
- [YOLO (You Only Look Once)](https://en.wikipedia.org/wiki/You_Only_Look_Once)

---

## License

MIT License

Copyright (c) 2026 tubakhxn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Credits

## Dev/Creator: Debi Beura

GitHub:
https://github.com/phoenix3428k
