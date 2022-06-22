"""Smart wheel interface with Streamlit."""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

import streamlit as st
from io import BytesIO

import matplotlib.pyplot as plt
import kineticstoolkit.lab as ktk
import analyse as a
from kineticstoolkit import TimeSeries
from pandas import DataFrame


def convert_df(df) -> DataFrame:
    """Convert dataframes to csv."""
    return df.to_csv().encode('utf-8')


def display_analyse(kinetics: TimeSeries, radius: float, max_velocity: float,
                    mean_velocity: float, nbr_push: int,
                    time_max_velocity: float, time_5_per_cent: float,
                    index_max: int, index_mean: int, nbr_analyse: int):
    """
    Display Analyse and widgets.

    Parameters
    ----------
    kinetics : Data in TimeSeries mode
    radius: radius in meter of the wheel
    max_velocity: maximun velocity
    mean_velocity: mean velocity
    nbr_push: number total of push
    time_max_velocity : time associated with the maximun velocity
    time_5per_cent: time associated with the mean velocity
    index_max: index of the TimeSeries associated with the maximun velocity
    index_mean: index associted with the 5% mean velocity
    nbr_analyse: desired number of analysis

    Returns
    -------
    None
    """
    st.write("Max velocity: ", round(3.6*radius*max_velocity, 2), " km/h")
    st.write("Mean velocity: ", round(
        3.6*radius*mean_velocity, 2), " km/h")
    st.write("Number of push: ", nbr_push)
    st.write("Total running time: ",
             round(kinetics.data['Velocity'][-1], 2), " s")

    st.write("Click on the top right corner to enlarge !")
    fig = a.display_graph(kinetics, time_max_velocity, time_5_per_cent,
                          mean_velocity, max_velocity,
                          index_max, index_mean)
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.download_button(
        label="Download graph",
        data=buf,
        file_name='graph_smart_wheel.png',
        mime="image/png")

    df = a.extract_data(kinetics, nbr_analyse)
    st.dataframe(df)

    df_convert = convert_df(df)

    st.download_button(
        label="Download dataframe",
        data=df_convert,
        file_name='df_smart_wheel.csv',
        mime='text/csv',)


if __name__ == "__main__":
    st.title("Smart wheel Analyse")

    format_data = st.selectbox('What is the data format?',
                               ('smartwheel', 'racingwheel', 'smartwheeltxt'))
    filename = st.file_uploader("Choose a file")

    if filename is None:
        option = st.selectbox(
            'Add a file or select since example',
            ('pushrimkinetics_propulsion.csv',
             'pushrimkinetics_offsets_propulsion.csv',
             'pushrimkinetics_offsets_baseline.csv'))

        kinetics = ktk.pushrimkinetics.read_file(option,
                                                 file_format='smartwheel')

        kinetics = a.analyse_data(kinetics)

        # Calculation of relevant values
        max_velocity = a.calculate_max_velocity(kinetics)
        time_max_velocity, index_max = a.calculate_time_max_velocity(kinetics,
                                                                     max_velocity)

        mean_velocity = a.calculate_mean_velocity(kinetics)
        time_5_per_cent, index_mean = a.calculate_time_5_per_cent_mean_velocity(
            kinetics, mean_velocity)

        nbr_push = a.calculate_push_number(kinetics)

        nbr_analyse = st.slider('How many cycles do you want to analyze?', 0,
                                nbr_push, 1)

        radius = st.number_input('Indicate the radius in meters')

        if st.button("Start"):
            display_analyse(kinetics, radius, max_velocity, mean_velocity,
                            nbr_push, time_max_velocity, time_5_per_cent,
                            index_max, index_mean, nbr_analyse)

    if filename is not None:
        # Reading and analysis of the file
        kinetics = ktk.pushrimkinetics.read_file(filename,
                                                 file_format=format_data)

        kinetics = a.analyse_data(kinetics)

        # Calculation of relevant values
        max_velocity = a.calculate_max_velocity(kinetics)
        time_max_velocity, index_max = a.calculate_time_max_velocity(kinetics,
                                                                     max_velocity)

        mean_velocity = a.calculate_mean_velocity(kinetics)
        time_5_per_cent, index_mean = a.calculate_time_5_per_cent_mean_velocity(
            kinetics, mean_velocity)

        nbr_push = a.calculate_push_number(kinetics)

        nbr_analyse = st.slider('How many cycles do you want to analyze?', 0,
                                nbr_push, 5)

        radius = st.number_input('Indicate the radius in meters')

        if st.button("Start"):
            display_analyse(kinetics, radius, max_velocity, mean_velocity,
                            nbr_push, time_max_velocity, time_5_per_cent,
                            index_max, index_mean, nbr_analyse)
