import math

F = -50
wanted_time_achieved = False
while wanted_time_achieved == False:
    Robot_time = math.sqrt(math.pow((abs(234 - Xtime) - F), 2)) + math.pow(Real_Y, 2) + math.pow((-970),2) * ROBOT_SPEED
    Conveyor_time = F * CONVEYOR_SPEED

    if Robot_time - Conveyor_time > 0.2:
        F = F - 5
    elif Robot_time - Conveyor_time < -0.2:
        F = F + 5

    else:
        wanted_time_achieved = True
        Xtime = Xtime + F

