import os
import sys
import time

# --- Add LSS library path (inside your repo) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LSS_LIB_SRC = os.path.join(CURRENT_DIR, "..", "libs", "LSS_Library_Python", "src")
sys.path.append(LSS_LIB_SRC)

import lss
import lss_const as lssc

# ===== SERIAL PORT CONFIG (YOU ALREADY FOUND THIS) =====
CST_LSS_Port = "/dev/ttyUSB0"      # your board's port
CST_LSS_Baud = lssc.LSS_DefaultBaud
# =======================================================

# We'll try different IDs here until one joint moves
TEST_ID = 1    # change this to 0,2,3,4,5 if nothing moves

def main():
    print(f"Opening {CST_LSS_Port} @ {CST_LSS_Baud}")
    lss.initBus(CST_LSS_Port, CST_LSS_Baud)

    servo = lss.LSS(TEST_ID)

    try:
        print("Move to 0°")
        servo.move(0)
        time.sleep(2)

        print("Move to +90°")
        servo.move(900)      # 90.0°
        time.sleep(2)

        print("Move to -90°")
        servo.move(-900)     # -90.0°
        time.sleep(2)

        print("Back to 0°")
        servo.move(0)
        time.sleep(2)
    finally:
        print("Limp servo")
        servo.limp()

if __name__ == "__main__":
    main()
