# import pya
import klayout.db as db
import math
import numpy as np
from datetime import date
today = date.today()

### Variables ###
central_period = 0.368
period_span =    0.05
steps = 11

p = np.linspace(central_period - period_span/2, central_period + period_span/2, num=steps)
period = [np.round(pl,3) for pl in p]
fillfactor = 0.86
inv_ff = 1 - fillfactor

### Layout ###
length = 500
height = 500
y = 1500
offset_from_origin = [500, 1500, 2500]
offset_from_origin1 = [500, 1500, 2500]
offset_from_origin2 = [500, 1500, 2500]

ly = db.Layout()
ly.dbu = 0.001
top_cell = ly.create_cell("TOP")
layer = ly.layer(1, 0)
l2 = ly.layer(2, 0)
l3 = ly.layer(3,0)

for per, off in zip(period[:3], offset_from_origin[:5]):
    n1 = math.floor(length / per)
    for i in range(0, n1):
        pt = db.DPoint((i * per)+off, 2000)
        box = db.DBox(pt, pt + db.DVector(per * inv_ff, height))

        top_cell.shapes(layer).insert(box)

for per, off in zip(period[3:6], offset_from_origin1):
    n2 = math.floor(length / per)
    for i in range(0, n2):
        pt = db.DPoint((i * per)+off, 1000)
        box = db.DBox(pt, pt + db.DVector(per * inv_ff, height))

        top_cell.shapes(layer).insert(box)
        
for per, off in zip(period[6:], offset_from_origin2):
    n2 = math.floor(length / per)
    for i in range(0, n2):
        pt = db.DPoint((i * per)+off, 0)
        box = db.DBox(pt, pt + db.DVector(per * inv_ff, height))

        top_cell.shapes(layer).insert(box)
        
x_text = [500, 1500, 2500, 500, 1500, 2500, 500, 1500, 2500]
y_text = [1950, 1950, 1950, 950, 950, 950, -50, -50, -50]

for index, (x, y) in enumerate(zip(x_text,y_text)):
    mag = 50
    gen = db.TextGenerator.default_generator()
    region = gen.text(f'P{np.round(period[index],4)}um, FF{fillfactor}', ly.dbu, mag)
    top_cell.shapes(l2).insert(region, db.DTrans(db.DVector(x, y)))

### Alignment Markers ###
x0 = 0
y0 = -500
x1 = 50
y1= -450
offsety = 3450
offsetx = 3450

top_cell.shapes(l3).insert(db.DBox(x0, y0, x1, y1))                                  # BL
top_cell.shapes(l3).insert(db.DBox(x0, y0+offsety, x1, y1+offsety))                  # TL 
top_cell.shapes(l3).insert(db.DBox(x0+100, y0+offsety, x1+100, y1+offsety))          # TL
top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0+offsety, x1+offsetx, y1+offsety))  # TR
top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0, x1+offsetx, y1))                  # BR

ly.write(f'{today}_Period_Sweep_GMR_P{period[0]}_P{period[-1]}_FF{fillfactor}um.gds')