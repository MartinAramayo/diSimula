#!/usr/bin/env python
"""Crea un video a partir de una/s trayectoria/s definida/s
como función/es de Python. Incorpora traza y vectores velocidad
y aceleración.

Usage:
  disimula.py <trajectory> -o <filename>
  disimula.py (-h | --help)
  disimula.py --version

Options:
  -h --help     Muestra este mensaje.
  --version     Muetra la versoin.
  -o            Archivo de salida (.gif o .mp4)
"""

import trajectories as traj
import plotmod as pltmod
import matplotlib.pyplot as plt
from functools import partial
from docopt import docopt

if __name__ == '__main__':
    
    arguments = docopt(__doc__, version='diSimula 1.0')

    
    # Dynamically access the function from the module
    trajectory = arguments['<trajectory>']
    trajectory_func = getattr(traj, trajectory, None)

    if trajectory_func is None:
        print(f"Function {trajectory} not found in trajectories module.")
        pass

    physics = pltmod.load_yaml("params.yml")
    params = physics['physics'][trajectory]
    R_vector = trajectory_func(**params)
    dt = params['dt']

    # For some reason the derivative is not well scaled
    V_vector, A_vector = pltmod.get_vel_acc_multi(R_vector, dt)

    # Set up the plot
    config = pltmod.load_yaml("config.yml")
    plt.style.use(config['style_args']) # set plot style

    # plot them all
    fig, ax = plt.subplots(tight_layout=True)
    pltmod.data_bound_box_multi(ax, R_vector, config)   
    Line, Point, Vel, Acc = pltmod.set_plot_multi(
        ax, R_vector, V_vector, A_vector, config
    )

    pltmod.add_legend(fig, ax, config)

    # run animation
    skip = pltmod.skip_step_change(dt, 1 / config['frames'])
    V_norm, A_norm = pltmod.multi_norm(V_vector), pltmod.multi_norm(A_vector)
    animate = partial(
        pltmod.animate_physics_multi, Line=Line, Point=Point, 
        Vel=Vel, Acc=Acc, R_vector=R_vector, 
        skip=skip, norm_cutoff=config['norm_cutoff'],
        V_vector=V_vector, V_norm=V_norm, 
        A_vector=A_vector, A_norm=A_norm
    )

    # save animation
    interval = 100 / config['frames'] # frame duration (ms)
    frames = len(R_vector[0,::skip]) # number of frames
    ani = pltmod.ani_object(skip, fig, animate, frames, interval, config)
    pltmod.ani2video(ani, arguments['<filename>'], config)
