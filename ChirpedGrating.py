import klayout.db as db
import numpy as np
from datetime import date
today = date.today()

ly = db.Layout()

top = ly.create_cell('TOP')
layer0 = ly.layer(0, 0)
layer1 = ly.layer(1, 0)

grating_width = 500

heights = [-250, 0, 250]
periods = [0.353, 0.360, 0.368]
ffs = [0.7, 0.7, 0.7]

grating_x = 0
grating_y = 0

rotate90 = True

num_of_periods = round(grating_width / max(periods))

x_cen = []
xs = []
ys = []
n = 1

for p, f, h in zip(periods, ffs, heights):
    temp = np.arange(-num_of_periods/2 * p, (num_of_periods/2 * p) + p, p)
    x_cen.append(list(temp))
    
x_cen = list(np.asarray(x_cen).reshape(len(periods), -1).transpose())

for x_c in x_cen:
    x_c = list(x_c)
    temp_x = []
    temp_y = []
    for p, f, h, xc in zip(periods, ffs, heights, x_c):
        temp_x.append(xc - p/2)
        temp_y.append(h)

    for p, f, h, xc in zip(reversed(periods), reversed(ffs), reversed(heights), reversed(x_c)):
        temp_x.append(xc - p/2 + (p * (1-f)))
        temp_y.append(h)
    xs.append(temp_x)
    ys.append(temp_y)

for x, y in zip(xs, ys):
    pts = []
    for pt in zip(x, y):
        pts.append(db.DPoint(*pt))
    t1 = db.DTrans.R90
    if rotate90:
        top.shapes(layer0).insert(db.DPolygon(pts) * t1)
    else:
        top.shapes(layer0).insert(db.DPolygon(pts))

ly.write(f'ChirpedGrating_{today}_PChirp{periods[2]}_{periods[0]}_FFChirp{ffs[2]}_{ffs[0]}.gds')