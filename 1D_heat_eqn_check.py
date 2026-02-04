#modules
import sys

import numpy as np
import matplotlib.pyplot as plt

#params-INPUT
## TODO: add input via config file
from config import (config)

#CHECKS-input
## TODO: add global check version
if INPUT["diffusivity"] <= 0:
    print("diffusivity must be greater than 0")
    exit()
if INPUT["rod_length"] <= 0:
    print("rod length must be positive")
    exit()
if INPUT["nodes"] <= 0:
    print("nodes must be positive")
    exit()
if INPUT["time"] <= 0:
    print("time must be positive")
    exit()
if INPUT["target_CFL"] <= 0:
    print("target_CFL must be positive")
    exit()
if INPUT["fps"] <= 0:
    print("fps must be positive")
    exit()

#params-DERIVED
dx=rod_length/(nodes-1) #m
dt=(0.4 * dx ** 2)/diffusivity #s
timesteps=int(time/dt) #-

#CHECKS-derived--w/-SUGGESTIONS
if (((diffusivity*dt)/(dx**2)) > 0.5):
    print("advective CFL not met. Increase diffusivity or reduce rod length")
    exit()

#init
u=np.zeros(nodes)+ti
u[0]=t1
u[-1]=t2

# TODO: add "this is what you want to solve. yes?"

#viz
## TODO: add viz options, document in "README" or "docs"
## TODO: add toggles
## TODO: add anal soln comp
fig, axis=plt.subplots()
img=axis.imshow(u[np.newaxis,:],cmap='jet',aspect="auto",vmin=0,vmax=100)

#solver
## TODO: add implicit v explicit options
## TODO: vectorisation
for j in range(timesteps):
    w=u.copy()
    for i in range(1,nodes-1):
        u[i]=w[i]+(diffusivity*dt/dx**2*(w[i+1]-2*w[i]+w[i-1]))
    residuals=np.abs(w-u)
    residuals_plot=np.max(residuals)
    print(residuals_plot) #ADD RESIDUALS PLOT HERE!!!

    img.set_data(u[np.newaxis,:])
    #plt.pause(1/fps)

    if np.max(residuals) < target_residuals:
        print(f"solution converged in {j} of {timesteps} iteration(s)")
        break

plt.show()

## TODO: "stress-test"