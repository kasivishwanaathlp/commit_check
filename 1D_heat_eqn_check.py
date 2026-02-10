#modules
import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.WARNING, format="WARNING: %(message)s")

#params-INPUT
from config import (config)
from dataclasses import dataclass

#CHECKS-input
## TODO: second rule table for warnings
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
@dataclass(frozen=True)
class Params:
    diffusivity: float
    rod_length: float
    nodes: int
    time: float
    t1: float
    t2: float
    ti: float
    target_CFL: float
    target_residuals: float
    fps: int

    dx: float
    dt: float
    timesteps: int
    calc_CFL: float

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

#params-DERIVED
def params_DERIVED(IP_file):
    dx=(IP_file["rod_length"])/((IP_file["nodes"])-1) #m
    dt=(IP_file["target_CFL"] * dx ** 2)/(IP_file["diffusivity"]) #s
    timesteps=int((IP_file['time'])/dt) #-
    calc_CFL=(IP_file["diffusivity"]*dt)/(dx**2)
    return {"dx":dx, "dt":dt, "timesteps":timesteps, "calc_CFL":calc_CFL}

#CHECKS-derived--w/-SUGGESTIONS
## TODO: rule table again? - 1. errors; 2. warnings
def derived_checks(IP_dict):
    errors=[]
    if IP_dict["dt"]<=0:
        errors.append("Computed dt is non-positive")
    if IP_dict["timesteps"]<=1:
        errors.append("Simulation time smaller than unit timestep")
    if IP_dict["calc_CFL"]>0.5:
        errors.append(f"Calculated CFL is > 0.5; Calculated CFL = {IP_dict['calc_CFL']}")
    if IP_dict["timesteps"]>1e9:
        errors.append("Calculated number of timesteps larger than 1e9")
    if IP_dict["timesteps"]>1e7:
        logging.warning("Calculated number of timesteps greater than 1e7 - simulation might be slow")
    if IP_dict["timesteps"]<1e2:
        logging.warning("Calculated number of timesteps smaller than 1e2 - solution may not reach steady behaviour")
    if errors:
        raise ValueError("\nInput validation failed:\n" + "\n".join(errors))

def assemble_params(config):
    input_checks(config)
    derived_params=params_DERIVED(config)
    derived_checks(derived_params)
    return Params(**config, **derived_params)
params = assemble_params(config)

#init
def init(params):
    u=np.full(params.nodes, params.ti, dtype=float)
    u[0]=params.t1
    u[-1]=params.t2
    return u
u=init(params)

#viz
## TODO: document in "README" or "docs"
## TODO: add cmap options
## TODO: add toggles
## TODO: add anal soln comp
fig, axis=plt.subplots()
img=axis.imshow(u[np.newaxis,:],cmap='jet',aspect="auto",vmin=0,vmax=100)

#solver
## TODO: add implicit v explicit options
## TODO: vectorisation
def solver_loop(params: Params, u):
    for j in range(params.timesteps):
        w = u.copy()
        for i in range(1, params.nodes - 1):
            u[i] = w[i] + (params.calc_CFL * (w[i + 1] - 2 * w[i] + w[i - 1]))
        residuals = np.max(np.abs(w - u))
        print(residuals)
        ##TODO: ADD RESIDUALS PLOT HERE!!!

        img.set_data(u[np.newaxis, :])
        #plt.pause(1/params.fps)

        if residuals < params.target_residuals:
            print(f"solution converged in {j} of {params.timesteps} iteration(s)")
            break
    plt.show()
solver_loop(params, u)

#wiki
## TODO: look for top 3 tangible differences between loop and vectorized and how to documnet them

## TODO: "stress-test"