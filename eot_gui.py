import eot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, RadioButtons, Button


e = 0.01671022                      # earth orbit eccentricity
orb_per = 365.25696                 # earth orbital period
peri_day = 3.0888                   # calendar day in January of perihelion (~3-5) (decimal/fractional format)
p_degs = 12.25                      # projection of the axis of the earth onto the plane of the orbit in degrees
axis_norm_degs = 23.4367            # angle between the earth's axis and the norm of the orbit

day_nums = np.arange(1.5, 366.5, 1)  # base calculation on noon UT of day

cal_dict = {1: 'Jan 1', 32: 'Feb 1', 60: 'Mar 1', 91: 'Apr 1', 121: 'May 1', 152: 'Jun 1',
            182: 'Jul 1', 213: 'Aug 1', 244: 'Sep 1', 274: 'Oct 1', 305: 'Nov 1', 335: 'Dec 1'}

scaling_on = False

fig = plt.figure(figsize=(10, 6), num='Equation of Time')
plt.subplots_adjust(top=.925, left=0.100, right=.950, wspace=0.1)
gs = GridSpec(22, 20, figure=fig)

eot_x = day_nums
eot_y = eot.eot_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
obl_y = eot.obl_gen(p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
ecc_y = eot.ecc_gen(e, p_degs, peri_day, orb_per, day_nums)
ax_eot = plt.subplot(gs.new_subplotspec((0, 0), colspan=9, rowspan=10))
ax_eot.set_title("Equation of Time")
ax_eot.minorticks_on()
ax_eot.grid(which='major', linestyle='-', linewidth=0.5, color='grey')
ax_eot.grid(which='minor', linestyle=':', linewidth=0.5, color='grey')
ax_eot.set_xlabel('Day')
ax_eot.set_ylabel('Minutes')
eot_line, = ax_eot.plot(eot_x, eot_y, 'k', linewidth=2, label='Equation of Time')
ecc_line, = ax_eot.plot(eot_x, ecc_y, 'b--', label='Eccentricity')
obl_line, = ax_eot.plot(eot_x, obl_y, 'g-.', label='Obliquity')
ax_eot.legend(loc='best', fontsize='small')
eot_ann_list = []

for d, dt_lbl in cal_dict.items():
    ann = ax_eot.annotate(dt_lbl, (eot_x[d - 1], eot_y[d - 1]), textcoords="offset points",
                          xytext=(-10, 10), ha='right', fontsize='small', color='red',
                          arrowprops=dict(arrowstyle="->", color='red'))
    eot_ann_list.append(ann)


day_nums = np.arange(1.5, 367.5, 1)  # base calculation on noon UT of day
min_x, dec_y = eot.analemma_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
ax_analemma = plt.subplot(gs.new_subplotspec((0, 12), colspan=9, rowspan=22))
ax_analemma.set_title("Analemma")
ax_analemma.minorticks_on()
ax_analemma.grid(which='major', linestyle='-', linewidth=0.5, color='grey')
ax_analemma.grid(which='minor', linestyle=':', linewidth=0.5, color='grey')
ax_analemma.set_xlabel('Minutes')
ax_analemma.set_ylabel('Angle')
analemma_line, = ax_analemma.plot(min_x, dec_y, 'k', lw=2)
analemma_ann_list = []

for d, dt_lbl in cal_dict.items():
    ann = ax_analemma.annotate(dt_lbl, (min_x[d - 1], dec_y[d - 1]), textcoords="offset points",
                               xytext=(-10, 10), ha='right', fontsize='small', color='red',
                               arrowprops=dict(arrowstyle="->", color='red'))
    analemma_ann_list.append(ann)


def update(val):
    global eot_ann_list, analemma_ann_list

    e = slider_e.val
    axis_norm_degs = slide_obl_deg.val
    p_degs = slide_sol_peri.val

    day_nums = np.arange(1.5, 366.5, 1)
    eot_x = day_nums
    eot_y = eot.eot_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
    obl_y = eot.obl_gen(p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
    ecc_y = eot.ecc_gen(e, p_degs, peri_day, orb_per, day_nums)
    eot_line.set_ydata(eot_y)
    ecc_line.set_ydata(ecc_y)
    obl_line.set_ydata(obl_y)

    for _, a in enumerate(eot_ann_list):
        a.remove()
    eot_ann_list[:] = []
    for d, dt_lbl in cal_dict.items():
        ann = ax_eot.annotate(dt_lbl, (eot_x[d - 1], eot_y[d - 1]), textcoords="offset points",
                              xytext=(-10, 10), ha='right', fontsize='small', color='red',
                              arrowprops=dict(arrowstyle="->", color='red'))
        eot_ann_list.append(ann)

    day_nums = np.arange(1.5, 367.5, 1)
    min_x, dec_y = eot.analemma_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_nums)
    analemma_line.set_ydata(dec_y)
    analemma_line.set_xdata(min_x)

    for _, a in enumerate(analemma_ann_list):
        a.remove()
    analemma_ann_list[:] = []
    for d, dt_lbl in cal_dict.items():
        ann = ax_analemma.annotate(dt_lbl, (min_x[d - 1], dec_y[d - 1]), textcoords="offset points",
                                   xytext=(-10, 10), ha='right', fontsize='small', color='red',
                                   arrowprops=dict(arrowstyle="->", color='red'))
        analemma_ann_list.append(ann)

    if scaling_on:
        xmin = min(eot_x)
        xmax = max(eot_x)
        ymin = min(eot_y + obl_y + ecc_y)
        ymax = max(eot_y + obl_y + ecc_y)
        if xmax != xmin:
            ax_eot.set_xlim(xmin - 0.1 * (xmax - xmin), xmax + 0.1 * (xmax - xmin))
        if ymax != ymin:
            ax_eot.set_ylim(ymin - 0.1 * (ymax - ymin), ymax + 0.1 * (ymax - ymin))
        xmin = min(min_x)
        xmax = max(min_x)
        ymin = min(dec_y)
        ymax = max(dec_y)
        if xmax != xmin:
            ax_analemma.set_xlim(xmin - 0.1 * (xmax - xmin), xmax + 0.1 * (xmax - xmin))
        if ymax != ymin:
            ax_analemma.set_ylim(ymin - 0.1 * (ymax - ymin), ymax + 0.1 * (ymax - ymin))

    fig.canvas.draw_idle()


def scale_update(val):
    global scaling_on

    if val == 'Auto Scaling On':
        scaling_on = True
        update(val)
    else:
        scaling_on = False


def reset(event):
    slider_e.reset()
    slide_obl_deg.reset()
    slide_sol_peri.reset()


ax_slider_e = plt.subplot(gs.new_subplotspec((13, 1), colspan=8, rowspan=1))
slider_e = Slider(ax_slider_e, 'Eccentricity', 0.00, 0.05, valinit=e, valfmt='%5.4f',
                  facecolor='blue', dragging=True)
slider_e.on_changed(update)

ax_slider_obl = plt.subplot(gs.new_subplotspec((14, 1), colspan=8, rowspan=1))
slide_obl_deg = Slider(ax_slider_obl, 'Obliquity (deg)', 0.0, 45.0, valinit=axis_norm_degs, valfmt='%4.2f',
                       facecolor='green', dragging=True)
slide_obl_deg.on_changed(update)

ax_slider_sol_peri = plt.subplot(gs.new_subplotspec((15, 1), colspan=8, rowspan=1))
slide_sol_peri = Slider(ax_slider_sol_peri, 'Solstice/Peri (deg)', 0.0, 120.0, valinit=p_degs, valfmt='%4.2f',
                        facecolor='orange', dragging=True)
slide_sol_peri.on_changed(update)

ax_radio_scale = plt.subplot(gs.new_subplotspec((17, 1), colspan=4, rowspan=5))
radio_scale = RadioButtons(ax_radio_scale, ('Auto Scaling On', 'Auto Scaling Off'), active=1, activecolor='black')
radio_scale.on_clicked(scale_update)

ax_reset = plt.subplot(gs.new_subplotspec((17, 6), colspan=2, rowspan=1))
reset_button = Button(ax_reset, 'Reset', color='lightgray', hovercolor='dimgray')
reset_button.on_clicked(reset)

plt.show()
