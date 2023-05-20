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

from trajectories import *
from plotmod import *
from functools import partial
from docopt import docopt

if __name__ == '__main__':
    
    arguments = docopt(__doc__, version='diSimula 1.0')

    trajectory = arguments['<trajectory>']
    trajectory_func = locals()[trajectory]

    physics = load_yaml("params.yml")
    params = physics['physics'][trajectory]
    R_vector = trajectory_func(**params)
    dt = params['dt']

    # For some reason the derivative is not well scaled
    V_vector, A_vector = get_vel_acc_multi(R_vector, dt)

    # Set up the plot
    config = load_yaml("config.yml")
    plt.style.use(config['style_args']) # set plot style

    # plot them all
    fig, ax = plt.subplots(tight_layout=True)
    data_bound_box_multi(ax, R_vector, config)   
    Line, Point, Vel, Acc = set_plot_multi(
        ax, R_vector, V_vector, A_vector, config
    )

    add_legend(fig, ax, config)

    # run animation
    skip = skip_step_change(dt, 1 / config['frames'])
    V_norm, A_norm = multi_norm(V_vector), multi_norm(A_vector)
    animate = partial(
        animate_physics_multi, Line=Line, Point=Point, 
        Vel=Vel, Acc=Acc, R_vector=R_vector, 
        skip=skip, ERROR=config['ERROR'],
        V_vector=V_vector, V_norm=V_norm, 
        A_vector=A_vector, A_norm=A_norm
    )

    # save animation
    interval = 100 / config['frames'] # frame duration (ms)
    frames = len(R_vector[0,::skip]) # number of frames
    ani = ani_object(skip, fig, animate, frames, interval, config)
    ani2video(ani, arguments['<filename>'], config)
