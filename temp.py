for j in range(IP_file["timesteps"]):
    w=u.copy()
    for i in range(1,IP_file["nodes"]-1):
        u[i]=w[i]+(IP_file["diffusivity"]*dt/dx**2*(w[i+1]-2*w[i]+w[i-1]))
    residuals=np.max(np.abs(w-u))
    print(residuals)
    ##TODO: ADD RESIDUALS PLOT HERE!!!

    img.set_data(u[np.newaxis,:])
    #plt.pause(1/fps)

    if residuals < IP_file["target_residuals"]:
        print(f"solution converged in {j} of {timesteps} iteration(s)")
        break

plt.show()


def solver_vectorized(IP_file):
    alpha = IP_file["diffusivity"] * dt / dx ** 2
    for j in range(IP_file["timesteps"]):
        w = u.copy()
        u[1:-1]=w[1:-1]+(alpha*w[2:]-2*w[1:-1]+w[-2])
        u[0]=IP_file["t1"]
        u[-1] = IP_file["t2"]
        residuals = np.max(np.abs(w - u))
        print(residuals)
        ##TODO: ADD RESIDUALS PLOT HERE!!!

        img.set_data(u[np.newaxis, :])
        # plt.pause(1/fps)

        if residuals < IP_file["target_residuals"]:
            print(f"solution converged in {j} of {timesteps} iteration(s)")
            break

    plt.show()
solver_vectorized(config)


if __name__=="__main__":
    main()
