"""Efectos de sonido sintetizados aqui mismo (sin derechos de nadie).

tictac(dur)  reloj de cuenta atras con un latido grave de tension que crece
acierto()    «ding-ding» que sube: es VERDAD
fallo()      «moc-moc» grave que baja: es MITO
mezcla(dur, [(t, sonido), ...]) -> wav mono 48 kHz en un fichero
"""
import wave

import numpy as np

SR = 48000


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _env(dur, ataque, caida):
    t = _t(dur)
    return np.minimum(1, t / max(ataque, 1e-4)) * np.exp(-t / caida)


def golpe(freq, dur=0.09, caida=0.018, ruido=0.35):
    """Un golpe de reloj: tono corto + chasquido."""
    t = _t(dur)
    rng = np.random.default_rng(int(freq))
    s = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2.7 * t)
    s += ruido * rng.standard_normal(len(t)) * np.exp(-t / 0.004)
    return s * _env(dur, 0.0008, caida)


def latido(dur=0.35):
    """Pulso grave (tension)."""
    t = _t(dur)
    f = 62 * (1 + 0.15 * np.exp(-t / 0.05))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return s * _env(dur, 0.01, 0.12)


def tictac(dur, paso=0.5):
    """Tic-tac durante `dur` s; el ultimo segundo va el doble de rapido.
    El latido grave sube de volumen hasta el final."""
    out = np.zeros(int(dur * SR) + SR)
    t, k = 0.0, 0
    while t < dur - 0.05:
        g = golpe(2300 if k % 2 == 0 else 1600)
        i = int(t * SR)
        out[i:i + len(g)] += 0.55 * g
        if k % 2 == 0:
            lt = latido()
            out[i:i + len(lt)] += (0.35 + 0.5 * t / dur) * lt
        k += 1
        t += paso if t < dur - 1.0 else paso / 2
    return out[:int(dur * SR)]


def _nota(freq, dur, caida):
    t = _t(dur)
    s = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t)
         + 0.12 * np.sin(6 * np.pi * freq * t))
    return s * _env(dur, 0.004, caida)


def acierto():
    """Dos notas que suben (La5 -> Mi6), como una campanita."""
    out = np.zeros(int(1.0 * SR))
    for t0, f in ((0.0, 880.0), (0.11, 1318.5)):
        n = _nota(f, 0.85, 0.28)
        i = int(t0 * SR)
        out[i:i + len(n)] += 0.6 * n[:len(out) - i]
    return out


def _zumbido(freq, dur):
    t = _t(dur)
    s = sum(np.sin(2 * np.pi * freq * h * t) / h for h in range(1, 9))
    return s * np.minimum(1, t / 0.008) * np.minimum(1, (dur - t) / 0.03)


def fallo():
    """Dos zumbidos graves que bajan: «moc-moc»."""
    out = np.zeros(int(0.7 * SR))
    for t0, f in ((0.0, 196.0), (0.27, 147.0)):
        z = _zumbido(f, 0.22)
        i = int(t0 * SR)
        out[i:i + len(z)] += 0.35 * z
    return out


def mezcla(dur, sonidos, ruta):
    """Pone cada sonido en su momento y guarda el wav (pico a -3 dB)."""
    out = np.zeros(int(dur * SR) + SR)
    for t0, s in sonidos:
        i = int(t0 * SR)
        n = min(len(s), len(out) - i)
        out[i:i + n] += s[:n]
    out = out[:int(dur * SR)]
    pico = np.abs(out).max() or 1
    # +5 dB sobre -3 dB de pico y limitador suave: queda a unos -16 LUFS,
    # como los videos con voz, sin que nada sature
    out = out / pico * 10 ** (2 / 20)
    umbral = 0.55
    a = np.abs(out)
    sobra = np.maximum(a - umbral, 0)
    out = np.sign(out) * np.where(a > umbral, umbral + (0.89 - umbral) * np.tanh(sobra / (0.89 - umbral)), a)
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    return ruta
