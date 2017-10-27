import math

Xtime = 900
ROBOT_SPEED = 1000
CONVEYOR_SPEED = 500
F = -300

wanted_time_achieved = False
while wanted_time_achieved == False:
    weg = Xtime - F
    Robot_time = math.sqrt(math.pow(abs(234 - weg), 2) + math.pow(103, 2) + math.pow(-970,2)) / ROBOT_SPEED
    Conveyor_time = F / CONVEYOR_SPEED
    print(Robot_time)
    print(Conveyor_time)
    print("F=", F)


    if Robot_time - Conveyor_time > 0.3:
        F = F - 10
        print("hoi")
    elif Robot_time - Conveyor_time < -0.3:
        F = F + 10
        print("nhoi2")

    else:
        wanted_time_achieved = True
        Xtime = Xtime + F
        print(Xtime)

