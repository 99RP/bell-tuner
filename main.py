import math
import numpy as np
import matplotlib.pyplot as plt

def main():
    # bell length (cm) and resonant frequencies (hz)
    data = [
        (20, [472, 618]),
        (30, [412, 580]),
    ]

    lengths = np.array([d[0] for d in data])
    freq1 = np.array([d[1][0] for d in data])
    freq2 = np.array([d[1][1] for d in data])

    # Linear fit for each frequency
    fit1 = np.polyfit(lengths, freq1, 1)
    fit2 = np.polyfit(lengths, freq2, 1)

    # Extrapolate to a wider range
    extrap_lengths = np.linspace(10, 80, 1000)
    extrap_freq1 = np.polyval(fit1, extrap_lengths)
    extrap_freq2 = np.polyval(fit2, extrap_lengths)

    # Harmonic ratios and their orders
    harmonic_ratios = {
        "1st (1/2)": (1/2, 'red'),
        "2nd (1/3)": (1/3, 'green'),
        "2nd (2/3)": (2/3, 'green'),
        "3rd (1/4)": (1/4, 'blue'),
        "3rd (3/4)": (3/4, 'blue'),
    }
    tolerance = 0.001  # 0.5% tolerance

    plt.plot(lengths, freq1, 'o', label='Freq1 Data')
    plt.plot(lengths, freq2, 'o', label='Freq2 Data')
    plt.plot(extrap_lengths, extrap_freq1, '-', label='Freq1 Extrapolated')
    plt.plot(extrap_lengths, extrap_freq2, '-', label='Freq2 Extrapolated')

    ratio = extrap_freq2 / extrap_freq1
    inv_ratio = extrap_freq1 / extrap_freq2

    for harmonic_label, (target_ratio, color) in harmonic_ratios.items():
        # harmonic_indices = np.where(np.abs(ratio - 3/2) < tolerance)[0]
        harmonic_indices = np.where(
            (np.abs(ratio - target_ratio) < tolerance) | 
            (np.abs(inv_ratio - target_ratio) < tolerance)
        )[0]
        harmonic_freq1 = extrap_freq1[harmonic_indices]
        harmonic_freq2 = extrap_freq2[harmonic_indices]
        harmonic_lengths = extrap_lengths[harmonic_indices]

        if len(harmonic_lengths) > 0:
            l = (harmonic_lengths[-1] + harmonic_lengths[0]) / 2
            # harmonic_freq = (harmonic_indices[-1] + harmonic_indices[0]) / 2
            f1 = (harmonic_freq1[-1] + harmonic_freq1[0]) / 2
            f2 = (harmonic_freq2[-1] + harmonic_freq2[0]) / 2

            plt.axvline(x=l, color=color, linestyle='-', alpha=0.7, linewidth=1, label=f"{harmonic_label} {l:.1f} cm, {f1:.0f} and {f2:.0f} Hz")

    plt.xlabel('Bell Length (cm)')
    plt.ylabel('Resonant Frequency (Hz)')
    plt.legend()
    plt.title('Linear Extrapolation of Bell Resonant Frequencies with Harmonic Lengths')
    plt.show()

if __name__ == "__main__":
    main()