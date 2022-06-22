"""Smart wheel data processing."""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from kineticstoolkit import TimeSeries
from pandas import DataFrame


def calcul_total_time(kinetics: TimeSeries) -> float:
    """
    Indicate the total time of the race.

    Parameters
    ----------
    kinetics : Data in TimeSeries

    Returns
    -------
    Return the total time of the race
    """
    total_time_race = round(kinetics.time[-1], 3)
    return total_time_race


def calculate_max_velocity(kinetics: TimeSeries) -> float:
    """
    Indicate the maximun velocity.

    Parameters
    ----------
    kinetics : Data in TimeSeries

    Returns
    -------
    Return the maximun velocity
    """
    max_velocity = max(kinetics.data['Velocity'])
    return max_velocity


def calculate_time_max_velocity(kinetics: TimeSeries,
                                max_velocity: float) -> float:
    """
    Indicate the time associated with the maximun velocity.

    Parameters
    ----------
    kinetics : Data in TimeSeries
    max_velocity : maximun velocity

    Returns
    -------
    Return te time of the max velocity
    """
    index = 0
    for elm in range(0, len(kinetics.data['Velocity'])):
        if (kinetics.data['Velocity'][elm] == max_velocity):
            index = elm
    time_max_velocity = kinetics.time[index]
    return time_max_velocity, index


def calculate_mean_velocity(kinetics: TimeSeries) -> float:
    """
    Calculate the mean velocity.

    Parameters
    ----------
    kinetics : Data in TimeSeries

    Returns
    -------
    Return the mean velocity
    """
    velocity = []

    for elm in range(0, len(kinetics.data['Velocity'])):
        velocity.append(kinetics.data['Velocity'][elm])

    sum_velocity = 0
    for elm in range(0, len(velocity)):
        sum_velocity += velocity[elm]

    mean_velocity = sum_velocity/len(velocity)
    return mean_velocity


def calculate_time_5_per_cent_mean_velocity(kinetics: TimeSeries,
                                            mean_velocity: float) -> float:
    """
    Indicate the time when the velocity not go below 5% of the mean velocity.

    Parameters
    ----------
    kinetics : Data in TimeSeries
    mean_velocity : mean velocity

    Returns
    -------
    Return the 5% time
    """
    index_mean = 0
    flag = 0
    for elm in range(0, len(kinetics.data['Velocity'])):
        if (kinetics.data['Velocity'][elm] <= (
                mean_velocity-0.05*mean_velocity) and flag == 0):
            index_mean = elm
        else:
            flag = 1

    time_mean_velocity = kinetics.time[index_mean]
    return time_mean_velocity, index_mean


def analyse_data(kinetics: str) -> TimeSeries:
    """
    Exploit the data from the smart wheel cart.

    Parameters
    ----------
    kinetics : Data in smart wheel sd format

    Returns
    -------
    Return the data in the form of TimeSeries
    """
    # calculate forces and moment
    gains = [-0.106, 0.106, 0.094, 0.022, -0.022, 0.0234999]

    offsets = [0., 10., 0., 0., 0., 0.]

    kinetics = ktk.pushrimkinetics.calculate_forces_and_moments(
        kinetics,
        gains=gains,
        offsets=offsets,
        transducer='smartwheel',
        reference_frame='hub')

    # Remove the offset
    kinetics = ktk.pushrimkinetics.remove_offsets(kinetics)

    # Velocity calculation
    kinetics = ktk.pushrimkinetics.calculate_velocity(kinetics)
    # Power calculation
    kinetics = ktk.pushrimkinetics.calculate_power(kinetics)

    kinetics = ktk.pushrimkinetics.remove_offsets(kinetics)

    return kinetics


def calculate_push_number(kinetics: TimeSeries) -> int:
    """
    Calculate the number of push of the race.

    Parameters
    ----------
    kinetics : Data in TimeSeries mode

    Returns
    -------
    Return the number of push
    """
    # Detect pushes
    kinetics.data['Ftot'] = np.sqrt(
        np.sum(kinetics.data['Forces'] ** 2, axis=1))

    kinetics = ktk.cycles.detect_cycles(
        kinetics, 'Ftot',
        event_names=['push', 'recovery'],
        thresholds=[5.0, 2.0],
        min_durations=[0.1, 0.1],
        min_peak_heights=[25.0, -np.Inf]
    )

    nbr_push = 0
    for i in range(0, len(kinetics.events)):
        if (np.isnan(kinetics.get_event_index("push", i)) == True):
            nbr_push += 0
        else:
            nbr_push += 1
    return nbr_push


