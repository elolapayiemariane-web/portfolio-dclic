import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# SIGNAL 1 : s(t) = sin(2*pi*f0*t)
N = 500
f0 = 5          # frequence du signal (Hz)
Fe = 10 * f0    # frequence d'echantillonnage (Hz)
tn = np.arange(N) * (1 / Fe)
sn = np.sin(2 * np.pi * f0 * tn)

Xk = np.fft.fft(sn)
module_Xk = np.abs(Xk)
module_Xk_d = np.fft.fftshift(module_Xk)
freq = np.fft.fftfreq(N) * Fe
freq_d = np.fft.fftshift(freq)

#Signal temporel
plt.figure(1)
plt.plot(tn, sn)
plt.title(r"Signal 1 : $s_n = \sin(2\pi f_0 t_n)$  -  $f_0 = 5$ Hz")
plt.xlabel(r"$t_n$ (s)")
plt.ylabel(r"$s_n$")
plt.grid(True)

#Spectre brut
plt.figure(2)
plt.plot(module_Xk)
plt.title(r"Signal 1 : Spectre d'amplitude $|X_k|$ du Signal 1 : $s_n = \sin(2\pi f_0 t_n)$")
plt.xlabel("Indice k")
plt.ylabel(r"$|X_k|$")
plt.grid(True)

#Spectre decale
plt.figure(3)
plt.plot(freq_d, module_Xk_d)
plt.title(r"Signal 1 : Spectre decale $|X_k|$ du Signal 1 : $s_n = \sin(2\pi f_0 t_n)$")
plt.xlabel("Frequence (Hz)")
plt.ylabel("Spectre d'amplitude decale")
plt.grid(True)

#SIGNAL 2 : Tri(t) — signal triangulaire avec np.bartlett
#Te = 0.001 s, N = 1000

Te2 = 0.001
N2 = 1000
Fe2 = 1 / Te2    # 1000 Hz
tn2 = np.arange(N2) * Te2
sn2 = np.bartlett(N2)

Xk2 = np.fft.fft(sn2)
module_Xk2 = np.abs(Xk2)
module_Xk2_d = np.fft.fftshift(module_Xk2)
freq2 = np.fft.fftfreq(N2) * Fe2
freq2_d = np.fft.fftshift(freq2)

#Signal temporel
plt.figure(4)
plt.plot(tn2, sn2)
plt.title(r"Signal 2: Tri(t)  -  $T_e = 0.001$ s, $N = 1000$")
plt.xlabel(r"$t_n$ (s)")
plt.ylabel("Amplitude")
plt.grid(True)

#Spectre brut
plt.figure(5)
plt.plot(module_Xk2)
plt.title(r"Signal 2 : Spectre d'amplitude $|X_k|$ de Tri(t)")
plt.xlabel("Indice k")
plt.ylabel(r"$|X_k|$")
plt.grid(True)

#Spectre decale
plt.figure(6)
plt.plot(freq2_d, module_Xk2_d)
plt.title(r"Signal 2: Spectre decale $|X_k|$ de Tri(t)")
plt.xlabel("Frequence (Hz)")
plt.ylabel("Spectre d'amplitude decale")
plt.grid(True)

#SIGNAL 3 :2*sin(8*pi*f1*t)+5*sin(2*pi*f1*t)  f1 = 440 Hz
f1 = 440
Fe3 = 10 * f1
N3 = 500
tn3 = np.arange(N3) * (1 / Fe3)
sn3 = 2 * np.sin(8 * np.pi * f1 * tn3) + 5 * np.sin(2 * np.pi * f1 * tn3)

Xk3 = np.fft.fft(sn3)
module_Xk3 = np.abs(Xk3)
module_Xk3_d = np.fft.fftshift(module_Xk3)
freq3 = np.fft.fftfreq(N3) * Fe3
freq3_d = np.fft.fftshift(freq3)

#Signal temporel
plt.figure(7)
plt.plot(tn3, sn3)
plt.title(r"Signal 3: $2\sin(8\pi f_1 t) + 5\sin(2\pi f_1 t)$  -  $f_1 = 440$ Hz")
plt.xlabel(r"$t_n$ (s)")
plt.ylabel("Amplitude")
plt.grid(True)

#Spectre brut
plt.figure(8)
plt.plot(module_Xk3)
plt.title(r"Signal 3 : Spectre d'amplitude $|X_k|$ de $2\sin(8\pi f_1 t) + 5\sin(2\pi f_1 t)$ ")
plt.xlabel("Indice k")
plt.ylabel(r"$|X_k|$")
plt.grid(True)

#Spectre decale
plt.figure(9)
plt.plot(freq3_d, module_Xk3_d)
plt.title(r"Signal 3 : Spectre decale $|X_k|$ de $2\sin(8\pi f_1 t) + 5\sin(2\pi f_1 t)$ ")
plt.xlabel("Frequence (Hz)")
plt.ylabel("Spectre d'amplitude decale")
plt.grid(True)

#SIGNAL 4 : sinc(pi*t)
Fe4 = 100
N4 = 500
tn4 = np.arange(N4) * (1 / Fe4)
sn4 = np.sinc(tn4)   # np.sinc(x) = sin(pi*x)/(pi*x) donc np.sinc(t) = sinc(pi*t)

Xk4 = np.fft.fft(sn4)
module_Xk4 = np.abs(Xk4)
module_Xk4_d = np.fft.fftshift(module_Xk4)
freq4 = np.fft.fftfreq(N4) * Fe4
freq4_d = np.fft.fftshift(freq4)

#Signal temporel
plt.figure(10)
plt.plot(tn4, sn4)
plt.title(r"Signal 4 : $\mathrm{sinc}(\pi t)$")
plt.xlabel(r"$t_n$ (s)")
plt.ylabel("Amplitude")
plt.grid(True)

#Spectre brut
plt.figure(11)
plt.plot(module_Xk4)
plt.title(r"Signal 4 : Spectre d'amplitude $|X_k|$ de $\mathrm{sinc}(\pi t)$")
plt.xlabel("Indice k")
plt.ylabel(r"$|X_k|$")
plt.grid(True)

#Spectre decale
plt.figure(12)
plt.plot(freq4_d, module_Xk4_d)
plt.title(r"Signal 4: Spectre decale $|X_k|$ de $\mathrm{sinc}(\pi t)$")
plt.xlabel("Frequence (Hz)")
plt.ylabel("Spectre d'amplitude decale")
plt.grid(True)

#Affichage simultane de toutes les fenetres
plt.show()
