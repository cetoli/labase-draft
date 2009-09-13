from visual import *
phi=(1+sqrt(5))/2
greek=(.9,.8,.7)
bord=(.5,.4,.3)
bord=(.9,.7,.6)
ellipsoid(size=(16.18,10,16.18), color=greek)
#ellipsoid( color=greek)
b=ring(color=bord, axis=(0,1,0), radius=2*phi, thickness=1.618/2, pos=(0,10/phi,0))
#b.rotate(angle=pi/4)
#b.pos=(0,2,0)

