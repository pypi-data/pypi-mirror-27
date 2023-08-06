plot_path = '<OUTPUT PATH WHERE PLOTS ARE WRITTEN>'

import os

import beatboxtestbed.plotting as p
import beatboxtestbed.helpers as h

import boxmox

import chemspectranslator
translator = chemspectranslator.Translator()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if not os.path.isdir(plot_path):
    os.makedirs(plot_path)

# shortcut to save figures
saveFigure = lambda f, n: f.savefig(os.path.join(plot_path, n + ".pdf"))

# Figure 3 (unofficial function)
archive_path = h.get_archive_path('NO2nc')

fig = p._regime(archive_path, 'MOZART_T1'); saveFigure(fig, 'fig3_regime'); plt.close()

# Figure 4
archive_path = h.get_archive_path('NO2nc')

fig, axarr = plt.subplots(2, 2, sharex=True, dpi=300)
xlabel='Time in h'
ylabel='Concentration in ppbv'
fig = p.NRCR( archive_path, 'NO2',  translator, ax=axarr[0][0], fig=fig,
              xlabel="", ylabel=ylabel, title=r"NO$_2$", plabel="(a)")
fig = p.NRCR( archive_path, 'O3',   translator, ax=axarr[1][0], fig=fig,
              xlabel=xlabel, ylabel=ylabel, title=r"O$_3$", plabel="(b)")
fig = p.NRCR( archive_path, 'CH2O', translator, ax=axarr[0][1], fig=fig,
              xlabel="", ylabel="", title=r"CH$_2$O", plabel="(c)")
axarr[0][1].legend(loc='best', fontsize='x-small')
fig = p.NRCR( archive_path, 'OH',   translator, ax=axarr[1][1], fig=fig,
              xlabel=xlabel, ylabel="", title=r"OH", plabel="(d)")
saveFigure(fig, 'fig4_NRCR')
plt.tight_layout()
plt.close()

# Figure 5, 6
for exp in [ 'NO2', 'CH2O' ]:
    concies = {}
    for run in [ exp + 'nc', exp + 'ac' ]:
        concies[run] = {}
        archive_path = h.get_archive_path(run)
        for spec in [ 'NO2', 'O3', 'CH2O', 'OH' ]:
            concies[run][spec] = h.read_conc_cycling( translator, archive_path, spec )
#
    fig, axarr = plt.subplots(4, 2, sharex=True, figsize=[8.0, 11.0], dpi=300)
#
    xlabel='Time in h'
    ylabel='Concentration in ppbv'
#
    run = exp + 'nc'
    archive_path = h.get_archive_path(run)
    fig = p.cycling( translator, archive_path, 'NO2', conc=concies[run]['NO2'],
                     ax=axarr[0][0], fig=fig, plot_legend=('NO2' == exp),
                     xlabel="", ylabel=ylabel, title=r'NO$_2$', plabel='(a)')
    fig = p.cycling( translator, archive_path, 'O3', conc=concies[run]['O3'],
                     ax=axarr[1][0], fig=fig, plot_legend=('O3' == exp),
                     xlabel="", ylabel=ylabel, title=r'O$_3$', plabel='(b)')
    fig = p.cycling( translator, archive_path, 'CH2O', conc=concies[run]['CH2O'],
                     ax=axarr[2][0], fig=fig, plot_legend=('CH2O' == exp),
                     xlabel="", ylabel=ylabel, title=r'CH$_2$O', plabel='(c)')
    fig = p.cycling( translator, archive_path, 'OH', conc=concies[run]['OH'],
                     ax=axarr[3][0], fig=fig, plot_legend=('OH' == exp),
                     xlabel=xlabel, ylabel=ylabel, title=r'OH', plabel='(d)')
