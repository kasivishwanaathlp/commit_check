#modules
import sys
import numpy as np
import matplotlib.pyplot as plt

#params-INPUT
from config import (config)

#CHECKS-input
INPUT_CHECKS={
    "diffusivity":(lambda i:isinstance(i,(int,float)) and i>0, "must be >0"),
    "rod_length":(lambda i:isinstance(i,(int,float)) and i>0, "must be >0"),
    "nodes":(lambda i:isinstance(i,int) and i>=2, "must be >=2"),
    "time":(lambda i:isinstance(i,(int,float)) and i>0, "must be >0"),
    "target_CFL":(lambda i:isinstance(i(int,float)) and 0<i<=0.5, "must be 0< and <=0.5"),
    "target_residuals":(lambda i:isinstance(i,float) and 0<i<1, "must be 0< <1"),
    "fps":(lambda i:isinstance(i,int) and i>0, "must be >0"),
}
def input_checks(config):
    errors=[]
    for key in config:
        if key not in INPUT_CHECKS:
            errors.append(f"Unknown config key: {key}")
    for key, (rule, msg) in INPUT_CHECKS.items():
        if key not in config:
            errors.append(f"{key} input is missing")
            continue
        value=config[key]
        if not rule(value):
            errors.append(f"{key} has invalid value, {msg}")
    if errors:
        raise ValueError("\nInput validation failed:\n" + "\n".join(errors))
## TODO: add "if __name__ == "__main__":" part for imports
input_checks(config)

#params-DERIVED
dx=(config["rod_length"])/((config["nodes"])-1) #m
dt=(config["target_CFL"] * dx ** 2)/(config["diffusivity"]) #s
timesteps=int((config['time'])/dt) #-

#CHECKS-derived--w/-SUGGESTIONS
## TODO: add "DERIVED_CHECKS" as funciton
#init
u=np.zeros(config["nodes"])+config["ti"]
u[0]=config["t1"]
u[-1]=config["t2"]

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
    for i in range(1,config["nodes"]-1):
        u[i]=w[i]+(config["diffusivity"]*dt/dx**2*(w[i+1]-2*w[i]+w[i-1]))
    residuals=np.abs(w-u)
    residuals_plot=np.max(residuals)
    print(residuals_plot)
    ##TODO: ADD RESIDUALS PLOT HERE!!!

    img.set_data(u[np.newaxis,:])
    #plt.pause(1/fps)

    if np.max(residuals) < config["target_residuals"]:
        print(f"solution converged in {j} of {timesteps} iteration(s)")
        break

plt.show()

## TODO: "stress-test"