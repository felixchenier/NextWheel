"""
The module permit to calibrate the instrumented wheel.

To be use with the nextwheel module ?
"""

import numpy as np


def normalize_vector(ob: np.ndarray) -> np.ndarray:
    """
    Normalize all vectors in multiple line array (each line is a vector).

    The function is for clarity.

    Parameters
    ----------
    ob : np.ndarray

    Returns
    -------
    normalized_vector : np.ndarray

    """
    normalized_vector = ob / np.tile(
        np.linalg.norm(ob, axis=0), (np.size(ob, axis=0), 1)
    )
    return normalized_vector


def estimate_gyro_bias(omega_static: np.ndarray) -> np.ndarray:
    """
    Estimate the Gyro bias with a static trial.

    Parameters
    ----------
    omega_static : np.ndarray
        Angular speed measure with the IMU (Gyro) - the wheel isn't suppose to
        move in a static trial, this is the bias.

    Returns
    -------
    bias : np.ndarray
        Median of the omega_static argument.

    """
    bias = np.median(omega_static, axis=0)
    return bias


def estimate_acc_bias(
    acc_static1: np.ndarray, acc_static2: np.ndarray, acc_static3: np.ndarray
) -> np.ndarray:
    """
    Estimate the bias of the accelerometer.

    The function needs three different static trials to estimate the bias of
    the accelerometer of the IMU. In short, the accelerometer measures a vector
    m that contain the measurement in x, y, z. If we observe the norm. we have:

        mx^2 + my^2 + mz^2 = (ax + bx)^2 + (ay + by)^2 + (az + bz)^2 = N^2.

    Where mx, my and mz are measure of the accelerometer, ax, ay and az are
    the acceleration of the gravity and bx, by and bz are the bias. N is the
    norm of the m vector.

    If we develop, we obtain :

        ax^2 + ay^2 + az^2 + 2(axbx + ayby + azbz) + bx^2 + by^2 + bz^2 = N^2
        = ||g||^2 + 2(axbx + ayby + azbz) + ||bias||^2 = N^2

    If we substract two norms square of two m vectors, the constant cancel each
    and we obtain :

        (N^2 - N'^2)/2 = bx(ax - ax') + by(ay - ay') + bz(az - az')

    This is the final equation, because (ax - ax') = (mx - mx'), (ay - ay') =
    (my - my') and (az - az') = (mz - mz'). This is already known. With three
    static trials, there is three equations and three unknown, so we can find
    the bias with a linear system Ax = b.

    Exemple with three static trial :

    [ (ax1 - ax2) (ay1 - ay2) (az1 - az2) ] [ bx ]     [ (N1^2 - N2^2)/2 ]
    [ (ax1 - ax3) (ay1 - ay3) (az1 - az3) ] [ by ]  =  [ (N1^2 - N3^2)/2 ]
    [ (ax2 - ax3) (ay2 - ay3) (az2 - az3) ] [ bz ]     [ (N2^2 - N3^2)/2 ]


    Parameters
    ----------
    acc_static1 : np.ndarray
        Measurement of the acceleration of the first static trial.
    acc_static2 : np.ndarray
        Measurement of the acceleration of the second static trial.
    acc_static3 : np.ndarray
        Measurement of the acceleration of the third static trial.

    Returns
    -------
    bias : np.ndarray
        Estimated bias.

    """
    grav1 = np.median(acc_static1, axis=0)
    grav2 = np.median(acc_static2, axis=0)
    grav3 = np.median(acc_static3, axis=0)

    norm1 = np.linalg.norm(grav1)
    norm2 = np.linalg.norm(grav2)
    norm3 = np.linalg.norm(grav3)

    delta_grav12 = grav1 - grav2
    delta_grav13 = grav1 - grav3
    delta_grav23 = grav2 - grav3

    delta_norm12 = norm1**2 - norm2**2
    delta_norm13 = norm1**2 - norm3**2
    delta_norm23 = norm2**2 - norm3**2

    norm_vector = np.vstack((delta_norm12, delta_norm13, delta_norm23))

    grav_matrix = np.vstack((delta_grav12, delta_grav13, delta_grav23))

    bias = np.linalg.solve(grav_matrix, norm_vector / 2)

    return bias


def get_z_axis_delsys_on_wheel(
    gyro_bias: np.ndarray, omega_dynamic: np.ndarray
) -> np.ndarray:
    """
    Calculate the z-axis with the IMU (Gyroscope).

    It takes a static and a dynamic trial of the angular speed of the
    instrumented wheel:
        - The static trial serve to find the bias of the Gyro
        - The dynamic trial is what determine the z_axis

    Parameters
    ----------
    omega_static : np.ndarray
        Angular speed measure with the IMU (Gyro) - the wheel isn't suppose to
        move in a static trial, this is the bias.
    omega_dynamic : np.ndarray
        Angular speed measure with the IMU (Gyro) - the IMU return the axis
        it turns around with the angular speed. The axis is the z_axis
        unnormalize with the bias.

    Returns
    -------
    z_axis : np.ndarray
        This is the median of the normalized omega_dynamic without bias and
        re-normalized.

    """
    omega_dynamic -= np.tile(gyro_bias, (np.size(omega_dynamic, axis=0), 1))
    z_axis = normalize_vector(
        np.median(normalize_vector(omega_dynamic), axis=0)
    )
    return z_axis


