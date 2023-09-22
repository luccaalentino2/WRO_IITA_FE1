from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

# Hub Things
hub = PrimeHub()
color1 =ColorSensor("D")
motor = Motor("B")
giro = Motor("C")
dist_izquierda = DistanceSensor("A")
dist_derecha = DistanceSensor("E")

# Variables
valor_violeta = True
valor_naranja = False
numero = 0

# Functions
def Stability():
    giro.run_to_position(0)
    wait_for_seconds(1)
    # Using the gyroscope which will reset itself every time I pass each section. So that the gyro is proper and safe.
    hub.motion_sensor.reset_yaw_angle()
    wait_for_seconds(1)

    while True:
        hub.light_matrix.show_image("ANGRY")
        # Obtains the distances of both side sensors.
        distiz_cm = dist_izquierda.get_distance_cm() 
        distha_cm = dist_derecha.get_distance_cm()

        # Conditional to avoid the default error that Lego Spike throws when the distance value is = NoneType
        if distiz_cm is not None and distha_cm is not None:
            # All these conditionals are responsible for straightening the robot.
            # So that no matter how far apart the walls are, it tries to stay in between them.

            if distiz_cm < distha_cm:
                giro.run_to_position(10) 
                motor.start(-20) 
                pass

            elif distiz_cm < 5:
                giro.run_to_position(20)
                motor.start(-20)
                pass

            elif distiz_cm > distha_cm:
                giro.run_to_position(355) 
                motor.start(-20)
                pass

            elif distha_cm < 5:
                giro.run_to_position(347)
                motor.start(-20)
                pass

            elif distiz_cm == distha_cm:
                giro.run_to_position(0)
                motor.start(-20)
                pass
        # In the case of NoneType the distance will accelerate a little, so as not to stand still.
        else:
            motor.start(-20)

        # By this logic the robot will know when it should break or simply pass according to the orange_value or violet_value.
        # These values depend on which value is detected first by the colour sensor.
        # In the case that it detects the orange colour first it will not take into account the violet and vice versa to know which direction to go.

        if (color1.get_red() - color1.get_green() > 67): # Orange
            if valor_naranja == True:
                pass
            elif valor_naranja == False:
                break
        elif (color1.get_reflected_light()<80): # Violet
            if valor_violeta == False:
                pass
            elif valor_violeta == True:
                break


def MainFinal():
    # Import of variables.
    global valor_violeta, valor_naranja, numero

    while True:
        # Obtain the gyroscope degrees and distances to perform the vehicle rotation successfully.
        grados = hub.motion_sensor.get_yaw_angle()
        distiz_cm = dist_izquierda.get_distance_cm()
        distha_cm = dist_derecha.get_distance_cm()

        # Object the orange colour by subtracting rg(b) as the colour sensor of this spike(2.0.8) version does not work properly.
        if (color1.get_red() - color1.get_green() > 67): # 65 # Naranja
            # As mentioned above change the purple_value and verify that the orange_value is false to perform the functions.
            # This is the process to verify which line will be taken into account.
            valor_violeta = False
            if valor_naranja == False:
                hub.light_matrix.show_image("HOUSE")
                # For each line you will add a section until you reach 12 which will be where you will complete the 3 laps.
                numero += 1
                while True:
                    grados = hub.motion_sensor.get_yaw_angle()
                    # If the degrees are less than 50, the robot will rotate until...

                    if grados < 50: 
                        giro.run_to_position(35)
                        motor.start(-45) 

                        # This conditional is not triggered very often because it will only happen if the turn is too tight.
                        # It will perform the action of a sharp movement in order to straighten up again.
                        if distiz_cm is not None and distha_cm is not None:
                            if distha_cm < 15:
                                giro.run_to_position(340)
                            if distiz_cm < 15:
                                giro.run_to_position(20)
                        else:
                            pass
                    # The robot will stop and slow down the cycle.
                    elif grados > 80:
                        motor.stop()
                        break

            # In case it detects the violet colour it will simply avoid it and will not take any action.
            elif (color1.get_reflected_light()<80):
                pass

        elif (color1.get_reflected_light()<80): # 30 # Violeta
            # Change the orange_value and verify that the purple_value is true to perform the functions.
            # This is the process to verify which line will be taken into account.
            valor_naranja = True
            if valor_violeta == True: # True
                hub.light_matrix.show_image("HAPPY")
                # For each line you will add a section until you reach 12 which will be where you will complete the 3 laps.
                numero += 1
                while True:
                    grados = hub.motion_sensor.get_yaw_angle()
                    # If the degrees are less than -50, the robot will rotate until...
                    
                    if grados > -50:
                        giro.run_to_position(335) # 340
                        motor.start(-50)

                        # This conditional is not triggered very often because it will only happen if the turn is too tight.
                        # It will perform the action of a sharp movement in order to straighten up again.
                        if distiz_cm is not None and distha_cm is not None:
                            if distha_cm < 15:
                                giro.run_to_position(30)
                            if distiz_cm < 15:
                                giro.run_to_position(340)
                        else:
                            pass

                    # If the degrees are more than -80, the robot will stop the cycle.
                    elif grados < (-80):
                        motor.stop()
                        giro.run_to_position(10)
                        break

            # In case it detects the orange colour it will simply avoid it and will not take any action.
            elif (color1.get_red() - color1.get_green() > 67):
                pass

        else:
            # I call an Else so that when it is neither purple nor orange, if it is white it will perform the Stability() function which is in charge of
            # of straightening the robot.
            if (color1.get_reflected_light()>91 and color1.get_reflected_light()<110): # Blanco
                Stability()

        # When numero reaches 12, the robot will stop performing the rest of the functions because it has already reached the 3 turns by adding the sections together.
        if numero == 12:
            print("Vueltas completadas.")
            # To make sure it ends in the middle I simply made it go on for a while and finally the programme ends.
            giro.run_to_position(0)
            motor.start(-10)
            wait_for_seconds(5.5)
            motor.stop()
            break

#Finally, I call the main function that links all the secondary functions.
MainFinal()
