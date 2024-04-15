# import rclpy
# from rclpy.node import Node

# from geometry_msgs.msg import Twist # topic cm_vel
# from sensor_msgs.msg import LaserScan #topicScan

# from rclpy.qos import QoSProfile
# from rclpy.qos import qos_profile_sensor_data

# class ObstacleAvoidanceSimple(Node):
#     def __init__(self):             #Konstruktor mit KLasse init
#         super().__inti__('ObstacleAvoidanceSimple')

#         self.scan = None #speichert die Messdaten
#         self.cdm_vel = Twist() #vektor mit der Geschwindigkeitsvorgabe (Vortwärtsgeschw. x, Drehgeschw umd die Z-Achse)
 
#         #Konstanten Variablen
#         self.SEGMENT_ANGLE_DEG = 60 #breite(öffnungswinkel) eines Segments
#         self.OBSTACLE_DIS = 0.30 #Mindestabstand zu einem Hinderniss
        
#         self.NORMAL_LIN_VEL = 0.15 #Normale Geschw. wenn kein Hindernis im Weg ist
#         self.TRANS_LIN_VEL = -0.05 #Lineare Geschw. sobald kein Hinderniss erkannt wurde
#         self.TRANS_ANG_VEL = 1.0 #Drehgeschw. sobald ein Hindernis erkannt wurde

#                         #Infos bekommen sie vom Node
#         self.scan_sub = self.create_subscription(LaserScan, 'scan',
#                                                  self.scan_callback,
#                                                  qos_profile_sensor_data)
#         self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', QoSProfile(depth=10) )

#         self.update_timer = self.create_timer(0.1, self.timer_callback)
#                                 #Funktion timer_callback wird aufgerufen bei create_timer
#                                 #man kann auch mehrer Timer anlegen

#     def scan_callback(self, msg): #scan callback wird automatisiert aufgerufen von ROS 
#         self.scan = msg           #wann wird sie aufgerufen: Zeile 26 - scan_callback
#         print (self.scan)         #wo sind die Daten drinnen: Array; Nachricht ist in msg drinnen

#     def timer_callback(self):
#         segment, ang_vel = self.obstacle_avoidance()
#         self.steer(segment, ang_vel)


# #neue Methode- Algorythmus, Sektor einteilung
#     def obstacle_avoidance(self):
#         if self.scan == None: #abfragen ob Scandaten vorhanden sind
#             return 0, 0.0 #Rückgabewerte: 1. Segment, 2. Drehgeschwindigkeit

# #1. Berechnung der Segmentanzahl
#         segment_size = int(360 / self.SEGMENT_ANGLE_DEG+0.5) #int drüber schreiben, damit er keine Kommerzahl bekommen
#                                                              #+0.5 = zum Aufrunden
# #2. Festlegung der Suchreihenfolge
#         segment_order = [0] * segment_size
#         for i in range (int(segment_size/2)): #range erstellt ein range-objekt 
#             segment_order[2*i] = i                     #range objekt (i) erstellt eine liste mit einträgen mit beginn 0 & endet bei segmentgröße halbe
#             segment_order[2*i+1] = segment_size -i -1
#         segment_order[-1] = int(segment_size/2) #-1= man greift auf das letzte Element zu
#         print("Segment order: ", segment_order)

#         #Beispiel: 6 Segmente -> segment_order: [0, 5, 1, 4, 2, 3]  
             
# #3.Bestimmung in welchen Segmenten Abstandsverletzungen vorliegen!
# # --> wo befindet sich ein Hindernis
#         segment_distances = segment_size * [[]]
#         segment_distances_size = int(len(self.scan.ranges) / segment_size) #in scan Zwischengespeichert die Daten
#         begin = -int(segment_distances_size/2)                             #len (gibt die Länge vom Array zurück)
#         end = int(segment_distances_size/2)
#         #alle Entfernungen von Segment 0 gespeichert (rund um die 0-Achse)
#         distance = self.scan.ranges[begin : ] + self.scan.ranged[0: end] #entfernungen zum hinderniss vom Anfang gespeichrt (rote Pfeile in der Mitte bei der Zeichnung in OneNote)

#         segment_distances[0] = [x for x in distance if x<=self.OBSTACLE_DIS and x != 'inf']
#         #wenn ein x in unserem radius drinnen ist (x<=self.OBSTACLE_DIS), soll er sich dies merken
#         #inf: es muss numerisch sein, also darf nicht unendlich sein!                                                                
#         print("Segment distance: ", segment_distances)

