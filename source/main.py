from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *


hub = PrimeHub()
color1 =ColorSensor("D")
motor = Motor("B")
giro = Motor("C")

dist_izquierda = DistanceSensor("A")
dist_derecha = DistanceSensor("E")
dist_frontal = DistanceSensor("F")


valor_violeta = True
valor_naranja = False
numero = 0




def GiroscopioCalculo():
    giro.run_for_degrees(0, 100)
    wait_for_seconds(2)
    hub.motion_sensor.reset_yaw_angle()

    while True:
        grados = hub.motion_sensor.get_yaw_angle()
        wait_for_seconds(1)
        print(grados)

def Giro():
    giro.run_to_position(20)
    # giro.run_to_position(355)

def Stability():
    giro.run_to_position(0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    wait_for_seconds(1)

    while True:
        hub.light_matrix.show_image("ANGRY")
        distiz_cm = dist_izquierda.get_distance_cm()
        distha_cm = dist_derecha.get_distance_cm()
        distfz_cm = dist_frontal.get_distance_cm()

        if distiz_cm is not None and distha_cm is not None:
            if distiz_cm < distha_cm:
                print("Giro levemente Derecha")
                giro.run_to_position(10, "shortest path", 100) # 10
                motor.start(-30) # -15 

                if distiz_cm < 5:
                    print("Giro bruscamente a la derecha")
                    giro.run_to_position(15, "shortest path", 100)
                    motor.start(-30)
            elif distiz_cm > distha_cm:
                print("Giro levemente Izquierda")
                giro.run_to_position(355, "shortest path", 100) # 355
                motor.start(-30)
                if distha_cm < 5:
                    print("Giro bruscamente a la izquierda")
                    giro.run_to_position(350, "shortest path", 100)
                    wait_for_seconds(1)
                    pass
            elif distiz_cm == distha_cm:
                print("Estoy en 0")
                giro.run_to_position(0, "shortest path", 100)
                motor.start(-15)
                wait_for_seconds(1)
                pass
        else:
            motor.start(-15)


        if (color1.get_red() - color1.get_green() > 65): # Naranja
            if valor_naranja == True:
                pass
            elif valor_naranja == False:
                break
        elif (color1.get_reflected_light()<80): # Violeta
            if valor_violeta == False:
                pass
            elif valor_violeta == True:
                break


def MainFinal():
    global valor_violeta, valor_naranja, numero


    while True:
        grados = hub.motion_sensor.get_yaw_angle()
        distiz_cm = dist_izquierda.get_distance_cm()
        distha_cm = dist_derecha.get_distance_cm()
        distfz_cm = dist_frontal.get_distance_cm()

        if (color1.get_red() - color1.get_green() > 65):# Naranja
            print("Color Naranja Detectado | +1 Parte")
            valor_violeta = False
            if valor_naranja == False:
                hub.light_matrix.show_image("HOUSE")
                print(grados)
                numero += 1
                while True:
                    grados = hub.motion_sensor.get_yaw_angle()
                    if grados < 80: # 55
                        print("Girando hasta 50 grados.")
                        giro.run_to_position(35) # 90 # 25 # 30
                        motor.start(-20) # 15

                        if distiz_cm is not None and distha_cm is not None:
                            if distha_cm < 15:
                                giro.run_to_position(340)
                                print("Giro bruscamente hacia la derecha")
                            if distiz_cm < 15:
                                giro.run_to_position(20)
                                print("Giro bruscamente hacia la izquierda")
                        else:
                            pass

                    elif grados > 80:
                        motor.stop()
                        print("Giro de 50 grados fue exitoso.")
                        break
                    # else:
                    #    motor.stop()
                    #    print("Giro de 55 grados exitoso.")
                    #    break

            elif (color1.get_reflected_light()<80):
                pass


        elif (color1.get_reflected_light()<80): # 30 # Violeta
            valor_naranja = True
            if valor_violeta == True: # True
                hub.light_matrix.show_image("HAPPY")
                print(grados)
                numero += 1
                while True:
                    grados = hub.motion_sensor.get_yaw_angle()
                    if grados > -80:
                        print("Girando hasta -50 grados")
                        giro.run_to_position(335) # 340
                        motor.start(-20)

                        if distiz_cm is not None and distha_cm is not None:
                            if distha_cm < 15:
                                giro.run_to_position(30)
                            if distiz_cm < 15:
                                giro.run_to_position(340)
                        else:
                            pass

                    elif grados < (-80):
                        motor.stop()
                        print("Giro de -50 grados fue exitoso.")
                        giro.run_to_position(10, "shortest path", 100)
                        break

            elif (color1.get_red() - color1.get_green() > 65):
                pass

        else:
            if (color1.get_reflected_light()>91 and color1.get_reflected_light()<110): # Blanco
                Stability()
                print("Detectado Blanco")

        if numero == 12:
            print("Vueltas completadas.")
            motor.start(-10)
            wait_for_seconds(3)
            motor.stop()
            break

MainFinal()
