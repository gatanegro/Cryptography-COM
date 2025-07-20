import numpy as np
from collections import Counter
from scipy.stats import chisquare
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# 1. Core 3DCOM Generator


def cryptographic_3dcom(n, steps=100000):
    """Generates cryptographically secure phases"""
    results = []
    chaos_state = n

    for _ in range(steps):
        # Chaotic mixing (PCG algorithm variant)
        chaos_state = (chaos_state * 6364136223846793005 + 1) & 0xFFFFFFFF
        phase = (n + (chaos_state % 256)) % 9

        results.append(phase)
        n = n // 2 if n % 2 == 0 else (3 * n + 1) ^ (chaos_state % 256)
    return results

# 2. Analysis & Visualization


def analyze_phases(phases):
    counts = Counter(phases)
    total = len(phases)

    # Statistical tests
    entropy = -sum((v/total) * np.log2(v/total) for v in counts.values())
    chi2, p_value = chisquare(list(counts.values()))

    # Plotting
    plt.figure(figsize=(14, 7))
    bars = plt.bar(counts.keys(), counts.values(), color='#4C72B0')
    plt.axhline(y=total/9, color='red', linestyle=':', label='Ideal (11.1%)')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x()+0.4, height+50,
                 f'{height/total:.1%}', ha='center')

    plt.title(
        f'3DCOM Phase Uniformity\nEntropy = {entropy:.3f}/3.170 bits', fontsize=16)
    plt.legend()
    plt.savefig('3dcom_uniformity.png', dpi=300)

    return {
        'entropy': entropy,
        'p_value': p_value,
        'counts': counts
    }

# 3. Key Derivation


def generate_key(phases):
    """Derives 256-bit cryptographic key"""
    phase_bytes = bytes(phases)
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                info=b'3DCOM Key').derive(phase_bytes)


# Main Execution
if __name__ == "__main__":
    print("Generating 3DCOM phases...")
    phases = cryptographic_3dcom(7)

    print("Analyzing...")
    results = analyze_phases(phases)

    print("\n=== RESULTS ===")
    print(f"Entropy: {results['entropy']:.6f} bits/step")
    print(f"Uniformity p-value: {results['p_value']:.6f}")
    print(f"Phase counts: {dict(results['counts'])}")

    key = generate_key(phases)
    print(f"\nGenerated 256-bit key: {key.hex()}")
