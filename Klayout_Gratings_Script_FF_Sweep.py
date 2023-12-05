# import pya
import klayout.db as db
import math
import numpy as np
from datetime import date
today = date.today()

### Variables ###
period = 0.440
fillfactor = [0.70, 0.75, 0.80, 0.85, 0.90]
inv_ff = [1 - ff for ff in fillfactor]

### Layout ###
length = 500
height = 500
y = 1500
offset_from_origin = [500, 1500, 2500]

ly = db.Layout()
ly.dbu = 0.001
top_cell = ly.create_cell("TOP")
layer = ly.layer(1, 0)
l2 = ly.layer(2, 0)
l3 = ly.layer(3,0)

for ff, off in zip(inv_ff[:3], offset_from_origin):
    n1 = math.floor(length / period)
    for i in range(0, n1):
        pt = db.DPoint((i * period)+off, y)
        box = db.DBox(pt, pt + db.DVector(period * ff, height))

        top_cell.shapes(layer).insert(box)
            
for ff, off in zip(inv_ff[:-2], offset_from_origin[:2]):
    n2 = math.floor(length / period)
    for i in range(0, n2):
        pt = db.DPoint((i * period)+off, 500)
        box = db.DBox(pt, pt + db.DVector(period * ff, height))

        top_cell.shapes(layer).insert(box)
        
x_text = [500, 1500, 2500, 500, 1500]
y_text = [1450, 1450, 1450, 450, 450]

for index, (x, y) in enumerate(zip(x_text,y_text)):
    mag = 50
    gen = db.TextGenerator.default_generator()
    region = gen.text(f'P{np.round(period,4)}um, FF{fillfactor[index]}', ly.dbu, mag)
    top_cell.shapes(l2).insert(region, db.DTrans(db.DVector(x, y)))

### Alignment Markers ###
x0 = 0
y0 = 0
x1 = 50
y1= 50
offsety = 2200
offsetx = 3450

top_cell.shapes(l3).insert(db.DBox(x0, y0, x1, y1))                                  # BL
top_cell.shapes(l3).insert(db.DBox(x0, y0+offsety, x1, y1+offsety))                  # TL 
top_cell.shapes(l3).insert(db.DBox(x0+100, y0+offsety, x1+100, y1+offsety))          # TL
top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0+offsety, x1+offsetx, y1+offsety))  # TR
top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0, x1+offsetx, y1))                  # BR

ly.write(f'FF_Sweep_GMR_P{period}um_FF{fillfactor[0]}_{fillfactor[-1]}_{today}.gds')