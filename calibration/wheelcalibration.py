"""
The module permit to calibrate the instrumented wheel.

The module use the NextWheel module to calibrate the instrumented wheel.

"""

import numpy as np
import math


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
        Mean of the omega_static argument.

    """
    bias = np.mean(omega_static, axis=0)

    return bias


def estimate_acc_bias(  # À modifier pour avoir plus de tâches
    acc_statics: np.ndarray,
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

        ax^2 + ay^2 + az^2 + 2(ax*bx + ay*by + az*bz) + bx^2 + by^2 + bz^2 = N^2
        = ||g||^2 + 2(ax*bx + ay*by + az*bz) + ||bias||^2 = N^2

    If we substract two norms square of two m vectors, the constants cancel and
    we obtain :

        (N^2 - N'^2)/2 = bx*(ax - ax') + by*(ay - ay') + bz*(az - az')

    This is the final equation, because (ax - ax') = (mx - mx'), (ay - ay') =
    (my - my') and (az - az') = (mz - mz'). This is already known. With three
    static trials, there is three equations and  three unknown, so we can find
    the bias with a linear system Ax = b. A -> (N,3) et b -> (N,1) avec N >=3.

    Exemple with three static trials :

    [ (ax1 - ax2) (ay1 - ay2) (az1 - az2) ] [ bx ]     [ (N1^2 - N2^2)/2 ]
    [ (ax1 - ax3) (ay1 - ay3) (az1 - az3) ] [ by ]  =  [ (N1^2 - N3^2)/2 ]
    [ (ax2 - ax3) (ay2 - ay3) (az2 - az3) ] [ bz ]     [ (N2^2 - N3^2)/2 ]


    Parameters
    ----------
    acc_statics : np.ndarray
        Contain at least three different static measurements of the wheel. Each
        line must be the median of an different static trial of the
        accelerometer.

    Returns
    -------
    bias : np.ndarray
        Estimated bias.

    """
    m, n = np.shape(acc_statics)
    norms = np.linalg.norm(acc_statics, axis=1)

    m_line_matrix = int(math.factorial(m) / (2 * math.factorial(m - 2)))

    delta_grav_matrix = np.zeros((m_line_matrix, 3))
    delta_norm_square = np.zeros((m_line_matrix, 1))

    i = 0
    for j in range(m):
        for k in range(j + 1, m):
            delta_grav_matrix[i, :] = acc_statics[j, :] - acc_statics[k, :]
            delta_norm_square[i, 0] = (norms[j] ** 2 - norms[k] ** 2) / 2
            i += 1

    bias = np.linalg.lstsq(delta_grav_matrix, delta_norm_square, rcond=None)

    return bias[0].T


def get_z_axis(gyro_bias: np.ndarray, omega_dynamic: np.ndarray) -> np.ndarray:
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
        This is the mean of the normalized omega_dynamic without bias and
        re-normalized.

    """
    omega_dynamic -= np.tile(gyro_bias, (np.shape(omega_dynamic)[0], 1))

    z_axis = omega_dynamic / np.transpose(
        np.tile(np.linalg.norm(omega_dynamic, axis=1), (3, 1))
    )

    z_axis = np.mean(
        z_axis,
        axis=0,
    )
    z_axis = z_axis / np.linalg.norm(z_axis)

    return z_axis


def get_wheel_reference(
    acc_static1: np.ndarray, acc_static2: np.ndarray, z_axis: np.ndarray
) -> np.ndarray:
    """
    Calculate the x and y axis with two trials and the z axis.

    The IMU measure the acceleration with accelerometer and the gravity is
    measured as well. The static trials measure two accelerations (with bias)
    of the gravity with the wheel at different angle. If you subtract one from
    another, we get rid of the bias and the new vector is in the xz-plane. From
    there, we can apply a cross product to find the y and then x or use the
    Gram–Schmidt process to find x first.

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
    wheel_ref : np.ndarray
        The complete wheel reference rotation matrix.
    """
    grav1 = np.mean(acc_static1, axis=0)
    grav2 = np.mean(acc_static2, axis=0)

    # if np.dot(grav1, z_axis) < 0:
    #     z_axis = -z_axis

    if np.abs(np.dot(grav1, z_axis)) > np.abs(np.dot(grav2, z_axis)):
        delta_grav = grav2 - grav1
    else:
        delta_grav = grav1 - grav2

    # x_axis = delta_grav - (np.dot(delta_grav, z_axis) * z_axis)
    # x_axis = x_axis / np.linalg.norm(x_axis)

    y_axis = np.cross(z_axis, delta_grav + z_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)

    x_axis = np.cross(y_axis, z_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)

    wheel_ref = np.vstack((x_axis, y_axis, z_axis))

    return wheel_ref


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
        Forces and moments matrix of all trials. The three first lines
        must be the force in x, y, z and the last three values are the moments.
    V : np.ndarray
        Voltages measured with the EMG installed in the instrumented wheel for
        each trials. Must be the same shape as FM.

    Returns
    -------
    np.ndarray
        The calibration matrix A.

    """
    AT = np.linalg.lstsq(V.T, FM.T, rcond=None)[0]

    return AT.T


def make_an_estimation_of_forces_moments(
    Trial: dict,
    acc_bias: np.ndarray,
    wheel_ref: np.ndarray,
    D: float = 0.52,
    H: float = 0.05,
):
    """
    Estimate the forces and moments of one trial.

    Parameters
    ----------
    Trial : dict
        Dictonary of one complete trial including the mass and degree.
    acc_bias : np.ndarray
        The accelerometer bias.
    wheel_ref : np.ndarray
        The 3x3 Matrix that link the IMU referential to the wheel referential.
    D : float, optional
        The diameter of the pushrim. The default is 0.52 m.
    H : float, optional
        The perpendicular distance between the wheel plane and the pushrim.
        It is the z-distance in cyclindrical coordinates of the wheel.
        The default is 0.05 m.

    Returns
    -------
    forces : np.ndarray
        The theorical estimate of the forces applied on the pushrim.
    moments : np.ndarray
        The theorical estimate of the moments applied on the pushrim..

    """
    force_application_point = np.ndarray((3, 1))
    force_application_point[0] = (
        0.5 * D * np.cos(np.pi * Trial["Degree"] / 180)
    )
    force_application_point[1] = (
        0.5 * D * np.sin(np.pi * Trial["Degree"] / 180)
    )
    force_application_point[2] = H  # H or -H ?
    force_application_point = np.transpose(force_application_point)

    ref_grav = np.transpose(np.mean(Trial["IMU"]["Acc"], axis=0) - acc_bias)
    ref_grav = ref_grav / np.linalg.norm(ref_grav)

    f1 = -1 * Trial["Mass"] * 9.81 * np.dot(wheel_ref[:3, :3], ref_grav)
    f1 = np.transpose(f1)

    # f2 = -1 * mass_mc * 9.81 * np.dot(wheel_ref_delsys[:3, :3], ref_grav)
    # f2 = np.transpose(f2)

    # f2 = [0, 0, 0]

    # forces = f1 + f2
    forces = f1
    moments = -np.cross(f1, force_application_point)
    # - np.cross(f2, np.array([[0, 0, H]]))

    return forces, moments
