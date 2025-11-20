
# Serial port config
PORT = "/dev/ttyUSB0"   #  working port
BAUD = 115200           # default LSS baud

# Servo IDs 
BASE_ID     = 1         
SHOULDER_ID = 2         
ELBOW_ID    = 3         
WRIST_ID    = 4         
GRIPPER_ID  = 5         

# Very conservative joint limits (in 0.1° = cdeg)
# Tune these as you learn safe ranges.
JOINT_LIMITS = {
    "base":     (-900, 900),   # -90° to +90°
    "shoulder": (-700, 300),   # -70° to +30°
    "elbow":    (-300, 900),   # -30° to +90°
    "wrist":    (-600, 600),   # -60° to +60°
    "gripper":  (-500, 500),   # -50° to +50°
}
