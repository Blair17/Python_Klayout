# import pya
import klayout.db as db
import math
import numpy as np
from datetime import date
today = date.today()

### Variables ###
p = np.linspace(0.3,0.6,num=11)
period = [np.round(pl,3) for pl in p]
fillfactor = 0.75
inv_ff = 1 - fillfactor

### Layout ###
length = 100
height = 5000
y = 800
offset_from_origin = [500, 800, 1100, 1400, 1700, 2000, 2300, 2600, 2900, 3200]

ly = db.Layout()
ly.dbu = 0.001
top_cell = ly.create_cell("TOP")
layer = ly.layer(1, 0)
l2 = ly.layer(2, 0)
l3 = ly.layer(3,0)

for per, off in zip(period, offset_from_origin):
    n1 = math.floor(length / per)
    for i in range(0, n1):
        pt = db.DPoint((i * per)+off, y)
        box = db.DBox(pt, pt + db.DVector(per * inv_ff, height))

        top_cell.shapes(layer).insert(box)

# for per, off in zip(period[5:], offset_from_origin):
#     n2 = math.floor(length / per)
#     for i in range(0, n2):
#         pt = db.DPoint((i * per)+off, 500)
#         box = db.DBox(pt, pt + db.DVector(per * inv_ff, height))

#         top_cell.shapes(layer).insert(box)
        
x_text = [400, 725, 1100, 1350, 1700, 1950, 2300, 2600, 3000, 3300]
x_text = [x - 150 for x in x_text]
y_text = [500, 300, 500, 300, 500, 300, 500, 300, 500, 300]

for index, (x, y) in enumerate(zip(x_text, y_text)):
    mag = 150
    gen = db.TextGenerator.default_generator()
    region = gen.text(f'P{np.round(period[index],4)}um', ly.dbu, mag)
    top_cell.shapes(l2).insert(region, db.DTrans(db.DVector(x, y)))

gen = db.TextGenerator.default_generator()
region = gen.text(f'FF{np.round(fillfactor,4)}', ly.dbu, mag)
top_cell.shapes(l2).insert(region, db.DTrans(db.DVector(np.median(x_text), 6200)))

### Alignment Markers ###
x0 = 0
y0 = 0
x1 = 50
y1= 50
offsety = 6300
offsetx = 3800

top_cell.shapes(l3).insert(db.DBox(x0, y0, x1, y1))                                  # BL
top_cell.shapes(l3).insert(db.DBox(x0, y0+offsety, x1, y1+offsety))                  # TL 
top_cell.shapes(l3).insert(db.DBox(x0+100, y0+offsety, x1+100, y1+offsety))          # TL
top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0+offsety, x1+offsetx, y1+offsety))  # TR
top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0, x1+offsetx, y1))                  # BR

ly.write(f'Long_GMR_Period_Sweep_GMR_P{period[0]}_P{period[-1]}_FF{fillfactor}um_{today}.gds')