#         for i in range(1, segment_size):
#             begin = end 
#             end = begin + segment_distances_size
#             distance = self.scan.ranges[begin : end]
#             segment_distances[i] = [x for x in distance if x<=self.OBSTACLE_DIS and x != 'inf']

#             #hier sind jetzt Daten in der Liste, von den Abstenden zu den Hindernissen oder
#             #eben von keinen Hindernissen

#         for i in segment_order: #dorthin fahren wo der geringste Abstand ist
#             if len(segment_distances[i]) == 0: #keine Hindernisse gefunden
#                 break
#         segment = i

# #Berechnung der Drehgeschwindigkeit:
#         if(segment == 0): #kein Hindernis im weg
#             ang_vel = 0.0
#         #Roboter ist von Hindernissen umgeben
#         elif segment == segment_order[-1] and len(segment_distances[segment]) != 0:
#             ang_vel == 0.0
#             segment = -1 #ungultiger WErt: Roboter soll stehen bleiben
#         elif segment > int(segment_size/2):    #Drehung nach links
#            ang_vel = -self.TRANS_ANG_VEL 
#         else: #Drehung nach rechts
#             ang_vel = +self.TRANS_ANG_VEL

#         return segment, ang_vel
    
#     def steer (self, segment, ang_vel=0.0):
#         #Wenn kein Segment zurückgegeben wird, soll der Roboter geradeaus fahren
#         if segment == 0: 
#             self.cdm_vel.linear.x = self.NORMAL_LIN_VEL
#             self.cdm_vel.angular.z= 0.0
#         #Roboter weicht einem Hindernis aus 
#         elif segment > 0: 
#             self.cdm_vel.linear.x = self.TRANS_LIN_VEL
#             self.cdm_vel.angular.z = ang_vel
#         #Um den Roboter herum sind Hindernisse -> stehen bleiben 
#         else: #segment < 0
#             self.cdm_vel.linear.x = 0.0 
#             self.cdm_vel.angular.z = 0.0 

#         #Nullsetzung aller unplausiblen Werten -> Sicherheitsmaßnahmen 
#         self.cdm_vel.linear.y = 0.0 
#         self.cdm_vel.linear.z = 0.0 
#         self.cdm_vel.angular.x = 0.0
#         self.cdm_vel.angular.y = 0.0 

#         #Übergabe der Parameter an den Roboter mittels Publisher 
#         self.cmd_vel_pub.publish(self.cdm_vel)


# def main():
#     rclpy.init()

#     obstacleavoidance_node = ObstacleAvoidanceSimple()
#     rclpy.spin(obstacleavoidance_node)
#     obstacleavoidance_node.destroy_node()

#     rclpy.shutdown()

import rclpy
from rclpy.node import Node
import math

