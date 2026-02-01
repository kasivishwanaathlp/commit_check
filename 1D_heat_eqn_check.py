#modules
import numpy as np
import matplotlib.pyplot as plt

#params
diffusivity=110 #m^2/s
rod_length=1 #m
time=4 #s
nodes=10 #-

#params2
dx=rod_length/(nodes-1) #m
dt=(0.40 * dx ** 2)/diffusivity #s
timesteps=int(time/dt) #-
fps=30 #fps
target_residuals=1e-3 #-

#ADD IF STATEMENT TO CHECK FOR EXPLICIT TIME STEPPING CONVERGENCE
#ADD SUGGESTION?

#init
u=np.zeros(nodes)+20
u[0]=100
u[-1]=0

#viz
fig, axis=plt.subplots()
img=axis.imshow(u[np.newaxis,:],cmap='jet',aspect="auto",vmin=0,vmax=100)

#solver
for j in range(timesteps):
    w=u.copy()
    for i in range(1,nodes-1):
        u[i]=w[i]+(diffusivity*dt/dx**2*(w[i+1]-2*w[i]+w[i-1]))
    residuals=np.abs(w-u)
    residuals_plot=np.max(residuals)
    print(residuals_plot) #ADD RESIDUALS PLOT HERE!!!

    img.set_data(u[np.newaxis,:])
    plt.pause(1/fps)

    if np.max(residuals) < target_residuals:
        print(f"solution converged in {j} of {timesteps} iteration(s)")
        break
plt.show()