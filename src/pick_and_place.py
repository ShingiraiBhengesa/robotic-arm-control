import time
from motion_utils import init_servos, move_pose_with_current
from poses import HOME, ABOVE_PICK, PICK, ABOVE_PLACE, PLACE

def list_to_pose_dict(angles):
    """Convert [b,s,e,w,g] list into a dict keyed by joint name."""
    names = ["base", "shoulder", "elbow", "wrist", "gripper"]
    return {n: a for n, a in zip(names, angles)}


def run_pick_and_place():
    servos = init_servos()

    # Track current joint angles (what we've commanded so far)
    current = {
        "base": 0,
        "shoulder": 0,
        "elbow": 0,
        "wrist": 0,
        "gripper": 0,
    }

    try:
        print("\n=== Pick and Place Demo (no camera) ===")

        # 1) Go to HOME
        print("1) Moving to HOME...")
        home_target = list_to_pose_dict(HOME)
        move_pose_with_current(servos, current, home_target, duration=2.0, steps=20)
        time.sleep(1.0)

        # 2) ABOVE_PICK
        print("2) Moving ABOVE_PICK...")
        above_pick_target = list_to_pose_dict(ABOVE_PICK)
        move_pose_with_current(servos, current, above_pick_target, duration=2.0, steps=20)
        time.sleep(1.0)

        # 3) Move down to PICK
        print("3) Moving to PICK...")
        pick_target = list_to_pose_dict(PICK)
        move_pose_with_current(servos, current, pick_target, duration=2.0, steps=20)
        time.sleep(0.5)

        # 4) Close gripper (simulate grasp)
        print("4) Closing gripper to grasp object...")
        # Decrease gripper angle a bit
        pick_target["gripper"] -= 150  # tune this value
        move_pose_with_current(servos, current, pick_target, duration=1.0, steps=10)
        time.sleep(0.5)

        # 5) Lift back to ABOVE_PICK with object
        print("5) Lifting back to ABOVE_PICK with object...")
        move_pose_with_current(servos, current, above_pick_target, duration=2.0, steps=20)
        time.sleep(1.0)

        # 6) Move ABOVE_PLACE
        print("6) Moving ABOVE_PLACE...")
        above_place_target = list_to_pose_dict(ABOVE_PLACE)
        move_pose_with_current(servos, current, above_place_target, duration=2.0, steps=20)
        time.sleep(1.0)

        # 7) Move down to PLACE
        print("7) Moving to PLACE...")
        place_target = list_to_pose_dict(PLACE)
        move_pose_with_current(servos, current, place_target, duration=2.0, steps=20)
        time.sleep(0.5)

        # 8) Open gripper to release
        print("8) Opening gripper to release object...")
        place_target["gripper"] += 300  # tune open amount
        move_pose_with_current(servos, current, place_target, duration=1.0, steps=10)
        time.sleep(0.5)

        # 9) Back to ABOVE_PLACE
        print("9) Back to ABOVE_PLACE...")
        move_pose_with_current(servos, current, above_place_target, duration=2.0, steps=20)
        time.sleep(1.0)

        # 10) Back to HOME
        print("10) Back to HOME...")
        move_pose_with_current(servos, current, home_target, duration=2.0, steps=20)
        time.sleep(1.0)

        print("\n=== Done ===")

    finally:
        print("Limping all servos...")
        for s in servos.values():
            s.limp()


if __name__ == "__main__":
    run_pick_and_place()
