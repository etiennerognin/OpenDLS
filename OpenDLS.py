# Libraries
# =========
import sys
import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Global parameters
# =================
try: N_meas = int(sys.argv[1])
except: N_meas = 1		# Number of measurements to take from Arduino

N_points=800            # Number of sampling points per serial pass
address='/dev/ttyUSB0'  # Arduino address
baud=115200             # baud for serial communication
lambd = 650e-9          # [m] Laser wavelength
n_s = 1.33              # Solvent refractive index at wavelength
k = 1.380649e-23        # [j/k] Boltzmann constant
T = 293                 # [K] Temperature
eta_s = 0.001           # [Pa.s] Solvent viscosity measurement at T
theta = np.pi/2         # Scattering angle
    

def data_from_Arduino():
    # Harvest 'N_points' data points from the Arduino via serial com.
    # Retrun tuple as (time series, duration of the whole sampling)
    # Duration is in microseconds
    
    
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
    
    #start serial com
    ser = serial.Serial(address,baud)
    print 'iter, duration, time step'
    print '-------------------------'

    # Loop over multiple measurements
    # ===============================
    for i in range(N_meas):
        
        # Harvest the data from the Arduino
        series, duration = data_from_Arduino()
        
        print i, duration, duration/N_points
        
        # Auto-correlation calculation
        auto = autocorrelate(series)
        
        auto_cum += auto

    # Display output
    # ==============

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

    dt = duration/N_points
    time = np.linspace(dt, duration, num=N_points, endpoint=True)
    ax1.plot(time, series, 'b-')
    ax1.plot(time, series, 'b.')
    ax1.set_xlabel('time (microseconds)')
    ax1.set_ylabel('detector value (a.u.)')
    
    
    ax2.semilogx(time[:N_points/2], auto[:N_points/2], '-')
    ax2.set_xlabel('time (microseconds)')
    ax2.set_ylabel('Autocorrelation (a.u.)')
    
    ax3.semilogx(time[:N_points/2], auto_cum[:N_points/2], '-')
    ax3.set_xlabel('time (microseconds)')
    ax3.set_ylabel('Cumulated autocorrelation (a.u.)')
    
    plt.show()

    # Curve fitting
    # =============
    
    # scattering vector
    q = 4*np.pi/lambd*n_s*np.sin(theta/2)
    
    # Function to fit
    def g(tau, a, b, c):
        return a*np.ones_like(tau) + b*np.exp(-c*tau)
        
    tau = 1e-6*time[:N_points/2]
    ydata = auto_cum[:N_points/2]
    # initial guess
    a0 = auto_cum[-1]
    b0 = auto_cum[0] - a0
    c0 = 2*q**2*k*T/(18*1e-7*eta_s)

    popt, pcov = curve_fit(g, tau, ydata, p0=[a0, b0, c0])
    
    (a, b, c) = popt
    
    # Extract hydrodynamic radius from fit
    D = c/(2*q**2)                  # Diffusion coefficient
    Rh = k*T/(6*np.pi*D*eta_s)      # Radius
    psize = 2*Rh*1e9                # Particle size in nanometers
    
    # Extract error
    perr = np.sqrt(np.diag(pcov))
    dc_over_c = perr[2]/c
    psizeerr = dc_over_c*psize
    

    plt.semilogx(tau, ydata, 'k.', label='Experiment')
    plt.semilogx(tau, g(tau, a, b, c), 'r-', label='fit: Diffusion = %.2E m^2/s, Particle size=%d nm, ' % (D,psize))
    plt.semilogx(tau, g(tau, a, b, 0.83*c), 'r--', label='+/- 20% in size')
    plt.semilogx(tau, g(tau, a, b, 1.25*c), 'r--')
    plt.xlabel('Tau (s)')
    plt.ylabel('Auto-correlation')
    plt.legend()
    plt.show()
    