def get_delsys_reference(
    acc_static1: np.ndarray, acc_static2: np.ndarray, z_axis: np.ndarray
) -> np.ndarray:
    """
    Calculate the x and y axis with two trials and the z axis.

    The IMU measure the acceleration with accelerometer, so the gravity is
    measured as well. The static trials measure two accelerations (with bias)
    of the gravity with the wheel at different angle. If you subtract one from
    another, we get rid of the bias and the new vector is in the xz-plane. From
    there, we can apply a cross product to find the y and than x or use the
    Gram–Schmidt process to find x first. The last one is used in this
    function.

    Parameters
    ----------
    acc_static1 : np.ndarray
        Gravity measured with the IMU (accelerometer) with a static trial. The
        trial include the bias of the accelerometer.
    acc_static2 : np.ndarray
        Similar to acc_static1 but with a different angle in the xz plane.
    z_axis : np.ndarray
        The z-axis find in previous step.

    Returns
    -------
    wheel_ref_delsys : np.ndarray
        The complete delsys on wheel reference rotation matrix.
    """
    grav1 = np.median(acc_static1, axis=0)
    grav2 = np.median(acc_static2, axis=0)

    if np.dot(grav1, z_axis) < 0:
        z_axis = -z_axis

    if np.dot(grav1, z_axis) > np.dot(grav2, z_axis):
        delta_grav = grav2 - grav1
    else:
        delta_grav = grav1 - grav2

    x_axis = normalize_vector(
        delta_grav - (np.dots(delta_grav, z_axis) * z_axis)
    )

    y_axis = normalize_vector(np.cross(z_axis, x_axis))

    wheel_ref_delsys = np.hstack((x_axis, y_axis, z_axis, np.array([0, 0, 0])))
    wheel_ref_delsys = np.vstack(
        (wheel_ref_delsys, np.array([[0], [0], [0], [1]]))
    )

    return wheel_ref_delsys


def calculate_calibration_matrix(FM: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Resolve the A @ V = FM to find A, the calibration matrix.

    We rewrite the equation with V^T @ A^T = FM^T. This can be seen as multiple
    linear equation to resolve. FM and V must have at least 6 columns (trials).

    Exemple :

        [(V^T @ a1) (V^T @ a2) (V^T @ a3) ...] = [f1 f2 f3 ...]

    where ak is the kth line of A and fk is the kth line of FM. We have the n
    linear equations that follows :

        V^T @ a1 = f1
        V^T @ a2 = f2
        V^T @ a3 = f3
            ...
        V^T @ an = fn

    Parameters
    ----------
    FM : np.ndarray
        Forces and moments matrix of all trials. The line three first line
        must be the force in x, y, z and the last three values are the moments.
    V : np.ndarray
        Voltages measured with the EMG installed in the instrumented wheel for
        each trials. Must be the same shape of the FM.

    Returns
    -------
    np.ndarray
        The calibration matrix A.

    """
    AT = np.linalg.lstsq(np.transpose(V), np.transpose(FM))

    return np.transpose(AT)


def calculate_forces_moments(
    theta: float,
    acc_static: np.ndarray,
    acc_bias: np.ndarray,
    wheel_ref_delsys: np.ndarray,
    masse: float = 1.0,
    masse_mc: float = 0.46,
    D: float = 0.52,
    H: float = 0.05,
):
    """
    Estimate the forces and moments of one trial.

    Parameters
    ----------
    theta : float
        DESCRIPTION.
    acc_static : np.ndarray
        DESCRIPTION.
    acc_bias : np.ndarray
        DESCRIPTION.
    wheel_ref_delsys : np.ndarray
        DESCRIPTION.
    masse : float, optional
        DESCRIPTION. The default is 1.0 kg.
    masse_mc : float, optional
        DESCRIPTION. The default is 0.46 kg.
    D : float, optional
        DESCRIPTION. The default is 0.52 m.
    H : float, optional
        DESCRIPTION. The default is 0.05 m.

    Returns
    -------
    forces : TYPE
        DESCRIPTION.
    moments : TYPE
        DESCRIPTION.

    """
    force_application_point = np.nadarray((3, 1))
    force_application_point[0] = 0.5 * D * np.cos(np.pi * theta / 180)
    force_application_point[1] = 0.5 * D * np.sin(np.pi * theta / 180)
    force_application_point[2] = H

    ref_grav = normalize_vector(np.median(acc_static - acc_bias, axis=0))

    f1 = (
        -1
        * masse
        * 9.81
        * np.dot(np.transpose(wheel_ref_delsys[:3, :3]), ref_grav)
    )  # Est-ce que ref_grav doit être normaliser (je crois que oui?), sinon,
    # on a la norme de la gravité deux fois dans l'équation...le biais n'est
    # pas en quelque sorte déjà inclu ?

    f2 = (
        -1
        * masse_mc
        * 9.81
        * np.dot(np.transpose(wheel_ref_delsys[:3, :3]), ref_grav)
    )

    forces = f1 + f2
    moments = np.cross(f1, force_application_point) + np.cross(
        (f1 + f2), np.array([[0], [0], [H]])
    )  # le moment de f1 n'est pas calculé deux fois avec H ???

    return forces, moments
