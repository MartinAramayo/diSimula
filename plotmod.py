import yaml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

def norm(x):
    return np.linalg.norm(x, axis=1)

def norm1d(x):
    return np.linalg.norm(x, axis=0)

def d_dt(x):
    return np.gradient(x, axis=0)

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

def load_yaml(filename):

    with open(filename, "r") as stream:
        try:
            params = yaml.safe_load(stream)
            return params
        except yaml.YAMLError as exc:
            print(exc)

def colormapL(color):

    output = LinearSegmentedColormap.from_list(
        '', 2*[color]
    )
    return output

def set_plot(ax, r_vector, v_vector, a_vector, params):
    
    r_0, v_0, a_0 = r_vector[0], v_vector[0], a_vector[0]
    
    line, = ax.plot(*r_0,**params['line_plot_args'])
    point = ax.scatter(*r_0, **params['scatter_args'])

    # initial conditions
    pick = (lambda x, e: x if x > e else e)
    v0 = pick(norm1d(v_0), params['ERROR'])
    a0 = pick(norm1d(a_0), params['ERROR'])

    # plot vectors
    plot_args = params['vector_plot_args']
    cm_vel = colormapL(params['vel_color'])
    cm_acc = colormapL(params['acc_color'])
    vel = ax.quiver(*r_0, *v_0, v0, cmap=cm_vel, **plot_args)
    acc = ax.quiver(*r_0, *a_0, a0, cmap=cm_acc, **plot_args)

    return line, point, vel, acc

def data_bound_box(ax, r_vector, params):

    # set up plotbox to data
    r_max = r_vector.max(axis=0)
    r_min = r_vector.min(axis=0)
    r_range = r_max - r_min

    # how much space to add to the range
    spacing = params['spacing']
    gap = r_range * spacing

    # get the new window range
    r_a, r_b = r_min - gap, r_max + gap
    x_a, y_a, x_b, y_b = *r_a, *r_b

    # Scale to data range
    ax.set_xlim(x_a, x_b)
    ax.set_ylim(y_a, y_b)

    # Make sure that the plot looks realistic
    center = (lambda x, y: (y + x) / 2)
    radius = (lambda x, y: (y - x) / 2)

    center_x = center(x_a, x_b)
    radius_x = radius(x_a, x_b)

    center_y = center(y_a, y_b)
    radius_y = radius(y_a, y_b)

    get_interval = (lambda r0, dr: [r0 - dr, r0 + dr])

    # Scale the shorter axis to the longest
    X_range, Y_range = r_range
    is_X_shorther = (X_range < Y_range)
    if is_X_shorther:
        ax.set_xlim(*get_interval(center_x, radius_y))
    else:
        ax.set_ylim(*get_interval(center_y, radius_x))
    ax.set_aspect('equal')

def add_legend(fig, ax, params):

    cm_vel = params['vel_color']
    cm_acc = params['acc_color']
    vel_patch = Patch(color=cm_vel, label=r'$\vec{v}$')
    acc_patch = Patch(color=cm_acc, label=r'$\vec{a}$')
    ax.legend(handles=[vel_patch, acc_patch])

    ax.set_xlabel('Coordenada $x$')
    ax.set_ylabel('Coordenada $y$')

def update_vector(quiv, position, norm, vector, index, ERROR):

    quiv.set_offsets(position)
    if norm[index] > ERROR:
        quiv.set_UVC(*vector[index], norm[index])
        quiv.set(alpha=0.9)
    else:
        quiv.set(alpha=0)

# Define the animation function
def animate_physics(
    i, line, point, vel, acc, r_vector, skip, ERROR,
    v_vector, v_norm, a_vector, a_norm
    ):

    j_1, j = skip*(i-1), skip*i

    # Update the line object
    line.set_data(r_vector[:j, 0], r_vector[:j, 1])

    # Update object position
    pos = r_vector[j_1]
    point.set_offsets(pos)

    update_vector(vel, pos, v_norm, v_vector, j_1, ERROR)
    update_vector(acc, pos, a_norm, a_vector, j_1, ERROR)

    return line, vel, acc, 

def ani_object(skip, fig, ani_func, frames, interval, params):
    
    # Create the animation
    aux = {"frames": frames, "interval": interval}
    ani = FuncAnimation(fig, ani_func, blit=True, **aux)

    return ani

def ani2video(ani, filename, params):

    aux = {"fps": params['frames']}
    if filename.endswith('.gif'):
        # to GIF
        ani.save(f'{filename}', writer='pillow', **aux)
    elif filename.endswith('.mp4'):

        # to MP4
        from matplotlib.animation import FFMpegWriter
        writer = FFMpegWriter(**aux)
        ani.save(f'{filename}', writer=writer)
        writer.finish()