#
    run = exp + 'ac'
    archive_path = h.get_archive_path(run)
    fig = p.cycling( translator, archive_path, 'NO2', conc=concies[run]['NO2'],
                     ax=axarr[0][1], fig=fig, plot_legend=False,
                     xlabel="", ylabel="", title=r'NO$_2$', plabel='(e)')
    fig = p.cycling( translator, archive_path, 'O3', conc=concies[run]['O3'],
                     ax=axarr[1][1], fig=fig, plot_legend=False,
                     xlabel="", ylabel="", title=r'O$_3$', plabel='(f)')
    fig = p.cycling( translator, archive_path, 'CH2O', conc=concies[run]['CH2O'],
                     ax=axarr[2][1], fig=fig, plot_legend=False,
                     xlabel="", ylabel="", title=r'CH$_2$O', plabel='(g)')
    fig = p.cycling( translator, archive_path, 'OH', conc=concies[run]['OH'],
                     ax=axarr[3][1], fig=fig, plot_legend=False,
                     xlabel=xlabel, ylabel="", title=r'OH', plabel='(h)')
#
    niceSpec = exp
    if exp == 'CH2O':
        niceSpec = 'CH$_2$O'
#
    if exp == 'NO2':
        niceSpec = 'NO$_2$'
#
    plt.text(0.3, 0.98, r"Only " + niceSpec + " inferred", fontsize=18,
             transform=fig.transFigure, horizontalalignment='center')
    plt.text(0.75, 0.98, r"Whole state vector inferred", fontsize=18,
             transform=fig.transFigure, horizontalalignment='center')
#
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.975])
    saveFigure(fig, 'fig56_cycling_' + exp)
    plt.close()


# Figure 7
fig = plt.figure(figsize=[8.0, 8.0], dpi=300)
axarr = []
axarr.append(plt.subplot2grid((4, 12), (0, 0), colspan=11, rowspan=1))
axarr.append(plt.subplot2grid((4, 12), (1, 0), colspan=11, rowspan=1, sharex=axarr[0]))
axarr.append(plt.subplot2grid((4, 12), (0, 11), rowspan=2))
archive_path = h.get_archive_path('NO2ac')
fig = p.sensitivities(archive_path, fig=fig, axarr=axarr, abs_max=100.0)
axarr[0].set_title(r'(a) NO$_2$ assimilation')
axarr = []
axarr.append(plt.subplot2grid((4, 12), (2, 0), colspan=11, rowspan=1))
axarr.append(plt.subplot2grid((4, 12), (3, 0), colspan=11, rowspan=1, sharex=axarr[0]))
axarr.append(plt.subplot2grid((4, 12), (2, 11), rowspan=2))
archive_path = h.get_archive_path('CH2Oac')
fig = p.sensitivities(archive_path, fig=fig, axarr=axarr, abs_max=100.0)
axarr[0].set_title(r'(b) CH$_2$O assimilation')
plt.tight_layout()
saveFigure(fig, 'fig7_sensitivities')
plt.close()

# Figure 8
run   = 'CH2Oac'
cycle = 9
archive_path = h.get_archive_path(run)
beatbox_result_path = os.path.join(archive_path, 'fcst_' + str(cycle), 'BEATBOX.p')
fig = plt.figure(figsize=[8.0, 8.0], dpi=300)
axarr = []
axarr.append(plt.subplot2grid((2, 2), (0, 0)))
axarr.append(plt.subplot2grid((2, 2), (0, 1)))
axarr.append(plt.subplot2grid((2, 2), (1, 0)))
axarr.append(plt.subplot2grid((2, 2), (1, 1)))
fig = p.scatter( beatbox_result_path, fig=fig, axarr=axarr, plabels=['(a)', '(b)', '(c)', '(d)'] )
saveFigure(fig, 'fig8_tracer_tracer_' + run + '_' + str(cycle))
plt.tight_layout()
plt.close()

# Figure 9
run   = 'CH2Oac'
cycle = 9
archive_path = os.path.join(h.get_archive_path(run), 'fcst_' + str(cycle))

nr  = boxmox.ExperimentFromExistingRun( os.path.join(archive_path, 'MCMv3_3', 'output') )
cr  = boxmox.ExperimentFromExistingRun( os.path.join(archive_path, 'MOZART_T1', 'output'), filename="25EN")
en  = boxmox.ExperimentFromExistingRun( os.path.join(archive_path, 'MOZART_T1', 'output'), filename="25AR_ens")
hyb = boxmox.ExperimentFromExistingRun( os.path.join(archive_path, 'MOZART_T1', 'output'), filename="25AR_hyb")

