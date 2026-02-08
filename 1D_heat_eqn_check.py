#modules
import sys
import numpy as np
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.WARNING, format="WARNING: %(message)s")

#params-INPUT
from config import (config)

#CHECKS-input
INPUT_CHECKS={
    "diffusivity":(lambda i:isinstance(i,(int,float)) and i>0, "must be >0"),
    "rod_length":(lambda i:isinstance(i,(int,float)) and i>0, "must be >0"),
    "nodes":(lambda i:isinstance(i,int) and i>=2, "must be and integer >=2"),
    "time":(lambda i:isinstance(i,(int,float)) and i>0, "must be >0"),
    "t1":(lambda i:isinstance(i,(int,float)), "must be numeric"),
    "t2":(lambda i:isinstance(i,(int,float)), "must be numeric"),
    "ti":(lambda i:isinstance(i,(int,float)), "must be numeric"),
    "target_CFL":(lambda i:isinstance(i,(int,float)) and 0<i<=0.5, "must be 0< and <=0.5"),
    "target_residuals":(lambda i:isinstance(i,float) and 0<i<1, "must be 0< <1"),
    "fps":(lambda i:isinstance(i,int) and i>0, "must be an integer >0"),
}
def input_checks(IP_file):
    errors=[]
    for key in IP_file:
        if key not in INPUT_CHECKS:
            errors.append(f"Unknown config key: {key}")
    for key, (rule, msg) in INPUT_CHECKS.items():
        if key not in IP_file:
            errors.append(f"{key} input is missing")
            continue
        value=IP_file[key]
        if not rule(value):
            errors.append(f"{key} has invalid value, {msg}")
    if IP_file["nodes"]<10:
        logging.warning("Number of nodes less than 10")
    if IP_file["nodes"]>1e6:
        logging.warning("Number of nodes greater than 1e6")
    if IP_file["target_residuals"]>1e-2:
        logging.warning("Target residuals > 1e-2 - convergence might be loose")
    if IP_file["target_residuals"]<1e-9:
        logging.warning("Target residuals < 1e-9 - may cause excessive runtime")
    if errors:
        raise ValueError("\nInput validation failed:\n" + "\n".join(errors))
## TODO: add "if __name__ == "__main__":" part for imports
input_checks(config)

#params-DERIVED
def params_DERIVED(IP_file):
    dx=(IP_file["rod_length"])/((IP_file["nodes"])-1) #m
    dt=(IP_file["target_CFL"] * dx ** 2)/(IP_file["diffusivity"]) #s
    timesteps=int((IP_file['time'])/dt) #-
    calc_CFL=(IP_file["diffusivity"]*dt)/(dx**2)
    return {"dx":dx, "dt":dt, "timesteps":timesteps, "calc_CFL":calc_CFL}
derived_params=params_DERIVED(config)

def derived_checks(IP_dict):
    errors=[]
    if IP_dict["dt"]<=0:
        errors.append("Computed dt is non-positive")
    if IP_dict["timesteps"]<=1:
        errors.append("Simulation time smaller than unit timestep")
    if IP_dict["calc_CFL"]>0.5:
        errors.append(f"Calculated CFL is > 0.5; Calculated CFL = {calc_CFL}")
    if IP_dict["timesteps"]>1e9:
        errors.append("Calculated number of timesteps larger than 1e9")
    if IP_dict["timesteps"]>1e7:
        logging.warning("Calculated number of timesteps greater than 1e7 - simulation might be slow")
    if IP_dict["timesteps"]<1e2:
        logging.warning("Calculated number of timesteps smaller than 1e2 - solution may not reach steady behaviour")
    if errors:
        raise ValueError("\nInput validation failed:\n" + "\n".join(errors))
derived_checks(derived_params)

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

if __name__=="__main__":
    main()

## TODO: "stress-test"