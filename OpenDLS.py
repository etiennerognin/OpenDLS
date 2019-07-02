
import serial
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

# Global parameters
# =================
N_points=800            # Number of sampling points per serial pass
address='/dev/ttyUSB0'  # Arduino address
baud=115200             # baud for serial communication

def data_from_Arduino():
    # Harvest 'N_points' data points from the Arduino via serial com.
    # Retrun tuple as (time series, duration of the whole sampling)
    # Duration is in microseconds
    
    ser = serial.Serial(address,baud)
    newdata = ser.readline()
    raw_data = np.fromstring(newdata, sep=',')
    return (raw_data[0:N_points], raw_data[-1])
    
def autocorrelate(series):
    # Calculate the auto-correlation function using FFT
    
    N = len(series)
    s_hat = np.fft.rfft(series)
    return np.fft.irfft(s_hat*np.conj(s_hat), N)

if __name__ == '__main__':
    
    # Setup
    # =====
    # Cummulative autocorrelation
    auto_cum = np.zeros(N_points)
    
    # Number of measurements to take from Arduino
    N_meas = 10

    # Loop over multiple measurements
    for i in range(N_meas):
        
        # Harvest the data from the Arduino
        series, duration = data_from_Arduino()
        
        print i, duration
        
        # Auto-correlation calculation
        auto = autocorrelate(series)
        
        auto_cum += auto

    # Display output

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

    dt = duration/N_points
    time = np.linspace(dt, duration, num=N_points, endpoint=True)
    ax1.plot(time, series)
    ax1.set_xlabel('time (microseconds)')
    ax1.set_ylabel('detector value (a.u.)')
    
    
    ax2.semilogx(time[:N_points/2], auto[:N_points/2], '+')
    ax2.set_xlabel('time (microseconds)')
    ax2.set_ylabel('Autocorrelation (a.u.)')
    
    ax3.semilogx(time[:N_points/2], auto_cum[:N_points/2], '.')
    ax3.set_xlabel('time (microseconds)')
    ax3.set_ylabel('Cumulated autocorrelation (a.u.)')
    
    plt.show()
