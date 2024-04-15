# #Exercise Title:    Remote Control for the TurtleBot3 Burger
# #Class:             BHME20
# #Date:              16.10.2023


# import select
# import rclpy
# import os
# import sys 

# from geometry_msgs.msg import Twist
# from rclpy.qos import QoSProfile
# #import msvcrt

# #wird benoetigt. um auf die Tastatur (Buffer) zugreifen zu koennen
# if os.name == 'nt':
#     import msvcrt
# else:
#     import termios
#     import tty

# msg = """ #globale Variable; msg = message
# Excercise:  Uebung 2 - RemoteCtrl
# Class:      BHME20
# Date:       23.10.2023
# """

# e = """
# Communications Failed
# """

# """
# 72... Cursor Beschleunigen
# 80... Cursor Bremsen
# 75... Cursor Drehung nach links
# 77... Cursor Drehung nach rechts
# """
# key_ctrl = [72, 80, 75, 77]


# #Physikalische Grenzen des Roboters
# MAX_LIN_VEL = 0.22          #m/s  #linear = von oben nach unten
# MAX_ANG_VEL = 2.84          #rad/s #angular = drehen 

# LIN_VEL_STEP_SIZE = 0.01    #m/s
# ANG_VEL_STEP_SIZE = 0.1     #rad/s


# def get_key(): #Funktion
#     old_settings = termios.tcgetattr(sys.stdin) #Alte einstellungen des Tastaturzugriffs merken
    
#     key = '' #Standartwert wenn nichts von der tastatur wurde
    
#     try:

#         tty.setraw(sys.stdin.fileno())
#         while True:
#             rlist, _, _ = select.select([sys.stdin], [], [], 0.1) #s wird ein timeout von 0.1 
#             if rlist:                                             #sekunde eingestellt
#                 key += os.read(sys.stdin.fileno(), 1).decode("utf-8") #man kann es zeichenweise einlesen; 
#             else:                                                    #in dem fall kann man 1 zeichen 
#                 break                                                #einlesen rewad(1)
#     finally: 
#         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

#     return key
        
# def main():
    
#     key_null_entered = False

#     rclpy.init()

#     qos = QoSProfile(depth=10)
#     node = rclpy.create_node('remotectrl')  #ros2 node lidte -> alle 
#     pub = node.create_publisher(Twist, 'cmd_vel', qos)
#                             #Datentyp, Variable, History wie lange er 
#                                                 #die Nachricht speichert

#     vel = Twist() #wir erstellen eine leere nachricht mit datentyp Twist
#                   #und den speichere ich mir auf vel ab
#                   #variable welche die Geschwindigkeitsvorgaben enthält
#                   #vom Datentyp Twist
                  
#     try:          #alles was unterhalb von try steht, wird einmal ausgeführt
#         while(1):   
#             key = get_key()
#             if key != '':
#                 str = "String: " + key.replace(chr(0x1B), '^')
#                 print(str)
#                 if key == "0x03": #Steuerung + c wurde gedrückt 
#                     vel.linear.x = 0.0 #m/s
#                     vel.angular.z = 0.0 #rad/s
#                     pub.publish(vel)
#                     break
#                 if (key == "\x1B[A"): #Pfeiltaste nach Oben; Hexcode für Escape
#                     print("Roboter beschleunigt in X-Richtung")
#                     vel.linear.x = vel.linear.x + LIN_VEL_STEP_SIZE
#                     if vel.linear.x > MAX_LIN_VEL:
#                         vel.linear.x = MAX_LIN_VEL

#                 elif (key == "\x1B[B"): #Pfeiltaste nach Unten
#                     print("Roboter verringert die Beschleunigung in X-Richtung")
#                     vel.linear.x = vel.linear.x - LIN_VEL_STEP_SIZE
#                     if vel.linear.x < MAX_LIN_VEL:
#                         vel.linear.x = MAX_LIN_VEL

#                 elif (key == "\x1B[C"): #Pferiltaste nach rechts
#                     print("Roboter dreht sich im Uhrzeigersinn")
#                     vel.angular.z = vel.angular.z + ANG_VEL_STEP_SIZE
#                     if vel.angular.z > MAX_ANG_VEL:
#                         vel.angular.z = MAX_ANG_VEL

#                 elif (key == "\x1B[D"): #Pfeiltaste nach links
#                     print("Roboter dreht sich gegen den Uhrzeigersinn")
#                     vel.angular.z = vel.angular.z + ANG_VEL_STEP_SIZE
#                     if vel.angular.z < MAX_ANG_VEL:
#                         vel.angular.z = MAX_ANG_VEL
#                 #if ord(key) == 0x00:
#                 #   key_null_entered = True