from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class ObastacleAvoidanceSimple(Node):
    def __init__(self, regional_angle_deg = 60, normal_lin_vel=0.2, trans_lin_vel=-0.05, trans_ang_vel=1.0):
        super().__init__('ObstacleAvoidanceSimple')

        """************************************************************
        ** Initialise variables
        ************************************************************"""

        self.scan = None
        self.cmd_vel_raw = None

        self.REGIONAL_ANGLE_DEG = regional_angle_deg
        self.OBSTACLE_DIST = 0.30

        self.NORMAL_LIN_VEL = normal_lin_vel
        self.TRANS_LIN_VEL  = trans_lin_vel
        self.TRANS_ANG_VEL  = trans_ang_vel

                
        self.vel_obj = Twist()

        """************************************************************
        ** Initialise ROS publishers and subscribers
        ************************************************************"""
        qos = QoSProfile(depth=10)

        # Initialise publishers - use method create_publisher

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', qos)

        # Initialise subscribers - use method create_subscription
        self.cmd_scan_sub = self.create_subscription(LaserScan, 'scan', 
                            self.scan_callback, qos_profile_sensor_data)
        
        
        self.cmd_vel_raw_sub = self.create_subscription(Twist,'cmd_vel_raw',
                               self.cmd_vel_raw_callback,qos)
        
        """************************************************************
        ** Initialise timers
        ************************************************************"""
        self.update_timer = self.create_timer(
            0.010,  # unit: s
            self.timer_callback)
    
    def scan_callback(self, msg):
        self.scan = msg
    
    def cmd_vel_raw_callback(self, msg):    #die Nachricht msg wird in cmdvelraw gespeichert
        self.cmd_vel_raw = msg
        print(msg)

    def timer_callback(self):
        segment, z_vel_angular = self.obstacle_avoidance()
        self.steer( segment, z_vel_angular )


    def obstacle_avoidance(self):
        if self.scan == None:
            return 0, 0.0
        
        #Berechnung der Segmentanzahl...
        segment_size = int(360 / self.REGIONAL_ANGLE_DEG + 0.5)
        segment_distance_size = int(len(self.scan.ranges) / segment_size)

        #Die Suchpriorisierung festelegen. Das Array enthält die Nummern der Segmente
        #segement_order = [0, 1, 6, 2, 5, 3, 4] #.....
        segment_order = [0] * segment_size
        for i in range(int((segment_size)/2)):
            segment_order[2*i] = i
            segment_order[2*i+1] = segment_size-i-1
        segment_order[-1] = int((segment_size)/2)

        #Bestimmung welche Regionen Abstandsverletzungen enthält. 
        #D.h. das Array nach Abständen < self.OBSTACLE_DIST filtern
        segment_distances = segment_size * [[]]      #Array mit leeren Feldern je Segment erstellen 
        begin = -int(segment_distance_size/2)
        end = begin + segment_distance_size
        distances = self.scan.ranges[begin : ] + self.scan.ranges[ : end]
        #Abstandsverletzung vor dem Roboter = Segment 0 filtern/berechnen
        segment_distances[0] = [x for x in distances if x <= self.OBSTACLE_DIST and x != 'inf']
        #Abstandsverletzungen in den restlichen Segmenten suchen
        for i in range(1,segment_size):
            begin = end
            end = begin + segment_distance_size
            distances = self.scan.ranges[begin : end]
            segment_distances[i] = [x for x in distances if (x <= self.OBSTACLE_DIST) and (x != 'inf')]
        
        #TODO - Beste Ausweichroute suchen - Siehe 3. Flussdiagramm
        #Segement in der Reihenfolge ihrer Priorität durchsuchen -> segment_order
        #Leere Segmente werden bevorzugt (keine Hindernisse), wenn keine Leeren Segmente gefunden werden,
        #könnte der Robot das Segment mit den größen Absthänden anfahren

        for i in segment_order:
            #print ("Segment-Schleife: ",  i)
            if len(segment_distances[i])==0: #keine Hindernisse im Segment gefunden
                break
        segment = i
        #Rückgabewert -> Freies Segment oder Beste Ausweichmöglichkeit
        # return segmentnr, z_vel_angular
        
        #TODO - Berechnung der Drehgeschwindigkeit
        #0.0 rad/s, -xx rad/s, +xx rad/s
        if segment == 0:
            ang_vel = 0.0
        elif segment == segment_order[-1] and len(segment_distances[segment]) == 0:
            ang_vel = 0.0
            segment = -1
        elif segment > int((segment_size)/2): #turn left
            #region = region - region_size
            ang_vel = -self.TRANS_ANG_VEL
        else:
            ang_vel = self.TRANS_ANG_VEL

        #TODO - Rückgabe des Ausweichsegments und der Drehgeschindigkeit
        #return ....

        print("Segment: ", segment, "Vel: ", ang_vel)
        return segment, ang_vel

    def steer(self, segment, ang_vel=0.0):
        if segment == 0:
            if (self.cmd_vel_raw != None): #Geschwindigkeitsvorgabe von der Fernbedieungung erhalten 
                self.vel_obj.linear.x = self.cmd_vel_raw.linear.x
                self.vel_obj.angular.z = self.cmd_vel_raw.angular.z
           
            else:
                self.vel_obj.linear.x = self.NORMAL_LIN_VEL
                self.vel_obj.angular.z = 0.0
        elif segment > 0:
            self.vel_obj.linear.x = self.TRANS_LIN_VEL
            self.vel_obj.angular.z = ang_vel
        else: #stop the robot!
            self.vel_obj.linear.x = 0.0
            self.vel_obj.angular.z = 0.0

        self.vel_obj.linear.y  = 0.0
        self.vel_obj.linear.z  = 0.0
        self.vel_obj.angular.x = 0.0
        self.vel_obj.angular.y = 0.0

        self.cmd_vel_pub.publish(self.vel_obj)

    def __del__(self):
        pass
        

def main(args=None):
    rclpy.init(args=args)

    obstacleavoidance_node = ObastacleAvoidanceSimple()

    rclpy.spin(obstacleavoidance_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    obstacleavoidance_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()