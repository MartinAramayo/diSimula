import yaml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

def load_yaml(filename):

    with open(filename, "r") as stream:
        try:
            file_dict = yaml.safe_load(stream)
            return file_dict
        except yaml.YAMLError as exc:
            print(exc)

# def norm(x):
#     return np.linalg.norm(x, axis=1)

def multi_norm(x):
    return np.linalg.norm(x, axis=2)

def norm1d(x):
    return np.linalg.norm(x, axis=0)

def d_dt(x):
    return np.gradient(x, axis=0)

def get_vel_acc_multi(R_vector, dt):
    
    # For some reason the derivative is not well scaled
    V_vector = []
    A_vector = []
    for n_object in range(len(R_vector)):
        r_vector = R_vector[n_object]
        v_vector = d_dt(r_vector) * 1 / dt # why? 
        a_vector = d_dt(v_vector) * 1 / dt # why?
        V_vector.append(v_vector)
        A_vector.append(a_vector)

    return V_vector, A_vector

def data_bound_box_from_ranges(ax, r_min, r_max, config):

    r_range = r_max - r_min

    # how much space to add to the range
    spacing = config['spacing']
    gap = r_range * spacing

    # get the new window range
    r_a, r_b = r_min - gap, r_max + gap
    x_a, y_a, x_b, y_b = *r_a, *r_b

    # Scale to data range
    ax.set_xlim(x_a, x_b)
    ax.set_ylim(y_a, y_b)

    # Make sure that the plot looks realistic
    def center(x, y): return (y + x) / 2
    def radius(x, y): return (y - x) / 2

    center_x = center(x_a, x_b)
    radius_x = radius(x_a, x_b)

    center_y = center(y_a, y_b)
    radius_y = radius(y_a, y_b)

    def get_interval(r0, dr): return [r0 - dr, r0 + dr]

    # Scale the shorter axis to the longest
    X_range, Y_range = r_range
    is_X_shorther = (X_range < Y_range)
    if is_X_shorther:
        ax.set_xlim(*get_interval(center_x, radius_y))
    else:
        ax.set_ylim(*get_interval(center_y, radius_x))
    ax.set_aspect('equal')

def data_bound_box(ax, r_vector, config):

    # set up plotbox to data, for one body
    r_max = r_vector.max(axis=0)
    r_min = r_vector.min(axis=0)

    data_bound_box_from_ranges(ax, r_min, r_max, config)

def data_bound_box_multi(ax, R_vector, config):

    # set up plotbox to data for multiple bodies
    r_min = R_vector.min(axis=0).min(axis=0)
    r_max = R_vector.max(axis=0).max(axis=0)

    data_bound_box_from_ranges(ax, r_min, r_max, config)

def colormapL(color):

    output = LinearSegmentedColormap.from_list(
        '', 2*[color]
    )
    return output

def set_plot(ax, r_vector, v_vector, a_vector, config):
    
    r_0, v_0, a_0 = r_vector[0], v_vector[0], a_vector[0]
    
    line, = ax.plot(*r_0,**config['line_plot_args'])
    point = ax.scatter(*r_0, **config['scatter_args'])

    # initial conditions
    def pick(x, e): return x if x > e else e
    v0 = pick(norm1d(v_0), config['norm_cutoff'])
    a0 = pick(norm1d(a_0), config['norm_cutoff'])

    # plot vectors
    plot_args = config['vector_plot_args']
    cm_vel = colormapL(config['vel_color'])
    cm_acc = colormapL(config['acc_color'])
    vel = ax.quiver(*r_0, *v_0, v0, cmap=cm_vel, **plot_args)
    acc = ax.quiver(*r_0, *a_0, a0, cmap=cm_acc, **plot_args)

    return line, point, vel, acc

def set_plot_multi(ax, R_vector, V_vector, A_vector, config):
    
    Line, Point, Vel, Acc = [], [], [], []

    for n_object in range(len(R_vector)):
        r_vector, v_vector, a_vector = (
            R_vector[n_object], 
            V_vector[n_object], 
            A_vector[n_object]
        )
        aux = set_plot(ax, r_vector, v_vector, a_vector, config)
        line, point, vel, acc = aux

        Line.append(line)
        Point.append(point)
        Vel.append(vel)
        Acc.append(acc)
    
    return Line, Point, Vel, Acc

def add_legend(fig, ax, config):

    cm_vel = config['vel_color']
    cm_acc = config['acc_color']
    vel_patch = Patch(color=cm_vel, label=r'$\vec{v}$')
    acc_patch = Patch(color=cm_acc, label=r'$\vec{a}$')
    ax.legend(handles=[vel_patch, acc_patch])

    ax.set_xlabel(config['x_label'])
    ax.set_ylabel(config['y_label'])

def skip_step_change(step1, step2):

    if step1 < step2:
        skip = int(step2 / step1)
        return skip if skip > 1 else 1
    else:
        error_str = (
            "The first step should be" 
            "smaller than the second"
        )
        raise ValueError(error_str)

def update_vector(quiv, position, norm, vector, index, norm_cutoff):

    quiv.set_offsets(position)
    if norm[index] > norm_cutoff:
        quiv.set_UVC(*vector[index], norm[index])
        quiv.set(alpha=0.9)
    else:
        quiv.set(alpha=0)

# Define the animation function
def animate_physics(
    i, line, point, vel, acc, r_vector, skip, norm_cutoff,
    v_vector, v_norm, a_vector, a_norm
    ):

    j_1, j = skip*(i-1), skip*i

    # Update the line object
    line.set_data(r_vector[:j, 0], r_vector[:j, 1])

    # Update object position
    pos = r_vector[j_1]
    point.set_offsets(pos)

    update_vector(vel, pos, v_norm, v_vector, j_1, norm_cutoff)
    update_vector(acc, pos, a_norm, a_vector, j_1, norm_cutoff)

    return line, vel, acc, 

def animate_physics_multi(
    i, Line, Point, Vel, Acc, R_vector, skip, norm_cutoff,
    V_vector, V_norm, A_vector, A_norm
    ):

    for n_object in range(len(R_vector)):

        r_vector, v_vector, a_vector = (
            R_vector[n_object], 
            V_vector[n_object], 
            A_vector[n_object]
        )

        v_norm, a_norm = (
            V_norm[n_object], 
            A_norm[n_object]
        )
        line, point, vel, acc = (
            Line[n_object], Point[n_object], Vel[n_object], Acc[n_object]
        )
    
        animate_physics(
            i, line, point, vel, acc, 
            r_vector, skip, norm_cutoff,
            v_vector, v_norm, a_vector, a_norm
        )

    return *Line, *Vel, *Acc, 

def ani_object(skip, fig, ani_func, frames, interval, config):
    
    # Create the animation
    aux = {"frames": frames, "interval": interval}
    ani = FuncAnimation(fig, ani_func, blit=True, **aux)

    return ani

def ani2video(ani, filename, config):

    aux = {"fps": config['frames']}
    if filename.endswith('.gif'):
        # to GIF
        ani.save(f'{filename}', writer='pillow', **aux)
    elif filename.endswith('.mp4'):

        # to MP4
        from matplotlib.animation import FFMpegWriter
        writer = FFMpegWriter(**aux)
        ani.save(f'{filename}', writer=writer)
        writer.finish()