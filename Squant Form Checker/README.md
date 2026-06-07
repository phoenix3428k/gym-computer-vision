
# Squant Form Checker & Hold Timer

This project is an **AI-powered squant (plank-squat) form checker and hold timer** using YOLOv8 pose estimation. It analyzes squant exercise form from video, provides real-time feedback, and tracks hold duration with a cinematic HUD overlay.

---

## Features
- **YOLOv8 Pose Estimation** (no MediaPipe)
- Cinematic HUD with real-time feedback
- Squant (plank-squat) form analysis (body alignment, hip level, neck, elbows)
- Hold timer with milestones and warnings
- Output video with overlays and screenshots
- Auto-installs required Python dependencies

---

## Getting Started

### 1. Clone or Fork the Repository

- **Fork** this repo on GitHub ([How to fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo))
- Or clone directly:

```bash
git clone https://github.com/phoenix3428k/squant-plank-checker.git
cd squant-plank-checker
```

### 2. Install Requirements

The script auto-installs dependencies, but you can also run:

```bash
pip install -r requirements.txt
```

### 3. Download a Video

Place your squant video (e.g., `video.mp4`) in the project folder.

### 4. Run the Script

```bash
python main.py video.mp4
```

- Output video: `output_plank_ai.mp4`
- Screenshots: `screenshots_plank/`

---

## About Squant

**Squant** is a playful term for plank-squat analysis. This project helps you check your squant form using AI.

- [Wikipedia: Plank (exercise)](https://en.wikipedia.org/wiki/Plank_(exercise))
- [Wikipedia: Squat (exercise)](https://en.wikipedia.org/wiki/Squat_(exercise))
- [YOLO (You Only Look Once)](https://en.wikipedia.org/wiki/You_Only_Look_Once)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits

## Dev/Creator: Debi Beura

GitHub:
https://github.com/phoenix3428k
---

## How to Contribute

1. Fork the repo
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

---

## MIT License

See [LICENSE](LICENSE) for details.
