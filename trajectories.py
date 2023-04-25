import numpy as np

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
    r_vector = np.asarray((x, y)).T

    return r_vector

def MRU(x0, y0, v0, angle, dt, t_max):
    
    # Convert angle to radians
    theta = np.radians(angle)

    # Create time array
    t = np.arange(0, t_max, dt)

    # Calculate x and y positions
    x = x0 + v0 * np.cos(theta) * t
    y = y0 + v0 * np.sin(theta) * t
    r_vector = np.asarray((x, y)).T

    return r_vector

def olita(x0, y0, omega1, alpha, omega2, dt, t_max):

    # Create time array
    t = np.arange(0, t_max, dt)

    # Calculate x and y positions
    x = x0 + 10 * np.sin(omega1 * t + alpha)
    y = y0 + 10 * np.sin(omega2 * t) 
    r_vector = np.asarray((x, y)).T

    return r_vector

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
    r_vector = np.asarray((x, y)).T

    return r_vector