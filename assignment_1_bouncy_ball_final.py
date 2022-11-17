#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Title: PHYS20161 1st assignment: Bouncy Ball

A program which takes user input values for the initial height, minimum height
of interest, and η (eta) to make a series of calculations regarding the motion
of a bouncy ball being dropped. The program calculates how many bounces the
ball makes over the minimum height of interest and how long it takes for the
ball to complete these bounces. There is an additional option to see the
trajectory visualised in the form of a height against time graph.

Oscar Fuentes Rebato  -  10827181  -  24/10/2022
"""

import numpy as np
import matplotlib.pyplot as plt

GRAVITY = 9.81

def time_for_bounce(height, gravity=GRAVITY):
    '''
    Parameters
    ----------
    Uses SUVAT equation s = u*t + 1/2*a*t**2 to calculate the time it takes for
    the ball to either go from height h to the ground, or from the ground to
    height h, using Earth's gravity.

    Parameters
    ----------
    height : float
        Height for which the time of motion of the ball is going to be
        calculated.
    gravity : float, optional
        Value for the acceleration due to gravity. Default is global variable
        GRAVITY = 9.81

    Returns
    -------
    time : float
        the time it takes for the ball to either go from height h to the
        ground, or from the ground to height h, using Earth's gravity.
    '''

    bounce_time = np.sqrt(2*height / gravity)
    return bounce_time

def height_input():
    '''
    Takes the input for the height the ball is dropped from and validates it
    is a number greater than 0.

    Returns
    -------
    Float
        The height the ball is dropped from.

    '''

    height = input('At what height (h) is the ball dropped from in metres, ' \
                    'where 0 < h: ')
    try:
        if float(height) < 0:
            print('h must be greater than 0')
            height = height_input()
    except ValueError:
        print('h must be a number')
        height = height_input()
    return float(height)


def height_min_input(height):
    '''
    Takes the input for the height the ball bouncing over and validates it
    is a number greater than 0 and less than the height it is dropped from.

    Returns
    -------
    Float
        The height the ball is bouncing over.

    '''

    height_min = input('What is the minimum height of interest (height_min) '\
                       'in metres, where 0 < height_min < h: ')
    try:
        if float(height_min) < 0 or float(height_min) > height:
            print('height_min must be greater than 0 and less than h')
            height_min = height_min_input(height)
    except ValueError:
        print('height_min must be a number')
        height_min = height_min_input(height)
    return float(height_min)

def eta_input():
    '''
    Takes the input for the bounce efficiency and validates it is a number
    greater than 0 and less than one.

    Returns
    -------
    Float
        The bounce efficiency of the ball.

    '''
    eta = input('What is the bounce efficiency (eta), where 0 < eta < 1: ')

    try:
        if float(eta) <= 0 or float(eta) >= 1:
            print('eta must be greater than 0 and less than one')
            eta = eta_input()
    except ValueError:
        print('eta must be a number')
        eta = eta_input()
    return float(eta)


def input_values():
    '''
    Takes the input for height the ball is dropped from (h), minimum height of
    interest and bounce efficiency. Checks that these are all valid inputs.

    Returns
    -------
    Tuple of height, height_min and eta
    '''
    height = height_input()
    height_min, eta = height_min_input(height), eta_input()
    return height, height_min, eta


def bounces(height, height_min, eta):
    '''
    Calculates the number of times the bouncy ball bounces over height_min when
    dropped from a height h, as well as the total time it takes for all of
    these bounces.

    Parameters
    ----------
    height : Float
        The height from which a bouncy ball is dropped (h)
    height_min : Float
        The height that the bouncy ball will bounce over n times.
    eta : Float
        Bounce efficiency, where after dropping from a height, the new height
        after the bounce is eta * height.  0 < eta < 1

    Returns
    -------
    Number of times the ball will bounce over height_min and the time it takes for
    these bounces.
    '''

    count = -1
    time = 0

    while height > height_min:
        time += time_for_bounce(height)
        count += 1
        height *= eta
        time += time_for_bounce(height)

    time -= time_for_bounce(height)
    return count, time

# These next three functions: trajectory_points_down(), trajectory_points_up()
# and trajectory_plot() are only called if the user chooses to plot the trajectory

def trajectory_points_down(start, end, height, gravity = GRAVITY):
    '''
    Returns x- and y-values for half a parabola starting at y = height and
    ending at y = 0
    Parameters
    ----------
    start : Float
        Starting x-value
    end : Float
        Ending x-value
    height : Float
        Maximum y-value.
    gravity : Float, optional
        Acceleration due to gravity for the bouncy ball. The default is GRAVITY.

    Returns
    -------
    x_values : Array
        100 evenly spaced points between start and end.
    y_values : Array
        100 points describing the parabolic shape of the trajectory of the ball.

    '''
    x_values = np.linspace(start, end, 100)
    y_values = -((gravity/2)*(x_values-(end-time_for_bounce(height)))**2)+height
    return x_values, y_values

def trajectory_points_up(start, end, height, gravity=GRAVITY):
    '''
    Returns x- and y-values for half a parabola starting at y = 0 and ending
    at y = height
    Parameters
    ----------
    start : Float
        Starting x-value
    end : Float
        Ending x-value
    height : Float
        Maximum y-value.
    gravity : Float, optional
        Acceleration due to gravity for the bouncy ball. The default is GRAVITY.

    Returns
    -------
    x_values : Array
        100 evenly spaced points between start and end.
    y_values : Array
        100 points describing the parabolic shape of the trajectory of the ball.

    '''
    x_values = np.linspace(start, end, 100)
    y_values = -((gravity/2)*(x_values-end)**2)+height
    return x_values, y_values

def trajectory_plot(height, height_min, eta):
    '''
    Plots the trajectory of the bouncy ball, which starts at height metres,
    has a bounce efficiency of eta and bounces over height_min
    Includes the final bounce which doesn't make it over height_min'

    Parameters
    ----------
    height : Float
        Height the ball is dropped from.
    height_min : Float
        Minimum height the ball bounces over to be counted.
    eta : Float
        Bounce efficiency of the ball.

    Returns
    -------
    None.

    '''
    bounces_x = []
    bounces_y = []
    count = 0
    time = 0
    while height > height_min:
        time += time_for_bounce(height)
        x_points, y_points = trajectory_points_down(time - time_for_bounce(height),
                                                    time, height)
        bounces_x = np.append(bounces_x, [x_points])
        bounces_y = np.append(bounces_y, [y_points])
        count += 1
        height *= eta
        time += time_for_bounce(height)
        x_points, y_points = trajectory_points_up(time - time_for_bounce(height),
                                                  time, height)
        bounces_x = np.append(bounces_x, [x_points])
        bounces_y = np.append(bounces_y, [y_points])
    time += time_for_bounce(height)
    x_points, y_points = trajectory_points_down(time - time_for_bounce(height),
                                                time, height)
    bounces_x = np.append(bounces_x, [x_points])
    bounces_y = np.append(bounces_y, [y_points])
    time_values = np.stack(bounces_x)
    height_values = np.stack(bounces_y)
    height_min_line = [[0, time], [height_min, height_min]]
    plt.plot(time_values, height_values, 'k-', label = 'Trajectory')
    plt.xlabel('Time (s)')
    plt.ylabel('Height (m)')
    plt.title('Trajectory of the bouncy ball')
    plt.plot(height_min_line[0], height_min_line[1], 'k--', label = 'height_min')
    plt.legend()
    plt.show()
    print('Trajectory plotted successfully')

def bouncy_ball_main():
    '''
    Prints the results of a bouncy ball dropped from height (h), over a height of height_min
    with bounce efficiency eta. There is an additional option to plot the trajectory.

    Parameters
    ----------
    height : Float, input
        The height from which a bouncy ball is dropped (h)
    height_min : Float, input
        The height that the bouncy ball will bounce over n times.
    eta : Float, input
        Bounce efficiency, where after dropping from height h, the new height
        is eta*h. 0 < eta < 1
    plot : Bool, input
        Whether or not the trajectory of the ball should be plotted.

    Returns
    -------
    None.
    '''

    height, height_min, eta = input_values()
    results = bounces(height, height_min, eta)
    print('\nWith an efficiency of', str(eta) + ', a bouncy ball dropped from',
          str(height) + 'm will bounce',results[0],'times above', str(height_min) +'m, ' \
              'and this will take', str(round(results[1], 2)) + 's')
    plot_input = input('Would you like this plotted? (Y/N): ')
    if plot_input in ('Y', 'y'):
        trajectory_plot(height, height_min, eta)
    else:
        print('Trajectory not plotted')

bouncy_ball_main()
