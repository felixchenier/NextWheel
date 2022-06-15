"""Mangement of the constant."""

import kineticstoolkit.lab as ktk


def truncate(n, decimals=0):
    """
    Round up a number.

    Each digit after a given position is replaced by 0.

    Parameters
    ----------
    n : number
    decimals : decimal for rounding (positive or negative)

    Returns
    -------
    Return the rounding number
    """
    multiplier = 10 ** decimals
    return int(int(n * multiplier) / multiplier)


filename = (
    ktk.doc.download('pushrimkinetics_offsets_propulsion.csv')
)

kinetics = ktk.pushrimkinetics.read_file(filename, file_format='smartwheel')

nbr_JSON_per_framme = 100
nbr_JSON_total = 7600
nbr_JSON_per_second = nbr_JSON_total/17

print("Number of JSON per second: ", round(nbr_JSON_per_second, 1))
real = 1 / (nbr_JSON_per_second/nbr_JSON_per_framme)

print("Tramme sent all ", round(real, 3), "s")

LENGTH_BUFFER = 100000

timer_fresh = 10
