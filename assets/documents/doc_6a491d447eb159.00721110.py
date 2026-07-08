import numpy as np
import soundfile as sf
import sounddevice as sd
from matplotlib import pyplot as plt
son, Fe = sf.read(r'C:\Users\HP\Documents\Audacity\tp2_son.wav')
N = son.shape[0]
print("Nombre d'échantillons : ", N)
print("Fréquence d'échantillonnage : ", Fe)
temps = np.arange(0,N)/Fe
plt.figure(1)
plt.plot(temps,son[ :,0],label='Voie 0')
plt.title('Signal audio wav')
plt.legend()
plt.grid(True)
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude (volt)')
#plot.show()
# Calcul de la TFD du son audio 
if son.ndim==1: # vérification du mode d’enregistrement de l’audio (mono ou  
# stéréo) 
    tfd_son = np.fft.fft(son) 
else: 
    tfd_son = np.fft.fft(son[:, 0])  
#Tracer du module du spectre de la TFD du signal temporel 
plt.figure(2) # initialisation figure N° 2 
freq = np.fft.fftfreq(N)*Fe # base de fréquence (abscisse) du spectre 
plt.plot(np.fft.fftshift(freq),np.fft.fftshift(np.abs(tfd_son).real/Fe),
label="Voie 0") 
plt.title('Module de la T.F.D.') 
plt.legend() 
plt.grid(True) 
plt.xlabel('Fréquence (Hz)') 
plt.ylabel('Amplitude (u.a.)') 
#Tracer de la phase du spectre du signal temporel 
plt.figure(3) 
plt.plot(np.fft.fftshift(freq),np.fft.fftshift(np.angle(tfd_son).real), 
label="Voie 0") 
plt.title('Phase de la T.F.D.') 
plt.legend() 
plt.grid(True) 
plt.xlabel('Fréquence (Hz)') 
plt.ylabel('Phase (rd)') 
plt.show()
