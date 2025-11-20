
"""
All joint angles are in 0.1 degrees (cdeg).
Order of joints: [base, shoulder, elbow, wrist, gripper]
"""

# Neutral home pose – arm tucked in and safe
HOME = [0, 0, 0, 0, 0]

# Above the pick location (object on table)
# Start with very small motions; we’ll tune them.
ABOVE_PICK = [
    0,      # base
    -300,   # shoulder: -30°
    600,    # elbow:    60°
    200,    # wrist:    20°
    0       # gripper open-ish
]

# At pick location (a bit lower)
PICK = [
    0,      # base
    -350,   # shoulder: -35°
    650,    # elbow
    150,    # wrist closer to down
    -200    # gripper slightly open, ready to close
]

# Above place location (somewhere else on table)
ABOVE_PLACE = [
    300,    # base rotated 30° to the right
    -250,   # shoulder
    550,    # elbow
    200,    # wrist
    -200    # gripper holding object
]

# At place location (lowered)
PLACE = [
    300,    # base
    -320,   # shoulder lower
    650,    # elbow
    150,    # wrist lower
    -200    # still holding object
]
