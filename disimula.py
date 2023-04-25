#!/usr/bin/env python
"""Crea un video a partir de una trayectoria definida
como función de Python y las condiciones iniciales.

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
    
    arguments = docopt(__doc__, version='Gofito 0.1')

    trajectory = arguments['<trajectory>']
    trajectory_func = locals()[trajectory]

    physics = load_yaml("initial_cond.yml")
    initial_cond = physics['physics'][trajectory]
    r_vector = trajectory_func(**initial_cond)
    dt = initial_cond['dt']

    # For some reason the derivative is not well scaled
    v_vector = d_dt(r_vector) * 1 / dt # why? 
    a_vector = d_dt(v_vector) * 1 / dt # why?

    # Set up the plot
    params = load_yaml("params.yml")
    plt.style.use(params['style_args']) # set plot style
    fig, ax = plt.subplots(tight_layout=True)
    aux = set_plot(ax, r_vector, v_vector, a_vector, params)
    line, point, vel, acc = aux
    data_bound_box(ax, r_vector, params)
    add_legend(fig, ax, params)

    # run animation
    v_norm, a_norm = norm(v_vector), norm(a_vector)
    skip = skip_step_change(dt, 1 / params['frames'])
    animate = partial(
        animate_physics, line=line, point=point, 
        vel=vel, acc=acc, r_vector=r_vector, 
        skip=skip, ERROR=params['ERROR'],
        v_vector=v_vector, v_norm=v_norm, 
        a_vector=a_vector, a_norm=a_norm
    )

    # save animation
    interval = 100 / params['frames'] # frame duration (ms)
    frames = len(r_vector[::skip]) # number of frames
    ani = ani_object(skip, fig, animate, frames, interval, params)
    ani2video(ani, arguments['<filename>'], params)
