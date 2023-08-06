import pybullet as p
import time
import math

p.connect(p.GUI)

cubeId = p.createCollisionShape(p.GEOM_BOX,halfExtents=[0.5,0.5,0.5])
p.changeVisualShape(cubeId,-1,rgbaColor=[1,0,0,1])
p.loadURDF("plane.urdf")
boxUid = p.createMultiBody(1,cubeId,-1)
#boxUid = p.createMultiBody(1,cubeId,-1,basePosition,baseOrientation)
#bid = p.createConstraint(p.cubeId,-1,-1,-1,p.JOINT_FIXED,[0,0,0],[0,0,0],[0,0,0])
#cubeId = p.loadURDF("cube_small.urdf",0,0,1)
p.setGravity(0,0,-10)
p.setRealTimeSimulation(1)
cid = p.createConstraint(cubeId,-1,-1,-1,p.JOINT_FIXED,[0,0,0],[0,0,0],[0,0,1])
#print cid
#print p.getConstraintUniqueId(0)
prev=[0,0,1]
a=-math.pi
while 1:
	a=a+0.01
	if (a>math.pi):
		a=-math.pi
	time.sleep(.01)
	p.setGravity(0,0,-10)
	pivot=[a,0,1]
	orn = p.getQuaternionFromEuler([a,0,0])
	p.changeConstraint(cid,pivot,jointChildFrameOrientation=orn, maxForce=50)

p.removeConstraint(cid)
