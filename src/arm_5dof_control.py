import os
import sys
import time

# --- Add LSS library path (inside your repo) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LSS_LIB_SRC = os.path.join(CURRENT_DIR, "..", "libs", "LSS_Library_Python", "src")
sys.path.append(LSS_LIB_SRC)

import lss
import lss_const as lssc

# ===== SERIAL PORT CONFIG =====
CST_LSS_Port = "/dev/ttyUSB0"     
CST_LSS_Baud = lssc.LSS_DefaultBaud
# ==============================

# ===== SERVO ID MAPPING =====
BASE_ID     = 1   # the ID that made the base move
SHOULDER_ID = 2   # shoulder
ELBOW_ID    = 3   # elbow
WRIST_ID    = 4   # wrist
GRIPPER_ID  = 5   # gripper
# ============================

def init_servos():
    lss.initBus(CST_LSS_Port, CST_LSS_Baud)

    base     = lss.LSS(BASE_ID)
    shoulder = lss.LSS(SHOULDER_ID)
    elbow    = lss.LSS(ELBOW_ID)
    wrist    = lss.LSS(WRIST_ID)
    gripper  = lss.LSS(GRIPPER_ID)

    return [base, shoulder, elbow, wrist, gripper]

def move_pose(servos, angles):
    """angles in 0.1° units (e.g. 900 = 90.0°)"""
    for s, a in zip(servos, angles):
        s.move(a)

def main():
    servos = init_servos()
    base, shoulder, elbow, wrist, gripper = servos

    try:
        print("Home pose...")
        move_pose(servos, [0, 0, 0, 0, 0])
        time.sleep(3)

        print("Reach forward pose (TUNE THESE ANGLES!)")
        move_pose(servos, [
            0,      # base
            -400,   # shoulder: -40.0°
            600,    # elbow:    60.0°
            300,    # wrist:    30.0°
            0       # gripper
        ])
        time.sleep(4)

        print("Gripper open/close...")
        for _ in range(3):
            gripper.move(300)   # open
            time.sleep(1)
            gripper.move(-300)  # close
            time.sleep(1)

        print("Back to home...")
        move_pose(servos, [0, 0, 0, 0, 0])
        time.sleep(3)

    finally:
        print("Limp all servos")
        for s in servos:
            s.limp()

if __name__ == "__main__":
    main()
