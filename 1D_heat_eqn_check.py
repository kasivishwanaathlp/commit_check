#modules
import numpy as np
import matplotlib.pyplot as plt

#params
diffusivity=110
rod_length=50 #mm
time=4 #s
nodes=10

#params2
dx=rod_length/nodes
dt= (0.4 * dx ** 2) / 2
t_nodes=int(time/dt)

#init
u=np.zeros(nodes)+20
u[0]=100
u[-1]=0

#jigina
fig, axis=plt.subplots()
img=axis.imshow(u[np.newaxis,:],cmap='jet',aspect="auto",vmin=0,vmax=100)

#solver
for _ in range(t_nodes):
    w=u.copy()
    for i in range(1,nodes-1):
        u[i]=w[i]+(diffusivity*dt/dx**2*(w[i+1]-2*w[i]+w[i-1]))
    img.set_data(u[np.newaxis,:])
    plt.pause(0.01)
plt.show()