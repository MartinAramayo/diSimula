<img src="logo.png" align="right" />

# DiSIMULA

Simulador de trayectorias con vector velocidad y aceleracion a partir de las 
coordenadas en funcion del tiempo $x(t)$ e $y(t)$.

![](output/olita.gif)

## Uso

Dentro del archivo `trajectories.py` crear una función que cree los $x(t)$ e $y(t)$ 
de la trayectoria que se quiere simular. Se pueden poner curvas paramétricas y 
ecuaciones horarias. Es posible pasar parámetros físicos adicionales. Los 
parámetros físicos y las condiciones iniciales se insertan en `initial_cond.yml`.

Hay algunos ejemplos de trayectorias cargados, sus animaciones están en `output` dentro del repo. Los ejemplos subidos en el repo se pueden crear de la siguiente manera:

~~~
Para agregar trayectorias es necesario agregar todos los parámetros físicos, el 
paso temporal $dt$ y el tiempo que dura la simulación $t_{max}$.

Usage:
  disimula.py <trajectory> -o <filename>
  disimula.py (-h | --help)
  disimula.py --version

Options:
  -h --help     Muestra este mensaje.
  --version     Muetra la versoin.
  -o            Archivo de salida (.gif o .mp4)
~~~

## Agregar trayectorias

Para agregar trayectorias es necesario agregar todos los parámetros físicos, el 
paso temporal $dt$ y el tiempo que dura la simulación $t_{max}$.

## Ejemplos

Para agregar una trayectoria creamos una función dentro de `trajectories.py`, con 
el vector de tiempo (asegurate de crearlo con `np.arange` o algo que cree valores 
equiespaciados). Con ese vector tiempo creas tus $x(t)$ e $y(t)$ para guardarlos
en el vector r_vector como indica el ejemplo que sigue:

~~~ python
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
~~~

Podes usar funciones de [numpy](https://numpy.org/) como `cos`, `sin`, `tan`, etc.

Podés agregar los parámetros que quieras para definir todas las cantidades, por 
ejemplo, podés agregar un tiempo inicial si no querés arrancar de t=0. 
Todos los parámetros se ajustan dentro del `initial_cond.yml` que, si tenés 
solo MRU se ve así:

~~~ yaml
physics: 
  MRU: 
    x0: 0.0
    y0: 0.0
    v0: 15.0
    angle: 45.0
    dt: 0.001
    t_max: 4
~~~

Acá podés cambiar la velocidad, el ángulo, el t_max y todos los parámetros que 
quieres agregar. Si querés ponerle un factor cuadrado simplemente lo agregas 
con el mismo estilo. Por ejemplo, podemos agregar $t_0=-10$ de la siguiente
manera. Primero el `initial_cond.yml` queda:

~~~ yaml
physics: 
  MRU: 
    x0: 0.0
    y0: 0.0
    v0: 15.0
    angle: 45.0
    dt: 0.001
    t_max: 4
    t_0: -10
~~~

Ahora en `trajectories.py` tenés que agregar `t_0`:

~~~ python
def MRU(x0, y0, v0, angle, dt, t_max, t_0):
    
    # Convert angle to radians
    theta = np.radians(angle)

    # Create time array
    t = np.arange(t_0, t_max, dt)

    # Calculate x and y positions
    x = x0 + v0 * np.cos(theta) * t
    y = y0 + v0 * np.sin(theta) * t
    r_vector = np.asarray((x, y)).T

    return r_vector
~~~

Para guardar la animación en el directorio `output` como un MP4 solo hace falta 
correr:

~~~ bash
python disimula.py MRU -o output/MRU.mp4
~~~


# Requisitos

Hace falta tener instalado, `python`, `matplotlib`, `numpy`, `docopt` y
`pyyaml`. En el repo hay un archivo `req.txt` que contiene todos los módulos necesarios. Para guardar `mp4` es necesario tener instalado `ffmpeg`. Para estar
seguro podés instalar con el `requirements file` `req.txt` para tener la misma 
Versión de los módulos que use.

## Instalar anaconda (Incluye python numpy y cosas para data science)

Instalar anaconda
[https://www.anaconda.com/download/](https://www.anaconda.com/download/)
