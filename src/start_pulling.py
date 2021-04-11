#!/usr/bin/env python
import rospy,signal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64

roll = 0.0
pitch = 0.0
yaw =0.0
atfront =0.0
atback =5.0
atside = 0.0
atside_initial = 0.0
x_position_2=0.0
x_position_1=0.0
x_position = 0.0
initial = 0
initial_switch=True
speed_value= 0.01


def exit_gracefully(sig,frame):
    twist = Twist()
    pub.publish(twist)
    rospy.signal_shutdown("Stop")

def range_filter(lidar_data):
    global atside
    atside = lidar_data.ranges[90]

def main():
    ## VARIABLES
    global twist,pub
    switch = True
    twist = Twist()

    sub_range = rospy.Subscriber("scan",LaserScan,range_filter)
    pub = rospy.Publisher('cmd_vel',Twist,queue_size=10,latch = False)
    ##To shutdown bucket brigade
    signal.signal(signal.SIGINT,exit_gracefully)
    #LOOP

    while not rospy.is_shutdown():
        if atside< 0.3 and atside != 0 and switch== True:
            twist.linear.x = speed_value
            print(twist.linear.x)
            switch = False
            print("Apple")


        pub.publish(twist)
        rospy.Rate(10).sleep()

if __name__=="__main__":
    rospy.init_node('BucketBrigade')
    main()
    rospy.spin()
