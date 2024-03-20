from controller import Robot, DistanceSensor, Motor

# Simulation step time
TIME_STEP = 65

MAX_SPEED = 6.28

# Robot instance
robot = Robot()

ps = []
psNames = ["ps0", "ps1"]
#  # ()
for i in range(2):
    ps.append(getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

front_left_motor = robot.getDevice("LFmotor")
front_right_motor = robot.getDevice("RFmotor")
rear_left_motor = robot.getDevice("LBmotor")
rear_right_motor = robot.getDevice("RBmotor")

front_right_motor.setPosition(float('inf'))
front_left_motor.setPosition(float('inf'))
rear_left_motor.setPosition(float('inf'))
rear_right_motor.setPosition(float('inf'))

front_right_motor.setVelocity(0.0)
front_left_motor.setVelocity(0.0)
rear_left_motor.setVelocity(0.0)
rear_right_motor.setVelocity(0.0)

# feedback loop: step simulation until receiving an exit event
while robot.step(TIME_STEP) != -1:
    # read sensors outputs
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    # detect obstacles
    right_obstacle = psValues[0] > 80.0
    left_obstacle = psValues[1] > 80.0

    # initialize motor speeds at 50% of MAX_SPEED.
    leftSpeed = 0.7 * MAX_SPEED
    rightSpeed = 0.7 * MAX_SPEED

    # modify speeds according to obstacles
    if left_obstacle:
        # turn right
        leftSpeed = 0.7 * MAX_SPEED
        rightSpeed = 0
    elif right_obstacle:
        # turn left
        leftSpeed = 0
        rightSpeed = 0.7 * MAX_SPEED

    # write actuators inputs

    front_right_motor.setVelocity(rightSpeed)
    front_left_motor.setVelocity(leftSpeed)
    rear_left_motor.setVelocity(leftSpeed)
    rear_right_motor.setVelocity(rightSpeed)
