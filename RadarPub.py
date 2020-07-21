#!/usr/bin/python
import rospy
from can_msgs.msg import Frame
#from std_msgs.msg import Float
from std_msgs.msg import String
from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import Float32MultiArray
import os,time

global  All_Rdis_Left
global All_Rdis_Center
global All_Rdis_Right
def RadarPub(data):
 
 Radar_Dist = Float32MultiArray()
 Radar_Dist.data = [0,0,0]
 if (data.id != 1343):
  a = UInt8MultiArray
  a = [0,0,0,0,0,0,0,0] # data bytes
 print ("data", data)

 for i in range (8):
      a[i] = ord(data.data[i])
      print ("a", a)
      byte_L5 = '{0:08b}'.format(a[5])
      byte_H6 = '{0:08b}'.format(a[6]) 
      Radial_angle = byte_H6[3:8]+byte_L5[0:6]
      Radial_angle = int(Radial_angle,2)
      Radial_angle = Radial_angle*0.1     # scaled value
      if (Radial_angle > 102.3):
        Radial_angle = Radial_angle - 204.8
      else:
        Radial_angle = Radial_angle
      angle = round(Radial_angle, 2)
      print"Scaled_Radial_angle = " , angle, "Degree"

      byte_L0 = '{0:08b}'.format(a[0])
      byte_H1 = '{0:08b}'.format(a[1]) 
      Radial_range = byte_H1[1:8]+byte_L0
      Radial_range = int(Radial_range,2)
      Radial_range = Radial_range*0.01     # scaled value
      R_range = (round(Radial_range, 2))
      print"Scaled_Radial_range = " , R_range, "m"
 
 if data.id < 1343 :   
      if (angle >= -15 and  angle <= 15): # Center Object distance
        print ("Center",angle)
        string_range = str(R_range)
        All_Rdis_Center.append(R_range)
        print ("Centre dis", min(All_Rdis_Center))

      elif (angle < -15 and  angle >= -45): # Left Object distance
        print(" Left ",angle)
        string_range = str(R_range)
        All_Rdis_Left.append(R_range)
        print ("Left dis", min(All_Rdis_Left))

      elif (angle > 15 and  angle <=45): # Right Object distance
        print(" Right ",angle)
        string_range = str(R_range)
        All_Rdis_Right.append(R_range)
        print ("Right dis", min(All_Rdis_Right))
      
      
 elif data.id >=1343:


        Rdis_Center = min (All_Rdis_Center)
        Rdis_Left = min (All_Rdis_Left)
        Rdis_Right = min (All_Rdis_Right)
        Radar_Dist= [Rdis_Left, Rdis_Center, Rdis_Right]
        print(Radar_Dist)

        global cond
        cond = String   
        '''if Rdis_Center <= 2 and Rdis_Left <= 2 and Rdis_Right <= 2:
           cond = "A"
           print("stop") 
        if Rdis_Center <= 2:
           cond = "A"
           print("stop")
        elif Rdis_Center <= 2 and Rdis_Left <= 2 and Rdis_Right >= 2: 
           cond = "B"
           print("go right")
        elif Rdis_Center <= 2 and Rdis_Left >= 2 and Rdis_Right <= 2:
           cond = "C"
           print("go left")
        elif Rdis_Center <= 2 and Rdis_Left >= 2 and Rdis_Right >= 2:
           if Rdis_Left > Rdis_Right:
              cond = "C"
              print("go left")
           else:
              print("go right")
              cond = "B"'''
        if Rdis_Center <= 1.5:
           cond = "A"
           print("Stop")
        elif Rdis_Center <= 1.5 and Rdis_Left <= 1.5 and Rdis_Right <= 1.5: 
           cond = "B"
           print("stop")
        elif Rdis_Left <= 1.5: 
           cond = "C"
           print("go right")
        elif Rdis_Right <= 1.5:
           cond = "D"
           print("go left")
        else:
           cond = "E"
           print("goes straight")
        '''
        #print (" Radar_Center", Rdis_Center)
        #print (" Radar_Left", Rdis_Left)
        #print (" Radar_Right", Rdis_Right)
        print(Radar_Dist)
        #key = input()    '''  
        pub = rospy.Publisher("Radar", String, queue_size = 10)
        pub.publish(cond)
        #rospy.loginfo(Radar_Dist)
       
        del All_Rdis_Center[:]
        del All_Rdis_Left[:]
        del All_Rdis_Right[:]
    
  

def listener():
    rospy.init_node('listener', anonymous = True)
    rospy.Subscriber('/can_tx', Frame, RadarPub, queue_size = 64)
    rospy.spin()


if __name__ == '__main__':

    global R_range
    global angle
    ange = '0'
    All_Rdis_Center = Float32MultiArray
    All_Rdis_Center = []
    All_Rdis_Left = Float32MultiArray
    All_Rdis_Left = []
    All_Rdis_Right = Float32MultiArray
    All_Rdis_Right = []
    All_Rdis_Center.append(ange)
    All_Rdis_Left.append(ange)
    All_Rdis_Right.append(ange)
    listener()