def display_graph(kinetics: TimeSeries, time_max_velocity: float,
                  time_mean_velocity: float, mean_velocity: float,
                  max_velocity: float, index_max: int, index_mean: int):
    """
    Display graph.

    Parameters
    ----------
    kinetics : Data in TimeSeries mode
    time_max_velocity : time associated with the maximun velocity
    time_mean_velocity: time associated with the mean velocity
    max_velocity: maximun velocity
    mean_velocity: mean velocity
    index_max: index of the TimeSeries associated with the maximun velocity
    index_mean: index associted with the 5% mean velocity

    Returns
    -------
    None
    """
    fig = plt.figure(1, figsize=(50, 30))
    SMALL_SIZE = 32
    MEDIUM_SIZE = 40
    BIGGER_SIZE = 48

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    # Velocity graph
    plt.subplot(4, 1, 1)
    kinetics.plot('Velocity')

    plt.axvline(x=time_max_velocity, color='gray', linestyle='--')
    max_str = str(round(time_max_velocity, 2)) + " s"
    plt.annotate('Maximun velocity',
                 xy=(time_max_velocity,
                     kinetics.data["Velocity"][index_max]),
                 xytext=(time_max_velocity+2,
                         kinetics.data["Velocity"][index_max]-2),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="angle3,angleA=0,angleB=-90"))
    plt.annotate(max_str, xy=(time_max_velocity+2,
                              kinetics.data["Velocity"][index_max]-2.5))

    plt.axvline(x=time_mean_velocity, color='gray', linestyle='--')
    mean_str = str(round(time_mean_velocity, 2)) + " s"
    plt.annotate('5% of mean',
                 xy=(time_mean_velocity,
                     kinetics.data["Velocity"][index_mean]),
                 xytext=(time_mean_velocity+2,
                         kinetics.data["Velocity"][index_mean]-2),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="angle3,angleA=0,angleB=-90"))
    plt.annotate(mean_str, xy=(time_mean_velocity+2,
                               kinetics.data["Velocity"][index_mean]-2.5))

    plt.axhline(y=mean_velocity-0.05*mean_velocity,
                color='gray', linestyle='--')
    plt.axhline(y=max_velocity, color='gray', linestyle='--')

    # Power graph
    plt.subplot(4, 1, 2)
    kinetics.plot('Power')

    plt.subplot(4, 1, 3)
    kinetics.plot("Forces")
    plt.subplot(4, 1, 4)
    kinetics.plot("Moments")

    plt.show()

    return fig


def extract_data(kinetics: TimeSeries, n_cycles: int) -> DataFrame:
    """
    Extract some key spatiotemporal and kinetic parameters.

    Express those parameters as a pandas DataFrame

    Parameters
    ----------
    kinetics : Data in TimeSeries mode
    n_cyles : number of cycle to analyse

    Returns
    -------
    Return DataFrame
    """
    # Detect pushes
    kinetics.data['Ftot'] = np.sqrt(
        np.sum(kinetics.data['Forces'] ** 2, axis=1))

    kinetics = ktk.cycles.detect_cycles(
        kinetics, 'Ftot',
        event_names=['push', 'recovery'],
        thresholds=[5.0, 2.0],
        min_durations=[0.1, 0.1],
        min_peak_heights=[25.0, -np.Inf]
    )

    records = []  # Init a list that will contains the results of the analysis

    for i_cycle in range(n_cycles):
        # Get a TimeSeries that spans only the push i_push
        ts_push = kinetics.get_ts_between_events(
            'push', 'recovery', i_cycle, i_cycle)

        # Get a TimeSeries that spans the entire cycle i_push
        ts_cycle = kinetics.get_ts_between_events(
            'push', '_', i_cycle, i_cycle)

        # Get some spatiotemporal parameters
        push_time = ts_push.time[-1] - ts_push.time[0]
        cycle_time = ts_cycle.time[-1] - ts_cycle.time[0]
        recovery_time = cycle_time - push_time

        push_angle = ts_push.data['Angle'][-1] - ts_push.data['Angle'][0]

        # Get some kinetic parameters
        propulsion_moment_mean = np.mean(ts_push.data['Moments'][:, 2])
        propulsion_moment_max = np.max(ts_push.data['Moments'][:, 2])

        total_force_mean = np.mean(ts_push.data['Ftot'])
        total_force_max = np.max(ts_push.data['Ftot'])

        # Record this information in the records list
        records.append({
            'Push time (s)': push_time,
            'Recovery time (s)': recovery_time,
            'Cycle time (s)': cycle_time,
            'Push angle (deg)': np.rad2deg(push_angle),
            'Mean propulsion moment (Nm)': propulsion_moment_mean,
            'Max propulsion moment (Nm)': propulsion_moment_max,
            'Mean total force (N)': total_force_mean,
            'Max total force (N)': total_force_max,
        })

    # Create and show a DataFrame of this information
    df = pd.DataFrame.from_dict(records)

    # Copy the dataframe to the clipboard for pasting into Excel (facultative)
    df.to_clipboard()
    return df
