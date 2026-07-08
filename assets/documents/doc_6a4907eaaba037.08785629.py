"""
Projet TTS - Conception de filtre numerique
Filtre passe-bande RII (IIR), methode Chebyshev de type I
INGC1 2025-2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sounddevice as sd
import os
import pathlib

plt.ion()  # toutes les figures s'affichent en meme temps 

AUDIO_REEL_PATH = None # METTRE LE CHEMIN DU FICHIER AUDIO  

# 1. GABARIT DU FILTRE

Fe = 8000.0
fp1, fp2 = 300.0, 3400.0
fa1, fa2 = 150.0, 3700.0
Ap = 1.0
Aa = 40.0

print("=" * 70)
print("1. GABARIT DU FILTRE")
print("=" * 70)
print(f"Fe  = {Fe} Hz")
print(f"Bande passante  : [{fp1}, {fp2}] Hz  (Ap = {Ap} dB)")
print(f"Bande attenuee  : ]0,{fa1}] U [{fa2}, Fe/2] Hz  (Aa = {Aa} dB)")


# 2. SYNTHESE DU FILTRE

print("\n" + "=" * 70)
print("2. SYNTHESE - ETAPES DETAILLEES")
print("=" * 70)


def prewarp(f, Fe):
    return 2 * Fe * np.tan(np.pi * f / Fe)


Wp1, Wp2 = prewarp(fp1, Fe), prewarp(fp2, Fe)
Wa1, Wa2 = prewarp(fa1, Fe), prewarp(fa2, Fe)
print("\n-- Etape 1 : pre-distorsion bilineaire --")
print(f"Omega_p1 = {Wp1:10.2f} rad/s   (fp1 = {fp1} Hz)")
print(f"Omega_p2 = {Wp2:10.2f} rad/s   (fp2 = {fp2} Hz)")
print(f"Omega_a1 = {Wa1:10.2f} rad/s   (fa1 = {fa1} Hz)")
print(f"Omega_a2 = {Wa2:10.2f} rad/s   (fa2 = {fa2} Hz)")

W0 = np.sqrt(Wp1 * Wp2)
B  = Wp2 - Wp1
print("\n-- Etape 2 : transformation passe-bande -> passe-bas normalise --")
print(f"Omega_0 (frequence centrale) = {W0:.2f} rad/s")
print(f"B (largeur de bande)         = {B:.2f} rad/s")


def to_lowpass(W, W0, B):
    return abs((W ** 2 - W0 ** 2) / (B * W))


Wls1 = to_lowpass(Wa1, W0, B)
Wls2 = to_lowpass(Wa2, W0, B)
Wls  = min(Wls1, Wls2)
print(f"Omega_a1 transformee (LP) = {Wls1:.4f}")
print(f"Omega_a2 transformee (LP) = {Wls2:.4f}")
print(f"-> Omega_s retenue = {Wls:.4f}  (Omega_p = 1 par construction)")

print("\n-- Etape 3 : ordre du filtre --")
eps     = np.sqrt(10 ** (Ap / 10) - 1)
ratio   = np.sqrt((10 ** (Aa / 10) - 1) / (10 ** (Ap / 10) - 1))
N_exact = np.arccosh(ratio) / np.arccosh(Wls)
print(f"epsilon = {eps:.4f}")
print(f"N (calcul exact) = {N_exact:.3f}  ->  N retenu = {int(np.ceil(N_exact))}")

print("\n-- Etape 4 : coefficients --")
N, Wn = signal.cheb1ord([fp1, fp2], [fa1, fa2], Ap, Aa, fs=Fe)
print(f"Ordre prototype N = {N},  ordre filtre numerique 2N = {2*N}")

b, a = signal.cheby1(N, Ap, Wn, btype="bandpass", fs=Fe)
sos  = signal.cheby1(N, Ap, Wn, btype="bandpass", fs=Fe, output="sos")

print(f"\nCoefficients a (denominateur) :")
print(np.round(a, 6))
print(f"\nCoefficients b (numerateur) :")
print(np.round(b, 6))

print(f"\nDecomposition en {sos.shape[0]} cellules biquadratiques :")
for i, section in enumerate(sos, 1):
    b0, b1, b2, a0, a1, a2 = section
    print(f"  Cellule {i}: H{i}(z) = ({b0:.6f} + {b1:.6f}z^-1 + {b2:.6f}z^-2) / "
          f"(1 + {a1:.6f}z^-1 + {a2:.6f}z^-2)")

z, p, k = signal.tf2zpk(b, a)
print(f"\nStabilite : module max des poles = {np.max(np.abs(p)):.4f} (< 1 => stable)")


# 3. FIGURE - REPONSE EN FREQUENCE + POLES/ZEROS

w, h   = signal.freqz(b, a, worN=4000, fs=Fe)
H_db   = 20 * np.log10(np.abs(h) + 1e-12)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ax = axes[0]
ax.plot(w, H_db, color="#1f6feb", linewidth=1.8, label="Reponse |H(f)| (dB)")
ax.axhspan(-Aa-30, -Aa, xmin=0,            xmax=fa1/(Fe/2), color="red",   alpha=0.12)
ax.axhspan(-Aa-30, -Aa, xmin=fa2/(Fe/2),   xmax=1,          color="red",   alpha=0.12)
ax.axhspan(0, 20,       xmin=fp1/(Fe/2),   xmax=fp2/(Fe/2), color="green", alpha=0.06)
ax.axhline(0,   color="gray",  linewidth=0.6)
ax.axhline(-Ap, color="green", linestyle="--", linewidth=1.2, label=f"-Ap = -{Ap} dB")
ax.axhline(-Aa, color="red",   linestyle="--", linewidth=1.2, label=f"-Aa = -{Aa} dB")
for f in [fp1, fp2]: ax.axvline(f, color="green", linestyle=":", linewidth=1)
for f in [fa1, fa2]: ax.axvline(f, color="red",   linestyle=":", linewidth=1)
ax.set_xlim(0, Fe/2); ax.set_ylim(-80, 5)
ax.set_xlabel("Frequence (Hz)"); ax.set_ylabel("Amplitude (dB)")
ax.set_title(f"Reponse en frequence - Passe-bande Chebyshev I (N={N}, ordre={2*N})")
ax.legend(loc="lower center", fontsize=8); ax.grid(alpha=0.3)

ax2 = axes[1]
theta = np.linspace(0, 2*np.pi, 200)
ax2.plot(np.cos(theta), np.sin(theta), color="gray", linewidth=1)
ax2.scatter(p.real, p.imag, marker="x", color="red",  s=80, label="Poles")
ax2.scatter(z.real, z.imag, marker="o", facecolors="none", edgecolors="blue", s=80, label="Zeros")
ax2.axhline(0, color="gray", linewidth=0.5); ax2.axvline(0, color="gray", linewidth=0.5)
ax2.set_xlim(-1.3, 1.3); ax2.set_ylim(-1.3, 1.3); ax2.set_aspect("equal")
ax2.set_title("Plan des poles et zeros")
ax2.legend(loc="upper right", fontsize=8); ax2.grid(alpha=0.3)

plt.pause(0.01)


# 4. SIMULATION SUR SIGNAL THEORIQUE BRUITE

print("\n" + "=" * 70)
print("3. SIMULATION - SIGNAL THEORIQUE BRUITE")
print("=" * 70)

duree = 0.05          # duree de la simulation (spectres + graphiques)
t     = np.arange(0, duree, 1/Fe)

signal_utile = np.sin(2 * np.pi * 1000.0 * t)
parasite_bf  = 0.6 * np.sin(2 * np.pi * 60.0  * t)
parasite_hf  = 0.5 * np.sin(2 * np.pi * 4500.0 * t)
np.random.seed(42)
bruit_blanc  = 0.25 * np.random.randn(len(t))

x_theorique  = signal_utile + parasite_bf + parasite_hf + bruit_blanc
y_theorique  = signal.sosfiltfilt(sos, x_theorique)


def snr_db(sig_ref, bruit):
    return 10 * np.log10(np.sum(sig_ref**2) / (np.sum(bruit**2) + 1e-12))


print(f"SNR avant filtrage : {snr_db(signal_utile, x_theorique - signal_utile):.2f} dB")
print(f"SNR apres filtrage : {snr_db(signal_utile, y_theorique - signal_utile):.2f} dB")


def spectre(x, Fe):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1/Fe)
    return f, 20*np.log10(np.abs(X) + 1e-12)


n_aff = int(0.01 * Fe)
fig, axes = plt.subplots(2, 2, figsize=(13, 8))
axes[0,0].plot(t[:n_aff]*1000, x_theorique[:n_aff], color="#d62728")
axes[0,0].set_title("Signal bruite - domaine temporel (avant filtrage)")
axes[0,0].set_xlabel("Temps (ms)"); axes[0,0].grid(alpha=0.3)

axes[0,1].plot(t[:n_aff]*1000, y_theorique[:n_aff], color="#2ca02c")
axes[0,1].set_title("Signal filtre - domaine temporel (apres filtrage)")
axes[0,1].set_xlabel("Temps (ms)"); axes[0,1].grid(alpha=0.3)

f1, X1 = spectre(x_theorique, Fe)
f2, X2 = spectre(y_theorique, Fe)
axes[1,0].plot(f1, X1, color="#d62728")
axes[1,0].set_title("Spectre avant filtrage")
axes[1,0].set_xlabel("Frequence (Hz)"); axes[1,0].set_xlim(0, Fe/2); axes[1,0].grid(alpha=0.3)

axes[1,1].plot(f2, X2, color="#2ca02c")
axes[1,1].set_title("Spectre apres filtrage")
axes[1,1].set_xlabel("Frequence (Hz)"); axes[1,1].set_xlim(0, Fe/2); axes[1,1].grid(alpha=0.3)

plt.tight_layout()
plt.pause(0.01)


# 5. APPLICATION SUR SIGNAL REEL + LECTURE AUDIO

print("\n" + "=" * 70)
print("4. APPLICATION - SIGNAL REEL (VOIX TELEPHONIQUE)")
print("=" * 70)

if AUDIO_REEL_PATH is not None and os.path.exists(AUDIO_REEL_PATH):
    Fe_real, x_real = wavfile.read(AUDIO_REEL_PATH)
    x_real = x_real.astype(float)
    if x_real.ndim == 2:
        print("Stereo detecte -> conversion mono")
        x_real = x_real.mean(axis=1)
    x_real /= np.max(np.abs(x_real))
    print(f"Son charge : {AUDIO_REEL_PATH}  (Fe={Fe_real} Hz, duree={len(x_real)/Fe_real:.1f}s)")
    if Fe_real != int(Fe):
        print(f"ATTENTION : Fe du fichier ({Fe_real} Hz) != Fe de conception ({int(Fe)} Hz)")
        print("Reechantillonnage en cours...")
        from scipy.signal import resample_poly
        from math import gcd
        g    = gcd(int(Fe), Fe_real)
        up   = int(Fe)  // g
        down = Fe_real  // g
        x_real  = resample_poly(x_real, up, down)
        Fe_real = int(Fe)
        print(f"Signal reechantillonne a {Fe_real} Hz — filtre applique correctement")
else:
    print("Fichier introuvable, generation d'un signal vocal synthetique.")
    t_v = np.arange(0, 1.0, 1/Fe)
    f0  = 120.0
    voix = sum(np.exp(-k/6) * np.sin(2*np.pi*f0*k*t_v) for k in range(1, 25))
    env  = 0.5 * (1 + np.sin(2*np.pi*2.5*t_v))
    voix *= env
    for fF in [500, 1500, 2500]:
        voix += 0.3 * np.sin(2*np.pi*fF*t_v) * env
    voix /= np.max(np.abs(voix))
    x_real  = voix + 0.4*np.sin(2*np.pi*50*t_v) + 0.3*np.sin(2*np.pi*4000*t_v) + 0.15*np.random.randn(len(t_v))
    Fe_real = int(Fe)

# --- Filtrage ---
y_real  = signal.sosfiltfilt(sos, x_real)
y_norm  = y_real / np.max(np.abs(y_real))

# --- Sauvegarde dans Telechargements ---
telechargements = pathlib.Path.home() / 'Downloads'
telechargements.mkdir(exist_ok=True)
chemin_sortie = telechargements / 'son_filtre.wav'
wavfile.write(str(chemin_sortie), int(Fe_real),
              (y_norm * 0.9 * 32767).astype(np.int16))
print(f'Son filtre sauvegarde -> {chemin_sortie}')

# --- Lecture du signal theorique (optionnel) ---
ECOUTER_THEORIQUE = True   # <<< mets False si tu ne veux pas ecouter le signal theorique

if ECOUTER_THEORIQUE:
    # Generation d un signal plus long uniquement pour l ecoute (3 secondes)
    # La simulation (graphiques + SNR) reste sur duree = 0.05 s
    duree_ecoute = 3.0
    t_ec = np.arange(0, duree_ecoute, 1/Fe)
    x_ec = (np.sin(2*np.pi*1000.0*t_ec)
           + 0.6*np.sin(2*np.pi*60.0*t_ec)
           + 0.5*np.sin(2*np.pi*4500.0*t_ec)
           + 0.25*np.random.randn(len(t_ec)))
    y_ec = signal.sosfiltfilt(sos, x_ec)
    print("Lecture du signal theorique ORIGINAL (bruite) — 3 secondes...")
    sd.play(x_ec.astype(np.float32), int(Fe))
    sd.wait()
    print("Lecture du signal theorique FILTRE (300-3400 Hz) — 3 secondes...")
    sd.play((y_ec / np.max(np.abs(y_ec))).astype(np.float32), int(Fe))
    sd.wait()

# --- Spectres ---
fig, axes = plt.subplots(2, 1, figsize=(11, 7))
f1r, X1r = spectre(x_real, Fe_real)
f2r, X2r = spectre(y_real, Fe_real)
axes[0].plot(f1r, X1r, color="#d62728", linewidth=0.9)
for fF in [fp1, fp2]: axes[0].axvline(fF, color="green", linestyle=":", linewidth=1)
axes[0].set_title("Signal reel - spectre AVANT filtrage")
axes[0].set_xlabel("Frequence (Hz)"); axes[0].set_xlim(0, Fe_real/2); axes[0].grid(alpha=0.3)

axes[1].plot(f2r, X2r, color="#2ca02c", linewidth=0.9)
for fF in [fp1, fp2]: axes[1].axvline(fF, color="green", linestyle=":", linewidth=1)
axes[1].set_title("Signal reel - spectre APRES filtrage passe-bande")
axes[1].set_xlabel("Frequence (Hz)"); axes[1].set_xlim(0, Fe_real/2); axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.ioff()
plt.show(block=True)  # garde toutes les figures ouvertes apres lecture audio

# --- Lecture audio ---
print("\nLecture du son ORIGINAL...")
sd.play(x_real, int(Fe_real))
sd.wait()

print("Lecture du son FILTRE (300-3400 Hz)...")
sd.play(y_norm, int(Fe_real))
sd.wait()

print("\nTERMINE.")
