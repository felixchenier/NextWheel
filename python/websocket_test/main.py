import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from nextwheel import NextWheel
from datetime import datetime

# ADC_LOG_FILENAME = "log_adc.csv"
# IMU_LOG_FILENAME = "log_imu.csv"

# fid_adc = open(ADC_LOG_FILENAME, "w")
# fid_adc.write(
#     "Y,M,D,h,m,s,us,ch[0],ch[1],ch[2],ch[3],ch[4],ch[5],ch[6],ch[7]\n"
# )
# fid_imu = open(IMU_LOG_FILENAME, "w")
# fid_imu.write(
#     "Y,M,D,h,m,s,us,"
#     "acc[0],acc[1],acc[2],"
#     "gyro[0],gyro[1],gyro[2],"
#     "mag[0],mag[1],mag[2]\n"
# )

power_values = []
voltage_values = []
current_values = []
power_time = []

encoder_values = []
encoder_time = []

mpl.rcParams["axes.prop_cycle"] = mpl.cycler(
    color=["r", "g", "b", "c", "m", "y", "k", "tab:orange"]
)
mpl.rcParams["figure.figsize"] = [10, 5]
mpl.rcParams["figure.dpi"] = 75
mpl.rcParams["lines.linewidth"] = 1

# define and adjust figure
fig = plt.figure(figsize=(12, 8))

adc_plot = plt.subplot(1, 1, 1)  # row, col, index
adc_plot.set_title("ADC")

# imu_plot = plt.subplot(4, 1, 2)  # row, col, index
# imu_plot.set_title("IMU")
#
# power_plot = plt.subplot(4, 1, 3)  # row, col, index
# power_plot.set_title("POWER")
#
# encoder_plot = plt.subplot(4, 1, 4)  # row, col, index
# encoder_plot.set_title("ENCODER")
plt.tight_layout()


# # funct to update the data
def update_plots(i):
    """
    Update the plots.

    This function updates the plots using global variables adc_values,
    imu_values, power_values and encoder_values. It is normally called by
    Matplotlib's FunctAnimation class.
    """
    data = nw.fetch()

    # ADC
    adc_plot.cla()
    adc_plot.set_title(f"[{i}] - Force Channels (ADC)")
    adc_plot.plot(data["Analog"]["Time"], data["Analog"]["Force"])

    # IMU
    # imu_plot.cla()
    # imu_plot.set_title("IMU")
    # imu_plot.plot(
    #     data["IMU"]["Time"],
    #     data["IMU"]["Acc"],
    #     data["IMU"]["Time"],
    #     data["IMU"]["Gyro"],
    #     data["IMU"]["Time"],
    #     data["IMU"]["Mag"],
    # )
    #
    # # POWER Sample frequency too slow to just use nw.fetch() alone
    # if len(data["Power"]["Time"]) != 0:
    #     power_time.append(data["Power"]["Time"][0])
    #     power_values.append(data["Power"]["Power"][0])
    #     voltage_values.append(data["Power"]["Voltage"][0])
    #     current_values.append(data["Power"]["Current"][0])
    #
    # if len(power_time) > 10:
    #     power_time.pop(0)
    #     power_values.pop(0)
    #     voltage_values.pop(0)
    #     current_values.pop(0)
    #
    # power_plot.cla()
    # power_plot.set_title("Battery level")
    # power_plot.plot(
    #     power_time,
    #     voltage_values,
    #     power_time,
    #     current_values,
    #     power_time,
    #     power_values,
    # )
    #
    # # ENCODER Sample frequency too slow to just use nw.fetch() alone
    # if len(data["Encoder"]["Time"]) != 0:
    #     encoder_time.append(data["Encoder"]["Time"][0])
    #     encoder_values.append(data["Encoder"]["Angle"][0])
    #
    # if len(power_time) > 10:
    #     encoder_time.pop(0)
    #     encoder_values.pop(0)
    #
    # encoder_plot.cla()
    # encoder_plot.set_title("Encoder")
    # encoder_plot.plot(encoder_time, encoder_values)


if __name__ == "__main__":
    # websocket.enableTrace(True)  # Uncomment to print all received data
    nw = NextWheel("10.0.1.2")
    nw.connect()

    # Set device to current time (unix time)
    nw.set_time(str(int(datetime.now().timestamp())))

    ani = FuncAnimation(fig, update_plots, interval=100)
    plt.show()
