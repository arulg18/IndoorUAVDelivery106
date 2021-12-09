#!/usr/bin/env python
import rospy
import numpy as np
import message_filters
from localization.msg import TimestampDistance
from std_msgs.msg import Float32
from geometry_msgs.msg import Pose
from math import sqrt


beacon_0 = np.array([0, 0.59, 1.78])
beacon_1 = np.array([3.87, 0.69, 1.53])
beacon_2 = np.array([3.17, 3.24, 1.66])
beacon_3 = np.array([0, 4.18, 1.70])

# beacon_0 = np.array([0, 0, 0])
# beacon_1 = np.array([10, 0, 0])
# beacon_2 = np.array([11, 7, 0])
# beacon_3 = np.array([5, 8, 0])
# beacons = np.vstack((beacon_0, beacon_1, beacon_2, beacon_3))


dist_offsets = [-0.825, -0.55, -0.3, -0.9]


publisher = None




# def trilateration(dist_0, dist_1, dist_2, dist_3):
# 	mag_0 = np.linalg.norm(beacon_0)
# 	mag_1 = np.linalg.norm(beacon_1)
# 	mag_2 = np.linalg.norm(beacon_2)
# 	mag_3 = np.linalg.norm(beacon_3)
# 	print("mag", mag_0, mag_1, mag_2, mag_3)

# 	A_0 = (beacon_0 - beacon_1)
# 	A_1 = (beacon_0 - beacon_2)
# 	A_2 = (beacon_0 - beacon_3)
# 	# A_0 = beacon_1 - beacon_0
# 	# A_1 = beacon_2 - beacon_0
# 	# A_2 = beacon_3 - beacon_0
# 	# print(A_0)
# 	A = 2 * np.vstack((A_0, A_1, A_2))
# 	print("A", A)

# 	b_0 = dist_1**2 - dist_0**2 + mag_0**2 - mag_1**2 
# 	b_1 = dist_2**2 - dist_0**2 + mag_0**2 - mag_2**2
# 	b_2 = dist_3**2 - dist_0**2 + mag_0**2 - mag_3**2

# 	b = np.vstack((b_0, b_1, b_2))
# 	print("b", b)
# 	return np.dot(np.matmul(np.linalg.pinv(np.matmul(A.T, A)), A.T), b)
# 	# return np.linalg.lstsq(A, b)[0]

def trilateration(distances):
    p1=np.array(distances[0][:3])
    p2=np.array(distances[1][:3])
    p3=np.array(distances[2][:3])       
    p4=np.array(distances[3][:3])
    r1=distances[0][-1]
    r2=distances[1][-1]
    r3=distances[2][-1]
    r4=distances[3][-1]
    e_x=(p2-p1)/np.linalg.norm(p2-p1)
    i=np.dot(e_x,(p3-p1))
    e_y=(p3-p1-(i*e_x))/(np.linalg.norm(p3-p1-(i*e_x)))
    e_z=np.cross(e_x,e_y)
    d=np.linalg.norm(p2-p1)
    j=np.dot(e_y,(p3-p1))
    x=((r1**2)-(r2**2)+(d**2))/(2*d)
    y=(((r1**2)-(r3**2)+(i**2)+(j**2))/(2*j))-((i/j)*(x))
    z1=np.sqrt(r1**2-x**2-y**2)
    z2=np.sqrt(r1**2-x**2-y**2)*(-1)
    ans1=p1+(x*e_x)+(y*e_y)+(z1*e_z)
    ans2=p1+(x*e_x)+(y*e_y)+(z2*e_z)
    dist1=np.linalg.norm(p4-ans1)
    dist2=np.linalg.norm(p4-ans2)
    if np.abs(r4-dist1)<np.abs(r4-dist2):
        return ans1
    else: 
        return ans2





# Called when message filter finds synchronize data
def received_sync_data(d0, d1, d2, d3):
	# Trilateration
	unfiltered_pose = Pose()

	# tri_out = trilateration(d0.distance, d1.distance, d2.distance, d3.distance)

	distances = np.array([[0, 0.59, 1.78, d0.distance - dist_offsets[0]], [3.87, 0.69, 1.53, d1.distance - dist_offsets[1]], [3.17, 3.24, 1.66, d2.distance -  - dist_offsets[2]], [0, 4.18, 1.70, d3.distance -  - dist_offsets[3]]])
	tri_out = trilateration(distances)
	tri_out += 0.5
	# tri_out[1] += 0.9
	unfiltered_pose.position.x = tri_out[0]
	unfiltered_pose.position.y = tri_out[1]
	unfiltered_pose.position.z = tri_out[2]

	
	# Compute [x, y] estimate and publish to some EKF topic
	publisher.publish(unfiltered_pose)



if __name__ == '__main__':
	rospy.init_node('listener', anonymous=True)
	
	# print(trilateration(sqrt(58), 3*sqrt(2), sqrt(32), sqrt(29)))

	publisher = rospy.Publisher("unfiltered_pose", Pose, queue_size=10)
	d0_sub = message_filters.Subscriber("distance_0", TimestampDistance)
	d1_sub = message_filters.Subscriber("distance_1", TimestampDistance)
	d2_sub = message_filters.Subscriber("distance_2", TimestampDistance)
	d3_sub = message_filters.Subscriber("distance_3", TimestampDistance)
	time_sync = message_filters.ApproximateTimeSynchronizer([d0_sub, d1_sub, d2_sub, d3_sub], queue_size=10, slop=0.5)
	time_sync.registerCallback(received_sync_data)
	

	r = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		r.sleep()
	
