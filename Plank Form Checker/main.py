"""
╔══════════════════════════════════════════════════════════════╗
║       AI PLANK FORM CHECKER & HOLD TIMER                    ║
║       Real-Time Pose Analysis · Injury Risk Detection       ║
║       Dev/Creator: tubakhxn                                  ║
║       GitHub: https://github.com/tubakhxn                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import subprocess
import importlib
import time
import math
import random
from pathlib import Path

# ─── AUTO INSTALLER ─────────────────────────────────────────────────────────

REQUIRED = [
    ("ultralytics", "ultralytics"),
    ("cv2",         "opencv-python"),
    ("numpy",       "numpy"),
    ("torch",       "torch"),
    ("torchvision", "torchvision"),
    ("scipy",       "scipy"),
    ("PIL",         "pillow"),
    ("mediapipe",   "mediapipe"),
    ("tqdm",        "tqdm"),
]

def print_banner():
    print("\033[96m")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       AI PLANK FORM CHECKER & HOLD TIMER                    ║")
    print("║       Body Alignment · Hold Timer · Injury Risk · HUD       ║")
    print("║       Dev/Creator: tubakhxn                                  ║")
    print("║       GitHub: https://github.com/tubakhxn                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\033[0m")

def install_step(step, total, name):
    bar_len = 30
    fill    = int(bar_len * step / total)
    bar     = "█" * fill + "░" * (bar_len - fill)
    pct     = int(100 * step / total)
    print(f"\r\033[93m[{step}/{total}] {name:<35} [{bar}] {pct}%\033[0m",
          end="", flush=True)

def auto_install():
    print_banner()
    steps = [
        "Checking Dependencies...",
        "Installing Packages...",
        "Loading Pose Model...",
        "Initializing AI Engine...",
        "Processing Video...",
        "Compressing Output...",
    ]
    print(f"\033[92m[1/6] {steps[0]}\033[0m")
    missing = []
    for mod, pkg in REQUIRED:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"\033[92m[2/6] {steps[1]}\033[0m")
        for i, pkg in enumerate(missing):
            install_step(i + 1, len(missing), f"Installing {pkg}")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        print()
    else:
        print(f"\033[92m[2/6] All packages present.\033[0m")

    print(f"\033[92m[3/6] {steps[2]}\033[0m")
    print(f"\033[92m[4/6] {steps[3]}\033[0m")

auto_install()

# ─── IMPORTS ─────────────────────────────────────────────────────────────────
import numpy as np
import cv2
import torch
from ultralytics import YOLO
from collections import defaultdict, deque
import warnings
warnings.filterwarnings("ignore")

# ─── GPU ─────────────────────────────────────────────────────────────────────
DEVICE  = "cuda" if torch.cuda.is_available() else "cpu"
USE_FP16 = DEVICE == "cuda"
print(f"\033[94m[GPU] Device: {DEVICE.upper()}  FP16: {USE_FP16}\033[0m")

# ─── MODEL ───────────────────────────────────────────────────────────────────
print("\033[93m[MODEL] Loading YOLOv8 pose model...\033[0m")
model = YOLO("yolov8n-pose.pt")
print("\033[92m[MODEL] Ready.\033[0m")

# ─── KEYPOINT INDICES ────────────────────────────────────────────────────────
# YOLOv8 pose keypoints (COCO format)
NOSE=0; L_EYE=1; R_EYE=2; L_EAR=3; R_EAR=4
L_SHOULDER=5; R_SHOULDER=6
L_ELBOW=7;    R_ELBOW=8
L_WRIST=9;    R_WRIST=10
L_HIP=11;     R_HIP=12
L_KNEE=13;    R_KNEE=14
L_ANKLE=15;   R_ANKLE=16

SKELETON_PAIRS = [
    (L_SHOULDER, R_SHOULDER),
    (L_SHOULDER, L_ELBOW),   (L_ELBOW, L_WRIST),
    (R_SHOULDER, R_ELBOW),   (R_ELBOW, R_WRIST),
    (L_SHOULDER, L_HIP),     (R_SHOULDER, R_HIP),
    (L_HIP, R_HIP),
    (L_HIP, L_KNEE),         (L_KNEE, L_ANKLE),
    (R_HIP, R_KNEE),         (R_KNEE, R_ANKLE),
    (NOSE, L_SHOULDER),      (NOSE, R_SHOULDER),
]

# ─── COLORS ──────────────────────────────────────────────────────────────────
GLOW = {
    "skeleton_good":  (0,  255, 180),
    "skeleton_warn":  (0,  200, 255),
    "skeleton_bad":   (60,  60, 255),
    "joint_good":     (0,  255, 120),
    "joint_warn":     (0,  180, 255),
    "joint_bad":      (60,  60, 255),
    "angle_good":     (0,  255, 100),
    "angle_warn":     (0,  180, 255),
    "angle_bad":      (60,  60, 255),
    "hud_accent":     (0,  200, 255),
    "rep_counter":    (0,  255, 120),
    "warning_text":   (60,  60, 255),
    "bar_fill_good":  (0,  220, 100),
    "bar_fill_bad":   (60,  60, 255),
    "trajectory":     (255, 140,  0),
}

# ─── EXERCISE CONFIGS ─────────────────────────────────────────────────────────
EXERCISES = {
    "PLANK": {
        "joints": [
            {"name": "Body Line",  "a": L_SHOULDER, "b": L_HIP,   "c": L_ANKLE,
             "good": (160, 180), "warn": (145, 180)},
            {"name": "Hip Sag",    "a": L_SHOULDER, "b": L_HIP,   "c": L_KNEE,
             "good": (160, 180), "warn": (148, 180)},
            {"name": "Neck Align", "a": NOSE,       "b": L_SHOULDER, "c": L_HIP,
             "good": (155, 180), "warn": (140, 180)},
            {"name": "Elbow",      "a": L_SHOULDER, "b": L_ELBOW, "c": L_WRIST,
             "good": (85, 100),  "warn": (75, 115)},
        ],
        "rep_joint":   L_HIP,
        "rep_angle":   (L_SHOULDER, L_HIP, L_ANKLE),
        "rep_down":    999,   # plank has no reps — timer mode instead
        "rep_up":      999,
        "description": "Straight body · No hip sag · Elbows under shoulders · Neutral neck",
    },
}

# Plank hold timer per person (pid → start timestamp)
PLANK_TIMERS = {}

# ─── ANGLE HELPER ─────────────────────────────────────────────────────────────
def calc_angle(a, b, c):
    """Angle at joint B formed by A-B-C."""
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return math.degrees(math.acos(np.clip(cosine, -1.0, 1.0)))

def get_kp(kps, idx):
    """Return (x, y, conf) for keypoint idx, or None."""
    if idx >= len(kps):
        return None
    kp = kps[idx]
    if kp[2] < 0.3:
        return None
    return (float(kp[0]), float(kp[1]), float(kp[2]))

# ─── EXERCISE DETECTOR ────────────────────────────────────────────────────────
def auto_detect_exercise(kps):
    return "PLANK"

# ─── PER-PERSON TRACKER ───────────────────────────────────────────────────────
class PersonTracker:
    def __init__(self):
        self.rep_count    = defaultdict(int)
        self.rep_state    = defaultdict(lambda: "UP")   # UP or DOWN
        self.form_scores  = defaultdict(lambda: deque(maxlen=30))
        self.angle_hist   = defaultdict(lambda: deque(maxlen=60))
        self.exercise_hist= defaultdict(lambda: deque(maxlen=20))
        self.id_map       = {}   # bbox_cx -> track_id
        self.next_id      = 0

    def match_id(self, cx, cy):
        best_id, best_d = None, 100
        for prev_id, (px, py) in self.id_map.items():
            d = math.hypot(cx - px, cy - py)
            if d < best_d:
                best_d, best_id = d, prev_id
        if best_id is None:
            best_id = self.next_id
            self.next_id += 1
        self.id_map[best_id] = (cx, cy)
        return best_id

    def count_rep(self, pid, angle, exercise):
        cfg = EXERCISES[exercise]
        down_thresh = cfg["rep_down"]
        up_thresh   = cfg["rep_up"]
        # handle both up→down and down→up exercises
        if down_thresh < up_thresh:   # squat / deadlift: down = small angle
            if angle < down_thresh and self.rep_state[pid] == "UP":
                self.rep_state[pid] = "DOWN"
            elif angle > up_thresh and self.rep_state[pid] == "DOWN":
                self.rep_state[pid] = "UP"
                self.rep_count[pid] += 1
        else:                         # curl / press: down = large angle
            if angle > down_thresh and self.rep_state[pid] == "UP":
                self.rep_state[pid] = "DOWN"
            elif angle < up_thresh and self.rep_state[pid] == "DOWN":
                self.rep_state[pid] = "UP"
                self.rep_count[pid] += 1

    def get_form_score(self, pid):
        hist = list(self.form_scores[pid])
        return int(np.mean(hist)) if hist else 100

# ─── DRAWING HELPERS ──────────────────────────────────────────────────────────
def glow_line(img, p1, p2, color, thickness=2, layers=3):
    for i in range(layers, 0, -1):
        gc = tuple(min(255, int(c * 0.25 * i)) for c in color)
        cv2.line(img, p1, p2, gc, thickness + i * 2)
    cv2.line(img, p1, p2, color, thickness)

def glow_circle(img, center, radius, color, thickness=-1, layers=2):
    for i in range(layers, 0, -1):
        gc = tuple(min(255, int(c * 0.3)) for c in color)
        cv2.circle(img, center, radius + i * 2, gc, 2)
    cv2.circle(img, center, radius, color, thickness)

def hud_text(img, text, pos, color=(0, 200, 255), scale=0.55, thick=1):
    x, y = pos
    cv2.putText(img, text, (x+1, y+1), cv2.FONT_HERSHEY_SIMPLEX, scale, (0,0,0), thick+1)
    cv2.putText(img, text, pos,         cv2.FONT_HERSHEY_SIMPLEX, scale, color,   thick)

def draw_angle_arc(img, b_pt, angle, color, radius=28):
    """Draw a small arc at joint showing the measured angle."""
    cv2.ellipse(img, b_pt, (radius, radius), 0, 0, int(angle),
                tuple(c//3 for c in color), 2)
    cv2.ellipse(img, b_pt, (radius, radius), 0, 0, int(angle), color, 1)
    hud_text(img, f"{int(angle)}", (b_pt[0]+radius+3, b_pt[1]+5),
             color, 0.35, 1)

def draw_skeleton(frame, kps, sk_color, joint_color):
    h, w = frame.shape[:2]
    valid = {}
    for idx in range(len(kps)):
        kp = kps[idx]
        if len(kp) >= 3 and kp[2] > 0.3:
            x, y = int(kp[0]), int(kp[1])
            if 0 <= x < w and 0 <= y < h:
                valid[idx] = (x, y)
    for a, b in SKELETON_PAIRS:
        if a in valid and b in valid:
            glow_line(frame, valid[a], valid[b], sk_color, 2, 2)
    for idx, pt in valid.items():
        glow_circle(frame, pt, 4, joint_color, -1, 2)
    return valid

def draw_form_bar(img, score, pos, width=120, label="FORM SCORE"):
    x, y = pos
    h_bar = 14
    cv2.rectangle(img, (x, y), (x+width, y+h_bar), (30,30,50), -1)
    fill  = int(width * score / 100)
    col   = GLOW["bar_fill_good"] if score >= 70 else GLOW["bar_fill_bad"]
    cv2.rectangle(img, (x, y), (x+fill, y+h_bar), col, -1)
    cv2.rectangle(img, (x, y), (x+width, y+h_bar), (80,80,100), 1)
    hud_text(img, f"{label}: {score}%", (x, y-5), col, 0.38, 1)

def draw_plank_timer(img, pid, form_score, pos):
    x, y = pos
    global PLANK_TIMERS
    if pid not in PLANK_TIMERS:
        PLANK_TIMERS[pid] = time.time()
    if form_score < 40:   # bad form resets timer
        PLANK_TIMERS[pid] = time.time()
    elapsed = int(time.time() - PLANK_TIMERS[pid])
    mins = elapsed // 60
    secs = elapsed % 60
    time_str = f"{mins:02d}:{secs:02d}"
    bg = np.zeros((70, 120, 3), dtype=np.uint8)
    cv2.rectangle(bg, (0,0),(119,69),(10,10,30),-1)
    cv2.rectangle(bg, (0,0),(119,69),GLOW["hud_accent"],1)
    roi = img[y:y+70, x:x+120]
    if roi.shape[:2] == (70,120):
        cv2.addWeighted(roi, 0.3, bg, 0.9, 0, roi)
    hud_text(img, "HOLD TIME", (x+18, y+18), GLOW["hud_accent"], 0.42, 1)
    col = GLOW["rep_counter"] if elapsed < 60 else (0,220,255) if elapsed < 120 else (255,180,0)
    hud_text(img, time_str, (x+20, y+54), col, 1.1, 3)
    return elapsed

def draw_angle_panel(img, angle_results, pos, panel_w=200):
    x, y = pos
    row_h = 22
    ph    = 20 + len(angle_results) * row_h
    panel = np.zeros((ph, panel_w, 3), dtype=np.uint8)
    cv2.rectangle(panel, (0,0), (panel_w-1, ph-1), (15,15,35), -1)
    cv2.rectangle(panel, (0,0), (panel_w-1, ph-1), GLOW["hud_accent"], 1)

    for i, (name, angle, status) in enumerate(angle_results):
        col = GLOW["angle_good"] if status == "GOOD" else (
              GLOW["angle_warn"] if status == "WARN" else GLOW["angle_bad"])
        ry = 16 + i * row_h
        bar_fill = int((panel_w - 90) * min(angle, 180) / 180)
        cv2.rectangle(panel, (85, ry-10), (85+bar_fill, ry+2), tuple(c//3 for c in col), -1)
        cv2.putText(panel, f"{name:<14}", (4, ry), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (180,180,200), 1)
        cv2.putText(panel, f"{int(angle):3d}", (80, ry), cv2.FONT_HERSHEY_SIMPLEX, 0.38, col, 1)

    roi = img[y:y+ph, x:x+panel_w]
    if roi.shape == panel.shape:
        cv2.addWeighted(roi, 0.2, panel, 0.9, 0, roi)

def draw_warning_overlay(img, warnings_list):
    if not warnings_list:
        return
    h, w = img.shape[:2]
    for i, warn in enumerate(warnings_list[:4]):
        y = h - 80 + i * 20
        hud_text(img, f"⚠  {warn}", (14, y), GLOW["warning_text"], 0.48, 1)

def draw_exercise_badge(img, exercise, pos):
    x, y = pos
    badge_w = len(exercise) * 9 + 16
    overlay = img.copy()
    cv2.rectangle(overlay, (x, y-18), (x+badge_w, y+4), (0,0,0), -1)
    cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)
    cv2.rectangle(img, (x, y-18), (x+badge_w, y+4), GLOW["hud_accent"], 1)
    hud_text(img, exercise, (x+6, y), GLOW["hud_accent"], 0.45, 1)

# ─── MAIN COMPOSE FUNCTION ────────────────────────────────────────────────────
def compose_frame(frame, results, tracker, frame_idx, total_frames, fps, ex_override=None):
    h, w   = frame.shape[:2]
    output = frame.copy()

    # scanline overlay
    overlay = np.zeros_like(output)
    for row in range(0, h, 4):
        overlay[row] = [0, 0, 0]
    cv2.addWeighted(output, 0.93, overlay, 0.07, 0, output)

    result   = results[0]
    n_people = 0
    total_form = []

    if result.boxes is not None and result.keypoints is not None:
        boxes = result.boxes.xyxy.cpu().numpy()
        kps_all = result.keypoints.data.cpu().numpy()
        n_people = len(boxes)

        for i, (box, kps) in enumerate(zip(boxes, kps_all)):
            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            pid = tracker.match_id(cx, cy)

            # ── detect exercise ──
            exercise = ex_override if ex_override else auto_detect_exercise(kps)
            tracker.exercise_hist[pid].append(exercise)
            # smooth by majority
            hist = list(tracker.exercise_hist[pid])
            exercise = max(set(hist), key=hist.count)

            cfg = EXERCISES[exercise]

            # ── measure joint angles ──
            angle_results = []   # (name, angle, status)
            frame_warnings = []
            joint_scores = []

            for jcfg in cfg["joints"]:
                pa = get_kp(kps, jcfg["a"])
                pb = get_kp(kps, jcfg["b"])
                pc = get_kp(kps, jcfg["c"])
                if pa and pb and pc:
                    angle = calc_angle(
                        (pa[0],pa[1]), (pb[0],pb[1]), (pc[0],pc[1])
                    )
                    lo_g, hi_g = jcfg["good"]
                    lo_w, hi_w = jcfg["warn"]
                    if lo_g <= angle <= hi_g:
                        status = "GOOD"
                        joint_scores.append(100)
                    elif lo_w <= angle <= hi_w:
                        status = "WARN"
                        joint_scores.append(60)
                        frame_warnings.append(f"{jcfg['name']}: {int(angle)}° — adjust form")
                    else:
                        status = "BAD"
                        joint_scores.append(20)
                        frame_warnings.append(f"{jcfg['name']}: {int(angle)}° — INJURY RISK")
                    angle_results.append((jcfg["name"], angle, status))

                    # draw arc at joint B
                    bpt = get_kp(kps, jcfg["b"])
                    if bpt:
                        arc_col = (GLOW["angle_good"] if status=="GOOD" else
                                   GLOW["angle_warn"] if status=="WARN" else
                                   GLOW["angle_bad"])
                        draw_angle_arc(output, (int(bpt[0]),int(bpt[1])), angle, arc_col)

            # ── rep counting ──
            ra, rb, rc = cfg["rep_angle"]
            pa2 = get_kp(kps, ra)
            pb2 = get_kp(kps, rb)
            pc2 = get_kp(kps, rc)
            if pa2 and pb2 and pc2:
                rep_angle = calc_angle(
                    (pa2[0],pa2[1]), (pb2[0],pb2[1]), (pc2[0],pc2[1])
                )
                tracker.count_rep(pid, rep_angle, exercise)
                tracker.angle_hist[pid].append(rep_angle)

            # ── form score ──
            frame_score = int(np.mean(joint_scores)) if joint_scores else 80
            tracker.form_scores[pid].append(frame_score)
            smooth_score = tracker.get_form_score(pid)
            total_form.append(smooth_score)

            # ── skeleton color based on score ──
            if smooth_score >= 75:
                sk_col, jt_col = GLOW["skeleton_good"], GLOW["joint_good"]
            elif smooth_score >= 45:
                sk_col, jt_col = GLOW["skeleton_warn"], GLOW["joint_warn"]
            else:
                sk_col, jt_col = GLOW["skeleton_bad"],  GLOW["joint_bad"]

            valid_pts = draw_skeleton(output, kps, sk_col, jt_col)

            # ── bounding box ──
            glow_line(output,(x1,y1),(x2,y1), sk_col, 2, 2)
            glow_line(output,(x1,y2),(x2,y2), sk_col, 2, 2)
            glow_line(output,(x1,y1),(x1,y2), sk_col, 2, 2)
            glow_line(output,(x2,y1),(x2,y2), sk_col, 2, 2)

            # ── exercise badge ──
            draw_exercise_badge(output, exercise, (x1, y1 - 22))

            # ── angle panel (right side of box) ──
            panel_x = min(x2 + 8, w - 210)
            if angle_results:
                draw_angle_panel(output, angle_results, (panel_x, y1), 205)

            # ── plank hold timer ──
            rc_x = max(x1, 4)
            rc_y = min(y2 + 8, h - 80)
            hold_secs = draw_plank_timer(output, pid, smooth_score, (rc_x, rc_y))

            # ── form bar ──
            draw_form_bar(output, smooth_score, (rc_x + 128, rc_y + 28), 120)

            # ── milestone badges ──
            milestones = {30:"30s!", 60:"1 MIN!", 90:"90s!", 120:"2 MINS!", 180:"3 MINS! BEAST!"}
            for ms_secs, ms_label in milestones.items():
                if hold_secs == ms_secs:
                    hud_text(output, ms_label, (int(cx)-40, int(y1)-60),
                             (0,255,255), 1.0, 3)

            # ── plank body alignment line ──
            ls_pt = get_kp(kps, L_SHOULDER)
            lh_pt = get_kp(kps, L_HIP)
            la_pt = get_kp(kps, L_ANKLE)
            if ls_pt and lh_pt and la_pt:
                body_angle = calc_angle(
                    (ls_pt[0],ls_pt[1]),(lh_pt[0],lh_pt[1]),(la_pt[0],la_pt[1])
                )
                line_col = GLOW["skeleton_good"] if body_angle>=160 else (
                           GLOW["skeleton_warn"] if body_angle>=145 else GLOW["skeleton_bad"])
                glow_line(output,
                          (int(ls_pt[0]),int(ls_pt[1])),
                          (int(la_pt[0]),int(la_pt[1])),
                          line_col, 2, 3)
                mid_x = int((ls_pt[0]+la_pt[0])/2)
                mid_y = int((ls_pt[1]+la_pt[1])/2)
                label = "ALIGNED" if body_angle>=160 else ("SLIGHT SAG" if body_angle>=145 else "HIP SAG!")
                hud_text(output, label, (mid_x+8, mid_y), line_col, 0.45, 1)

            # ── tip text ──
            hud_text(output, cfg["description"], (x1, y2 + 85),
                     (180, 220, 255), 0.35, 1)

            # ── ID ──
            hud_text(output, f"ID:{pid}", (x1, y1 - 42),
                     GLOW["hud_accent"], 0.4, 1)

            # ── warnings ──
            draw_warning_overlay(output, frame_warnings)

            # ── angle history mini-graph ──
            ang_hist = list(tracker.angle_hist[pid])
            if len(ang_hist) > 2:
                gw, gh = 120, 40
                gx, gy = w - gw - 12, y1
                graph_bg = np.zeros((gh, gw, 3), dtype=np.uint8)
                cv2.rectangle(graph_bg, (0,0),(gw-1,gh-1),(15,15,35),-1)
                cv2.rectangle(graph_bg, (0,0),(gw-1,gh-1),(60,60,80),1)
                pts = ang_hist[-gw:]
                for pi in range(1, len(pts)):
                    ax = int((pi-1) / len(pts) * gw)
                    bx = int(pi     / len(pts) * gw)
                    ay = gh - int(pts[pi-1] / 180 * gh)
                    by = gh - int(pts[pi]   / 180 * gh)
                    cv2.line(graph_bg,(ax,ay),(bx,by),GLOW["hud_accent"],1)
                roi = output[gy:gy+gh, gx:gx+gw]
                if roi.shape == graph_bg.shape:
                    cv2.addWeighted(roi, 0.3, graph_bg, 0.85, 0, roi)
                hud_text(output, "ANGLE GRAPH", (gx, gy-5),
                         (120,120,180), 0.3, 1)

    # ── HUD HEADER ────────────────────────────────────────────────────────────
    progress = frame_idx / max(total_frames, 1)
    cv2.rectangle(output, (0, 0), (w, 42), (0, 0, 0), -1)
    cv2.addWeighted(output[0:42], 0.5,
                    np.zeros((42, w, 3), dtype=np.uint8), 0.5, 0, output[0:42])
    hud_text(output, "▸ AI PLANK FORM CHECKER & HOLD TIMER", (10, 28),
             GLOW["hud_accent"], 0.6, 2)
    hud_text(output, f"FPS:{fps:.0f}  FRAME:{frame_idx}/{total_frames}  DEVICE:{DEVICE.upper()}",
             (w - 340, 28), (180, 255, 180), 0.45)

    # progress bar
    cv2.rectangle(output, (0, h-6), (w, h),             (20,20,40), -1)
    cv2.rectangle(output, (0, h-6), (int(w*progress),h), GLOW["hud_accent"], -1)

    # stats row
    avg_form = int(np.mean(total_form)) if total_form else 0
    hud_text(output, f"PEOPLE IN FRAME: {n_people}", (10, 60),
             (200,255,200), 0.5)
    hud_text(output, f"AVG BODY ALIGNMENT: {avg_form}%", (10, 80),
             GLOW["rep_counter"] if avg_form>=70 else GLOW["warning_text"], 0.5)

    # watermark
    hud_text(output, "tubakhxn | github.com/tubakhxn",
             (w - 268, h - 18), (80, 80, 120), 0.35)

    return output


# ─── VIDEO PROCESSOR ─────────────────────────────────────────────────────────
def process_video(video_path, exercise_override=None):
    print(f"\033[92m[5/6] Processing Video: {video_path}\033[0m")

    out_dir   = Path("output_plank")
    shots_dir = Path("screenshots_plank")
    out_dir.mkdir(exist_ok=True)
    shots_dir.mkdir(exist_ok=True)
    output_path = "output_plank_ai.mp4"
    tmp_path    = str(out_dir / "tmp_plank.mp4")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"\033[91m[ERROR] Cannot open: {video_path}\033[0m")
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    orig_fps     = cap.get(cv2.CAP_PROP_FPS) or 30.0
    fw           = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fh           = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer  = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*"mp4v"),
                              orig_fps, (fw, fh))
    tracker = PersonTracker()

    frame_idx     = 0
    t_start       = time.time()
    shot_interval = max(1, total_frames // 10)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        elapsed = time.time() - t_start
        fps     = frame_idx / elapsed if elapsed > 0 else orig_fps
        eta     = (total_frames - frame_idx) / fps if fps > 0 else 0

        results  = model(frame, verbose=False, device=DEVICE,
                         half=USE_FP16, classes=[0])
        composed = compose_frame(frame, results, tracker,
                                 frame_idx, total_frames, fps,
                                 exercise_override)
        writer.write(composed)

        if frame_idx % shot_interval == 0:
            cv2.imwrite(str(shots_dir / f"shot_{frame_idx:05d}.jpg"), composed)

        pct = int(100 * frame_idx / total_frames)
        bar = "█" * (pct // 3) + "░" * (34 - pct // 3)
        print(f"\r\033[93m  [{bar}] {pct}%  ETA:{eta:.1f}s  FPS:{fps:.1f}\033[0m",
              end="", flush=True)

    print()
    cap.release()
    writer.release()

    # ── ffmpeg compression ────────────────────────────────────────────────────
    print(f"\033[92m[6/6] Compressing output...\033[0m")
    try:
        ret = subprocess.run(
            ["ffmpeg", "-y", "-i", tmp_path, "-vcodec", "libx264",
             "-crf", "23", "-preset", "fast", output_path],
            capture_output=True
        )
        if ret.returncode != 0:
            import shutil; shutil.copy(tmp_path, output_path)
    except FileNotFoundError:
        import shutil; shutil.copy(tmp_path, output_path)

    print(f"\033[92m[✓] Output saved  → {output_path}\033[0m")
    print(f"\033[92m[✓] Screenshots   → {shots_dir}/\033[0m")
    size_mb = os.path.getsize(output_path) / 1e6
    print(f"\033[94m[i] File size: {size_mb:.2f} MB\033[0m")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print_banner()
    if len(sys.argv) < 2:
        print("\033[96mUsage examples:\033[0m")
        print("  python gym_form.py plank_video.mp4")
        print("  python gym_form.py curl_video.mp4 'BICEP CURL'")
        print("  python gym_form.py press_video.mp4 'SHOULDER PRESS'")
        print("  python gym_form.py deadlift_video.mp4 DEADLIFT")
        print("\033[93m  Exercise: PLANK — measures body line, hip sag, neck, elbow angles\033[0m")
        sys.exit(1)

    video   = sys.argv[1]
    ex_arg  = " ".join(sys.argv[2:]).upper() if len(sys.argv) > 2 else None
    if ex_arg and ex_arg not in EXERCISES:
        print(f"\033[91m[WARN] Unknown exercise '{ex_arg}', using auto-detect.\033[0m")
        ex_arg = None

    process_video(video, ex_arg)