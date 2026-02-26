import os
import pandas as pd
import matplotlib.pyplot as plt

data_dir = 'data/'
time_col_candidates = ['Timestamp', 'timestamp', 'time', 't']

def find_time_column(df):
    for col in time_col_candidates:
        if col in df.columns:
            return col
    raise ValueError("No time column found in CSV.")




if __name__ == "__main__":

    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    n_files = len(csv_files)
    if n_files == 0:
        print("No CSV files found in the directory.")
        exit(1)

    # Ensure plots directory exists
    plots_dir = 'histograms'
    os.makedirs(plots_dir, exist_ok=True)

    csv_files = ["BAUD_1M_I2C_FREQ_400kHZ_UPDATE_FREQ_400Hz_BNO085_exp_01_different_update_rates_200us_waitI2C.csv", "BAUD_1M_I2C_FREQ_400kHZ_UPDATE_FREQ_400Hz_BNO085_exp_02_different_update_rates_100us_waitI2C.csv","BAUD_1M_I2C_FREQ_400kHZ_UPDATE_FREQ_400Hz_BNO085_exp_04_500us_wait_I2C_quat_and_gyro_only.csv","BAUD_1M_I2C_FREQ_400kHZ_UPDATE_FREQ_400Hz_BNO085_exp_05_500us_wait_I2C.csv"] 

    for filename in csv_files:
        filepath = os.path.join(data_dir, filename)
        df = pd.read_csv(filepath)
        plt.figure(figsize=(8, 4))
        try:
            time_col = find_time_column(df)
            times = df[time_col]
            if times.isnull().all():
                # Try as float/int seconds
                times = df[time_col].astype(float)
                time_diffs = times.diff().dropna()  # Convert to microseconds if in milliseconds
            else:
                # Assume times are relative (e.g., seconds or milliseconds)
                times = df[time_col].astype(float)
                time_diffs = times.diff().dropna()  # Convert to microseconds if in milliseconds
            bin_width = 200  # Set a smaller bin width (e.g., 10 microseconds)
            min_diff = time_diffs.min()
            max_diff = time_diffs.max()
            bins = int((max_diff - min_diff) / bin_width)
            plt.hist(time_diffs.values, bins=bins, edgecolor='k')
            plt.title(f"Time Differences: {filename}")
            plt.suptitle(f"Total samples: {len(df)}", fontsize=10, y=0.96)
            plt.ylabel('No. of Data samples (tuple of Quaternions, Accel, Gyro)')
            plt.xlabel('Time Difference Between Data Points (microseconds)')
            plt.grid(True)
        except Exception as e:
            plt.text(0.5, 0.5, f"Error: {e}", ha='center', va='center', transform=plt.gca().transAxes)
            plt.title(f"{filename} (Error)")
            plt.suptitle(f"Total samples: {len(df)}", fontsize=10, y=0.96)
            plt.ylabel('No. of Data samples (tuple of Quaternions, Accel, Gyro)')
            plt.xlabel('Time Difference Between Data Points (microseconds)')
            plt.grid(True)
        plt.tight_layout()
        # Save plot as PNG in plots/ directory
        plot_filename = os.path.splitext(filename)[0] + '.png'
        plot_path = os.path.join(plots_dir, plot_filename)
        plt.savefig(plot_path)
        plt.show()