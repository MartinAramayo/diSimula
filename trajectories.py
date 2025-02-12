import numpy as np

def pack_object(r_vector):
    return np.asarray((r_vector,))

def pack_object_multi(R_vector):
    return np.asarray(tuple(R_vector,))

def parabolic_trajectory(x0, y0, v0, angle, g, dt):
    
    # Convert angle to radians
    theta = np.radians(angle)
    
    # Calculate time of flight
    t_max = 2 * v0 * np.sin(theta) / g

    # Create time array
    t = np.arange(0, t_max, dt)

    # Calculate x and y positions
    x = x0 + v0 * np.cos(theta) * t
    y = y0 + v0 * np.sin(theta) * t - 0.5 * g * t**2

    # packaging the array for the plotter
    r_vector = np.asarray((x, y)).T

    return pack_object(r_vector)

def parabolic_trajectory_multi(x0, y0, v0, angle, g, dt):
    
    R_vector = []

    
    # Calculate time of flight
    t_max = 2 * v0 * np.sin(45) / g

    # Create time array
    t = np.arange(0, 2*t_max, dt)
    
    for n_object in range(72):
    
        # Convert angle to radians
        theta = np.radians(angle + 5 * n_object)

        # Calculate x and y positions
        x = x0 + v0 * np.cos(theta) * t
        y = y0 + v0 * np.sin(theta) * t - 0.5 * g * t**2

        # packaging the array for the plotter
        r_vector = np.asarray((x, y)).T

        R_vector.append(r_vector)

    return pack_object_multi(R_vector)

def MRU(x0, y0, v0, angle, dt, t_max):
    
    # Convert angle to radians
    theta = np.radians(angle)

    # Create time array
    t = np.arange(0, t_max, dt)

    # Calculate x and y positions
    x = x0 + v0 * np.cos(theta) * t
    y = y0 + v0 * np.sin(theta) * t

    # packaging the array for the plotter
    r_vector = np.asarray((x, y)).T

    return pack_object(r_vector)

def MCU_multi(x0, y0, r, omega, dt, t_max):
    
    R_vector = []

    # Create time array
    t = np.arange(0, t_max, dt)

    for n_object in range(5):

        R = r + n_object * 1

        # Calculate x and y positions
        x = x0 + R * np.cos(omega * t)
        y = y0 + R * np.sin(omega * t) 

        # packaging the array for the plotter
        r_vector = np.asarray((x, y)).T

        R_vector.append(r_vector)

    return pack_object_multi(R_vector)

def olita(x0, y0, omega1, alpha, omega2, dt, t_max):

    # Create time array
    t = np.arange(0, t_max, dt)

    # Calculate x and y positions
    x = x0 + 10 * np.sin(omega1 * t + alpha)
    y = y0 + 10 * np.sin(omega2 * t) 

    # packaging the array for the plotter
    r_vector = np.asarray((x, y)).T

    return pack_object(r_vector)

def kokoro(x0, y0, dt, t_max):

    # Create time array
    t = np.arange(0, t_max, dt)

    # Calculate x and y positions
    x = x0 + 16 * np.sin(t)**3
    y = (
        y0 
        + 13 * np.cos(t) 
        - 5 * np.cos(2*t) 
        - 2 * np.cos(3*t) 
        - np.cos(4*t)
    )

    # packaging the array for the plotter
    r_vector = np.asarray((x, y)).T

    return pack_object(r_vector)

def kokoro_multi(x0, y0, r, dt, t_max):

    R_vector = []

    # Create time array
    t = np.arange(0, t_max, dt)
    
    for n_object in range(5):

        R = r + n_object * 1

        # Calculate x and y positions
        x = R * (x0 + 16 * np.sin(t)**3)
        y = R * (
            y0 
            + 13 * np.cos(t) 
            - 5 * np.cos(2*t) 
            - 2 * np.cos(3*t) 
            - np.cos(4*t)
        )

        # packaging the array for the plotter
        r_vector = np.asarray((x, y)).T

        R_vector.append(r_vector)

    return pack_object_multi(R_vector)

def parabolic_trajectory_multi_kokoro(x0, y0, v0, angle, g, dt):
    
    R_vector = []

    
    # Calculate time of flight
    t_max = 2 * v0 * np.sin(45) / g

    # Create time array
    t = np.arange(0, 2*t_max, dt)

    def kokoro_vector_scaler(t):
        vx = (x0 + 16 * np.sin(t)**3)/12
        vy = (
            y0 
            + 13 * np.cos(t) 
            - 5 * np.cos(2*t) 
            - 2 * np.cos(3*t) 
            - np.cos(4*t)
        )/12
        return vx, vy
    
    for n_object in range(72):
    
        # Convert angle to radians
        theta = np.radians(angle + 5 * n_object)

        proj_x, proj_y = kokoro_vector_scaler(theta)

        # Calculate x and y positions
        x = x0 + v0 * proj_x * t
        y = y0 + v0 * proj_y * t - 0.5 * g * t**2

        # packaging the array for the plotter
        r_vector = np.asarray((x, y)).T

        R_vector.append(r_vector)

    return pack_object_multi(R_vector)