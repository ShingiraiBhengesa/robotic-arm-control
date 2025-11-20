import os
import sys
import time

# --- Add LSS library path (inside your repo) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LSS_LIB_SRC = os.path.join(CURRENT_DIR, "..", "libs", "LSS_Library_Python", "src")
sys.path.append(LSS_LIB_SRC)

import lss
import lss_const as lssc

from config_arm import (
    PORT, BAUD,
    BASE_ID, SHOULDER_ID, ELBOW_ID, WRIST_ID, GRIPPER_ID,
    JOINT_LIMITS
)

# Map short keys to joint names
JOINT_KEYS = {
    "b": "base",
    "s": "shoulder",
    "e": "elbow",
    "w": "wrist",
    "g": "gripper",
}


def init_servos():
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


def clamp(name, value):
    mn, mx = JOINT_LIMITS[name]
    return max(mn, min(mx, value))


def main():
    servos = init_servos()

    # Track current angles
    current = {
        "base": 0,
        "shoulder": 0,
        "elbow": 0,
        "wrist": 0,
        "gripper": 0,
    }

    STEP = 50  # = 5 degrees (50 * 0.1°)
    print("\n=== Simple Teleop Mode ===")
    print("Control each joint with the keyboard")
    print("-----------------------------------")
    print("Examples:")
    print("    b +       (base +5°)")
    print("    s -       (shoulder -5°)")
    print("    open      (open gripper)")
    print("    close     (close gripper)")
    print("    home      (return all to 0°)")
    print("    q         (quit)")
    print("-----------------------------------\n")

    try:
        # Go to home
        for name in current:
            servos[name].move(0)
        time.sleep(1)

        while True:
            cmd = input("Command: ").strip().lower()

            if cmd in ("q", "quit", "exit"):
                print("Exiting teleop...")
                break

            if cmd == "home":
                print("Returning to HOME...")
                for name in current:
                    current[name] = 0
                    servos[name].move(0)
                time.sleep(0.5)
                continue

            if cmd == "open":
                print("Opening gripper...")
                name = "gripper"
                current[name] = clamp(name, current[name] + STEP)
                servos[name].move(current[name])
                time.sleep(0.2)
                continue

            if cmd == "close":
                print("Closing gripper...")
                name = "gripper"
                current[name] = clamp(name, current[name] - STEP)
                servos[name].move(current[name])
                time.sleep(0.2)
                continue

            # Expect format like "b +" or "shoulder -"
            parts = cmd.split()
            if len(parts) != 2:
                print("Invalid command. Use: b + | s - | e + | w - | g + etc.")
                continue

            joint_key, direction = parts
            joint_name = JOINT_KEYS.get(joint_key, joint_key)  # allow both 'b' and 'base'

            if joint_name not in servos:
                print("Unknown joint:", joint_key)
                continue

            if direction not in ("+", "-"):
                print("Direction must be + or -")
                continue

            delta = STEP if direction == "+" else -STEP
            new_value = clamp(joint_name, current[joint_name] + delta)
            current[joint_name] = new_value

            print(f"Moving {joint_name} to {new_value/10:.1f}°")

            servos[joint_name].move(new_value)
            time.sleep(0.2)

    finally:
        print("Limping all servos...")
        for s in servos.values():
            s.limp()


if __name__ == "__main__":
    main()
