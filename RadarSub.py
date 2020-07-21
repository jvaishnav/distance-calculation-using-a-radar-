#!/usr/bin/python
import rospy
import time
from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import Float32MultiArray
from adafruit_servokit import ServoKit
from std_msgs.msg import String
from can_msgs.msg import Frame 

kit = ServoKit(channels=16)
kit.servo[0].angle = 88
kit.continuous_servo[1].throttle = 0.23



def callback1(data):
    print("going")
    cond = data.data
    #cond = String
    if cond == "A":
      print("stop")
      kit.servo[4].angle = 88
      kit.continuous_servo[2].throttle = 0.0
    elif cond == "B":
      print("stop")
      kit.servo[4].angle = 88
      kit.continuous_servo[2].throttle = 0
    elif cond == "C":
      print("right")
      kit.servo[4].angle = 142
      kit.continuous_servo[2].throttle = 0.25
    elif cond == "D":
      print("left")
      kit.servo[4].angle = 45
      kit.continuous_servo[2].throttle = 0.25
    elif cond == "E":
      print("straight")
      kit.servo[4].angle = 88
      kit.continuous_servo[2].throttle = 0.25

  
def listener1():
    rospy.init_node('listener1', anonymous=True)

    rospy.Subscriber("Radar", String, callback1)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener1()

