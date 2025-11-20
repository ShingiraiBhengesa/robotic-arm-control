# src/motion_utils.py

import os
import sys
import time

# Add LSS library to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LSS_LIB_SRC = os.path.join(CURRENT_DIR, "..", "libs", "LSS_Library_Python", "src")
sys.path.append(LSS_LIB_SRC)

import lss
import lss_const as lssc
from config_arm import PORT, BAUD, BASE_ID, SHOULDER_ID, ELBOW_ID, WRIST_ID, GRIPPER_ID, JOINT_LIMITS


def init_servos():
    """Initialize the LSS bus and return a dict of named servo objects."""
    print(f"Opening {PORT} @ {BAUD}")
    lss.initBus(PORT, BAUD)

    servos = {
        "base":    lss.LSS(BASE_ID),
        "shoulder": lss.LSS(SHOULDER_ID),
        "elbow":   lss.LSS(ELBOW_ID),
        "wrist":   lss.LSS(WRIST_ID),
        "gripper": lss.LSS(GRIPPER_ID),
    }
    return servos


def clamp(name, value_cdeg):
    """Clamp angle according to JOINT_LIMITS."""
    mn, mx = JOINT_LIMITS[name]
    return max(mn, min(mx, value_cdeg))


def move_pose(servos, target_angles, duration=2.0, steps=20):
    """
    Smoothly move from current pose to target_angles over given duration.
    servos: dict with keys base/shoulder/elbow/wrist/gripper
    target_angles: list [b, s, e, w, g] in cdeg
    """
    names = ["base", "shoulder", "elbow", "wrist", "gripper"]

    # Read current position (we'll assume what we last commanded)
    # For now, we just start from 0; you can extend this to track state.
    # To make it consistent, we’ll pass in a "current" dict from outside.
    raise NotImplementedError("Use move_pose_with_current instead")


def move_pose_with_current(servos, current, target, duration=2.0, steps=20):
    """
    Interpolate from 'current' dict to 'target' dict.
    - servos: dict of LSS objects
    - current: dict like {'base': 0, ...} in cdeg
    - target:  dict like {'base': 100, ...} in cdeg
    """
    names = ["base", "shoulder", "elbow", "wrist", "gripper"]

    dt = duration / float(steps)

    for step in range(1, steps + 1):
        alpha = step / float(steps)
        for name in names:
            start = current[name]
            end = target[name]
            value = int(round(start + (end - start) * alpha))
            value = clamp(name, value)
            servos[name].move(value)
        time.sleep(dt)

    # Update current dict at the end
    for name in names:
        current[name] = int(target[name])
