"""Mangement of the constant."""


def csv_count_line(filename: str) -> int:
    """
    Count line number in a csv file.

    Parameters
    ----------
    filename : file with csv file

    Returns
    -------
    Return number of line
    """
    with open(filename, 'r') as f:
        n = 0
        for line in f:
            n += 1
    return n


data_wheel_file = 'kinetics.csv'
nbr_JSON_per_framme = 10
nbr_JSON_total = csv_count_line(data_wheel_file)
nbr_JSON_per_second = nbr_JSON_total/17

print("Number of JSON per second: ", round(nbr_JSON_per_second, 1))
real = 1 / (nbr_JSON_per_second/nbr_JSON_per_framme)

print("Tramme sent all ", round(real, 3), "s")

LENGTH_BUFFER = 100000

timer_fresh = 10
