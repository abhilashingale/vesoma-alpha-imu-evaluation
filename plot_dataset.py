import os
import pandas as pd
import matplotlib.pyplot as plt

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv') or f.endswith('.txt')]

files =  ["BAUD_1M_I2C_FREQ_400kHZ_UPDATE_FREQ_400Hz_BNO085_exp_06_500us_wait_I2C_game_Rotation_vector.csv"]

for fname in files:
    path = os.path.join(data_dir, fname)
    df = pd.read_csv(path)  # Automatically uses first row as headers

    time = (df.iloc[:, 0] - df.iloc[0, 0])/1000  # Normalize time to start at 0 and scale milliseconds to seconds

    # Prepare data
    quat_x = df.iloc[:, 1]
    quat_y = df.iloc[:, 2]
    quat_z = df.iloc[:, 3]
    quat_w = df.iloc[:, 4]
    acc_x = df.iloc[:, 5]
    acc_y = df.iloc[:, 6]
    acc_z = df.iloc[:, 7]
    gyro_x = df.iloc[:, 8]
    gyro_y = df.iloc[:, 9]
    gyro_z = df.iloc[:, 10]

    # Create a figure with 3 rows (one for each plot type)
    fig, axs = plt.subplots(3, 1, figsize=(12, 14))

    # Plot quaternion values (4 subplots in first row)
    axs0 = axs[0].twinx()  # To overlay all quaternions on the same axis
    axs[0].plot(time, quat_x, label='Quat X')
    axs[0].plot(time, quat_y, label='Quat Y')
    axs[0].plot(time, quat_z, label='Quat Z')
    axs[0].plot(time, quat_w, label='Quat W')
    axs[0].set_ylabel('Quaternion')
    axs[0].set_title('Quaternion Values')
    axs[0].legend()

    # Plot acceleration values
    axs[1].plot(time, acc_x, label='Acc X')
    axs[1].plot(time, acc_y, label='Acc Y')
    axs[1].plot(time, acc_z, label='Acc Z')
    axs[1].set_ylabel('Acceleration')
    axs[1].set_title('3-Axis Acceleration')
    axs[1].legend()

    # # Plot gyroscope values
    # axs[2].plot(time, gyro_x, label='Gyro X')
    # axs[2].plot(time, gyro_y, label='Gyro Y')
    # axs[2].plot(time, gyro_z, label='Gyro Z')
    # axs[2].set_ylabel('Gyroscope')
    # axs[2].set_xlabel('Time (s)')
    # axs[2].set_title('3-Axis Gyroscope')
    # axs[2].legend()

    fig.suptitle(f'Sensor Data: {fname}')
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save the figure
    os.makedirs('graphs', exist_ok=True)
    save_name = os.path.splitext(fname)[0] + '.png'
    save_path = os.path.join('graphs', save_name)
    plt.savefig(save_path)

    plt.show()
