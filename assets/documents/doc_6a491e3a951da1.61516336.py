"""
ELOLA Payié Mariane

TP : Détection DTMF par Transformée de Fourier Discrète
Étapes :
  1. Charger un signal DTMF (.wav)
  2. Tracer et jouer le signal temporel
  3. Calculer et afficher le spectre (TFD)
  4. Identifier graphiquement les fréquences DTMF
  5. Déduire la touche correspondante
"""
import numpy as np
import soundfile as sf
import sounddevice as sd
from matplotlib import pyplot as plt
#TABLE DTMF DE RÉFÉRENCE
DTMF_TABLE = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
}
LOW_FREQS  = [697, 770, 852, 941]   # fréquences lignes (fl)
HIGH_FREQS = [1209, 1336, 1477, 1633]  # fréquences colonnes (fc)
# 1. CHARGEMENT DU SIGNAL
FICHIER = 'son_c.wav'   # ← modifier ici pour changer de son
son, Fe = sf.read(FICHIER)
N = son.shape[0]
print(f"Fichier                  : {FICHIER}")
print(f"Nb d'échantillons        : {N}")
print(f"Fréq. échantillonnage Fe : {Fe} Hz")
print(f"Durée                    : {N/Fe:.3f} s")
# Passage en mono si stéréo
if son.ndim > 1:
    signal = son[:, 0]
    print("Mode                  : stéréo → canal 0 utilisé")
else:
    signal = son
    print("Mode                     : mono")

# 2. SIGNAL TEMPOREL
temps = np.arange(N) / Fe

plt.figure(1, figsize=(10, 3))
plt.plot(temps, signal, color='steelblue')
plt.title(f'Signal DTMF temporel — {FICHIER}')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
# Lecture audio 
print("\nLecture du signal audio...")
sd.play(son, Fe)
sd.wait()

# 3. CALCUL DE LA TFD
tfd_son = np.fft.fft(signal)
freq    = np.fft.fftfreq(N) * Fe          # axe fréquentiel complet
module  = np.abs(tfd_son) / Fe            # module normalisé
phase   = np.angle(tfd_son)               # phase en radians
# Spectre centré (fftshift)
freq_c   = np.fft.fftshift(freq)
module_c = np.fft.fftshift(module)
phase_c  = np.fft.fftshift(phase)

#Figure 2 : Module 
plt.figure(2, figsize=(10, 4))
plt.plot(freq_c, module_c, color='darkorange', label='Voie 0')
plt.title('Module de la T.F.D.')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude')
plt.xlim(-2500, 2500)
plt.grid(True)
plt.legend()
plt.tight_layout()

#Figure 3 : Phase
plt.figure(3, figsize=(10, 4))
plt.plot(freq_c, phase_c, color='seagreen', label='Voie 0')
plt.title('Phase de la T.F.D.')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Phase (rad)')
plt.xlim(-2500, 2500)
plt.grid(True)
plt.legend()
plt.tight_layout()

# 4. IDENTIFICATION GRAPHIQUE DES FRÉQUENCES (spectre unilatéral avec repères DTMF)
# Spectre unilatéral (fréquences positives uniquement)
mask     = freq > 0
freq_pos = freq[mask]
mag_pos  = module[mask]
def pic_dominant(liste_freq, freqs, magnitudes, fenetre=30):
    """Retourne la fréquence DTMF la plus énergétique dans la liste."""
    best_f, best_m = None, 0
    for f in liste_freq:
        w = (freqs >= f - fenetre) & (freqs <= f + fenetre)
        if w.any():
            m = magnitudes[w].max()
            if m > best_m:
                best_m, best_f = m, f
    return best_f, best_m
fl_det, ml = pic_dominant(LOW_FREQS,  freq_pos, mag_pos)
fh_det, mh = pic_dominant(HIGH_FREQS, freq_pos, mag_pos)

#Figure 4 : Spectre unilatéral annoté 
plt.figure(4, figsize=(11, 5))
plt.plot(freq_pos, mag_pos, color='royalblue', linewidth=0.8, label='Spectre unilatéral')
# Repères des fréquences DTMF
for f in LOW_FREQS:
    couleur = 'red' if f == fl_det else 'salmon'
    plt.axvline(f, color=couleur, linestyle='--', linewidth=0.9, alpha=0.7)
    plt.text(f, mag_pos.max() * 1.02, f'{f}', ha='center', fontsize=7, color=couleur)

for f in HIGH_FREQS:
    couleur = 'darkgreen' if f == fh_det else 'lightgreen'
    plt.axvline(f, color=couleur, linestyle='--', linewidth=0.9, alpha=0.7)
    plt.text(f, mag_pos.max() * 1.05, f'{f}', ha='center', fontsize=7, color=couleur)
# Marquer les pics détectés
plt.annotate(f'fl = {fl_det} Hz',
             xy=(fl_det, ml), xytext=(fl_det + 80, ml * 0.9),
             arrowprops=dict(arrowstyle='->', color='red'), color='red', fontsize=9)
plt.annotate(f'fc = {fh_det} Hz',
             xy=(fh_det, mh), xytext=(fh_det + 80, mh * 0.9),
             arrowprops=dict(arrowstyle='->', color='darkgreen'), color='darkgreen', fontsize=9)

plt.title(f'Spectre TFD — Identification des fréquences DTMF\n(rouge = fréquence ligne fl et vert = fréquence colonne fc)')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0, 2200)
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()

# 5. DÉDUCTION DE LA TOUCHE
touche = DTMF_TABLE.get((fl_det, fh_det), '?')
print("\n─── Résultat de la détection DTMF ───")
print(f"  Fréquence basse  fl = {fl_det} Hz")
print(f"  Fréquence haute  fc = {fh_det} Hz")
print(f"  ➜  Touche détectée : [{touche}]")

#Affichage
plt.show()
