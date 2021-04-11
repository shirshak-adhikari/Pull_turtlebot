#!/usr/bin/env python
import rospy,signal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64


atside = 0.0
speed_value= 0.02
twist = Twist()



def exit_gracefully(sig,frame):
    twist = Twist()
    twist.linear.x= 0.0
    pub.publish(twist)
    rospy.signal_shutdown("Stop")
    print("Last MSG")

def range_filter(lidar_data):
    global atside
    atside= lidar_data.ranges[90]


def main():
    switch = True

    while not rospy.is_shutdown():
        if atside< 0.3 and atside != 0 and switch== True:
            twist.linear.x = speed_value
            print(twist.linear.x)
            switch = False



        pub.publish(twist)
        rospy.Rate(10).sleep()



if __name__ == '__main__':
    rospy.init_node('robot_pull')
    sub_range = rospy.Subscriber("scan",LaserScan,range_filter)
    pub = rospy.Publisher('cmd_vel',Twist,queue_size=1,latch = False)
    signal.signal(signal.SIGINT,exit_gracefully)
    main()
    rospy.spin()