moz_flx_lbls = {
                'CH3OH + OH --> VOC_OH + CH2O + HO2':       { "label": r'CH$_3$OH + OH -> CH$_2$O + HO$_2$',                "color": 'cornflowerblue' },
                'CH2O + OH --> VOC_OH + CO + HO2 + H2O':    { "label": r'CH$_2$O + OH -> CO + HO$_2$ + H$_2$O',             "color": 'orange'},
                'CH2O --> CO + 2 HO2':                      { "label": r'CH$_2$O -> CO + 2 HO$_2$',                         "color": 'green'},
                'CH2O --> H2 + CO':                         { "label": r'CH$_2$O -> H$_2$ + CO',                            "color": 'red'},
                'NO + CH3O2 --> RO2_NO + CH2O + NO2 + HO2': { "label": r'NO + CH$_3$O$_2$ -> CH$_2$O + NO$_2$ + HO$_2$',    "color": 'mediumpurple'}
                }

mcm_flx_lbls = {
                'CH3OH + OH --> HCHO + HO2':                { "label": r'CH$_3$OH + OH -> CH$_2$O + HO$_2$',                "color": 'cornflowerblue' },
                'CH3O --> HCHO + HO2':                      { "label": r'CH$_3$O -> CH$_2$O + HO$_2$',                      "color": 'orange'},
                'HCHO --> CO + 2 HO2':                      { "label": r'CH$_2$O -> CO + 2 HO$_2$',                         "color": 'green'},
                'HCHO + OH --> CO + HO2':                   { "label": r'CH$_2$O + OH -> CO + HO$_2$',                      "color": 'red'},
                'HCHO --> H2 + CO':                         { "label": r'CH$_2$O -> H$_2$ + CO',                            "color": 'mediumpurple'}
                }

ylims = ( -0.4, 0.7 )

fig = plt.figure(figsize=[8.0, 10.0], dpi=300)
axarr = []
axarr.append(plt.subplot2grid((3, 2), (0, 0)))
axarr.append(plt.subplot2grid((3, 2), (0, 1)))
axarr.append(plt.subplot2grid((3, 2), (1, 0)))
axarr.append(plt.subplot2grid((3, 2), (1, 1)))
axarr.append(plt.subplot2grid((3, 2), (2, 0)))
nr.plotter.fluxes('HCHO', fig=fig, ax=axarr[0], plabel="(a)", xlabel="", ylim=ylims,
                  plot_netflux=False, plot_xaxlabels=False, flx_labels=mcm_flx_lbls)
axarr[0].set_title(r"NR (MCM v3.3)")
cr.plotter.fluxes('CH2O', fig=fig, ax=axarr[1], plabel="(b)", xlabel="", ylabel="", ylim=ylims,
                  plot_netflux=False, plot_xaxlabels=False, flx_labels=moz_flx_lbls)
axarr[1].set_title(r"EN (MOZART-4)")
en.plotter.fluxes('CH2O', fig=fig, ax=axarr[2], plabel="(c)", xlabel="", ylim=ylims,
                  plot_netflux=False, plot_xaxlabels=False, flx_labels=moz_flx_lbls)
axarr[2].set_title(r"AR_ens (MOZART-4)")
hyb.plotter.fluxes('CH2O', fig=fig, ax=axarr[3], plabel="(d)", ylabel="", ylim=ylims,
                   plot_netflux=False, flx_labels=moz_flx_lbls)
axarr[3].set_title("AR_hyb (MOZART-4)")

p._net_fluxes({ 'NR': 'HCHO'  , 'EN': 'CH2O'   , 'AR_ens': 'CH2O'    , 'AR_hyb': 'CH2O'   },
              { 'NR': nr      , 'EN': cr       , 'AR_ens': en        , 'AR_hyb': hyb      },
              { 'NR': 'black' , 'EN': 'red'    , 'AR_ens': 'green'   , 'AR_hyb': 'blue'   },
              fig=fig, ax=axarr[4], plabel="(e)", scale_factor=3600.0*1000.0, ylim= ( -0.2, 0.1 ) )

saveFigure(fig, 'fig9_fluxes_CH2O')
plt.tight_layout()
plt.close()
