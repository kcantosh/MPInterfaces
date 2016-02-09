import os

from pymatgen.io.vasp.outputs import Vasprun

import matplotlib.pyplot as plt


def get_band_structures(directories):

    band_gaps = {}
    for directory in directories:
        os.chdir(directory)
        vasprun = Vasprun('vasprun.xml')
        band_gap = vasprun.get_band_structure().get_band_gap()

        transition = band_gap['transition'].split('-')

        if transition[0] == transition[1]:
            is_direct = True
        else:
            is_direct = False

        if band_gap['energy']:
            cbm = vasprun.get_band_structure().get_cbm()
            vbm = vasprun.get_band_structure().get_vbm()
            efermi = vasprun.efermi
            band_gaps[directory] = {'CBM': cbm, 'VBM': vbm,
                                    'Direct': is_direct, 'E_Fermi':efermi}
        else:
            band_gaps[directory] = False
        os.chdir('../')

    return band_gaps


def plot_band_alignments(band_gaps):

    ax = plt.figure(figsize=(16, 10)).gca()

    x_max = len(band_gaps)*1.625
    ax.set_xlim(0, x_max)

    x_ticklabels = []
    vbms = []
    for compound in band_gaps:
        vbms.append(band_gaps[compound]['VBM']['energy'])

    y_min = min(vbms) - 0.5

    i = 0
    for compound in band_gaps:
        x_ticklabels.append(compound)
        efermi = band_gaps[compound]['E_Fermi']
        cbm = band_gaps[compound]['CBM']['energy']  # - efermi?
        vbm = band_gaps[compound]['VBM']['energy']  # - efermi?
        if band_gaps[compound]['Direct']:
            linewidth = 5
        else:
            linewidth = 0

        ax.add_patch(plt.Rectangle((i, cbm), height=-cbm, width=0.8,
                                   facecolor="#002b80", linewidth=linewidth,
                                   edgecolor="#e68a00"))
        ax.add_patch(plt.Rectangle((i, y_min),
                                   height=(vbm - y_min), width=0.8,
                                   facecolor="#002b80", linewidth=linewidth,
                                   edgecolor="#e68a00"))

        i += 1

    ax.set_ylim(y_min, 0)

    ax.plot([0, i], [-1.9, -1.9], color='k', alpha=0.6, linewidth=4)
    ax.text(i*1.05, -1.94, r'$\mathrm{CO_2+\/e^-\/\rightarrow\/CO^-_2}$',
            size=20)

    ax.plot([0, i], [-0.61, -0.61], color='k', alpha=0.6, linewidth=4)
    ax.text(i*1.05, -0.7,
            r'$\mathrm{CO_2\/+\/2H^+\/+\/2e^-\/\rightarrow\/HCO_2H}$', size=20)

    ax.plot([0, i], [-0.53, -0.53], color='k', alpha=0.6, linewidth=4)
    ax.text(i*1.05, -0.59,
            r'$\mathrm{CO_2\/+\/2H^+\/+\/2e^-\/\rightarrow\/CO\/+\/H_2O}$',
            size=20)

    ax.plot([0, i], [-0.48, -0.48], color='k', alpha=0.6, linewidth=4)
    ax.text(i*1.05, -0.48,
            r'$\mathrm{CO_2\/+\/4H^+\/+\/4e^-\/\rightarrow\/HCHO\/+\/H_2O}$',
            size=20)

    ax.plot([0, i], [-0.38, -0.38], color='k', alpha=0.6, linewidth=4)
    ax.text(i*1.05, -0.37,
            r'$\mathrm{CO_2\/+\/6H^+\/+\/6e^-\/\rightarrow\/CH_3OH\/+\/H_2O}$',
            size=20)

    ax.plot([0, i], [-0.24, -0.24], color='k', alpha=0.6, linewidth=4)
    ax.text(i*1.05, -0.24,
            r'$\mathrm{CO_2\/+\/8H^+\/+\/8e^-\/\rightarrow\/CH_4\/+\/2H_2O}$',
            size=20)

    ax.set_xticks([n + 0.4 for n in range(i)])
    ax.set_xticklabels(x_ticklabels, family='serif', size=20, rotation=60)
    ax.set_yticklabels(ax.get_yticks(), family='serif', size=20)

    ax.add_patch(plt.Rectangle((i*1.1, y_min + (-y_min*0.15)), width=x_max*0.1,
                               height=(-y_min*0.1), facecolor='#002b80',
                               edgecolor='#e68a00', linewidth=5))
    ax.text(i*1.18, y_min*0.8, 'Direct', family='serif', color='w',
            size=20, horizontalalignment='center', verticalalignment='center')

    ax.add_patch(plt.Rectangle((i*1.1, y_min), width=x_max*0.1,
                               height=(-y_min*0.1), facecolor='#002b80',
                               linewidth=0))
    ax.text(i*1.18, y_min*0.95, 'Indirect', family='serif', size=20,
            color='w', horizontalalignment='center',
            verticalalignment='center')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    plt.savefig('band_alignments.pdf', transparent=True)

