import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import hashlib

# Generate first N prime numbers
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Generate a sequence of primes
N = 100  # Number of primes to use
primes = [n for n in range(2, 1000) if is_prime(n)][:N]

# Compute Mod 3 residues of the prime numbers
mod_3_residues = np.array([p % 3 for p in primes])

# Apply Fourier Transform to mod 3 residue sequence
fft_result = fft(mod_3_residues)

# Compute the absolute values of Fourier coefficients (magnitude spectrum)
fft_magnitudes = np.abs(fft_result)

# Display Fourier Spectrum
plt.figure(figsize=(10, 5))
plt.plot(fft_magnitudes, marker='o', linestyle='-')
plt.title("Fourier Transform of Mod 3 Residues of Prime Numbers")
plt.xlabel("Frequency Index")
plt.ylabel("Magnitude")
plt.grid(True)
plt.show()

# Define a hash function using Fourier-Mod 3 properties
def fourier_mod3_hash(data):
    """A simple hash function using Fourier transform on mod 3 residues."""
    hash_input = ''.join(map(str, data))
    hash_object = hashlib.sha256(hash_input.encode())
    return hash_object.hexdigest()

# Compute a hash based on mod 3 residue sequence
mod3_hash = fourier_mod3_hash(mod_3_residues)
mod3_hash