#                 #if key_null_entered == True and key_ctrl[0] == ord(key): #Beschleunigen
#                 #   vel.linear.x
#                 #elif key_null_entered == True and key_ctrl[1] == ord(key): # Bremsen
#                 #    pass
                
#                 print("V.lin.x = %.2f, V.ang.z = %.2f" % (vel.linear.x, vel.angular.z))
#                 pub.publish(vel) # wir schicken eine Nachrichten raus und der Roboter
#                                 # holt sich die Nahcricht, wenn er sie braucht.
#                                 # Nachricht mit den neuen Geschiwndigkeitsvorgaben (vel) 
#                                 # wird in das Netzwerk gesendet

#     except Exception as e:
#         print(e)

#     finally:
#         pass
             
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()

#Exercise Title:    Remote Control for the TurtleBot3 Burger
#Group:             ?
#Class:             ?
#Date:              ?

import rclpy
import os
import select
import sys

from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile


#wird benoetigt um auf die Tastatur (Buffer) zugreifen zu koennen
if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

msg = """
Excercise:  Uebung 2 - RemoteCtrl
Group:      -
Class:      4 BHME
Date:       23.10.2023
"""

e = """
Communications Failed
"""

"""
72... Cursor Beschleunigen
80... Cursor Bremsen
75... Cursor Drehung nach links
77... Cursor Drehung nach rechts
"""
key_ctrl = [72, 80, 75, 77]


#Physikalische Grenzen des Roboters
MAX_LIN_VEL = 0.22          #m/s
MAX_ANG_VEL = 2.84          #rad/s

LIN_VEL_STEP_SIZE = 0.01    #m/s
ANG_VEL_STEP_SIZE = 0.1     #rad/s

def get_key():
    old_settings = termios.tcgetattr(sys.stdin) #Alte Einstellunbgen des Tasturzugriffs merken

    key = '' #Standardwert wenn nichts von der Tastur gelesen wurde

    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1) #Es wird ein Timeout von 0.1 s eingestellt
            if rlist:
                key += os.read(sys.stdin.fileno(), 1).decode("utf-8")
            else:
                break
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    return key
 
def main():
    
    rclpy.init()

    qos = QoSProfile(depth=10)
    node = rclpy.create_node('remotectrl')      #//ros2 node list -> alle laufenden nodes im terminao auflisten
    pub = node.create_publisher(Twist, 'cmd_vel', qos)

    vel = Twist()   #Variable welch die Geschwindigkeitsvorgaben enthält

    try:
        while(1):
            key = get_key()
            if key != '':
                str = "String: " + key.replace(chr(0x1B), '^')
                print(str)
                if key == "\x03": #STRG+C wurde gedrueckt
                    vel.linear.x = 0.0 #m/s
                    vel.angularremotectrl.z = 0.0 #rad/s
                    pub.publish(vel)
                    break
                elif key == "\x1B":
                    vel.linear.x = 0.0
                    vel.angular.z = 0.0
                
                if (key == "\x1B[A"):   #Pfeiltaste: Vorne
                    print("Roboter erhoeht beschleunigt in X-Richtung")
                    vel.linear.x = vel.linear.x + LIN_VEL_STEP_SIZE
                    if vel.linear.x > MAX_LIN_VEL:
                        vel.linear.x = MAX_LIN_VEL
                    
                elif (key == "\x1B[B"): #Pfeiltaste: Unten
                    print ("Roboter verringert die Beschleunigung in X-Richtung")
                    vel.linear.x = vel.linear.x - LIN_VEL_STEP_SIZE
                    if vel.linear.x < -MAX_LIN_VEL:
                        vel.linear.x = -MAX_LIN_VEL
                elif (key == "\x1B[C"): #Pfeiltaste: Rechts
                    print ("Roboter erhöht Drehung in Z-Richtung")
                    vel.angular.z = vel.angular.z + ANG_VEL_STEP_SIZE
                    if vel.angular.z > MAX_ANG_VEL:
                        vel.angular.z = MAX_ANG_VEL
                elif (key == "\x1B[D"):
                    print ("Roboter bremst Drehung in Z-Richtung")
                    vel.angular.z = vel.angular.z - ANG_VEL_STEP_SIZE
                    if vel.angular.z < -MAX_ANG_VEL:
                        vel.angular.z = -MAX_ANG_VEL

                
                print ("V.lin.x = %.2f, V.ang.z = %.2f" % (vel.linear.x, vel.angular.z))
                
                # print ("V.lin.x = %.2f" % vel.linear.x,
                #        "V.ang.z = %.2f" % vel.angular.z)
                
                pub.publish(vel)    #Nachricht mit den neuen Geschwindigkeitsvorgaben
                                    #(vel) wird in das Netzwerk gesendet

    except Exception as e:
        print(e)

    finally:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    