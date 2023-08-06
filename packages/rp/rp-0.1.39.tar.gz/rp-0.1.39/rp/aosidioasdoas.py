import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from rp import *
win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: PanningPlot')

plt = win.addPlot()
curve = plt.plot()
data = []
count = 0

def ptlaunch():
    print('ray')
    print('pf')
    print('sunshine')
    pseudo_terminal(globals())
def update():
    global data, curve, count
    # print("HOI!")
    #
    #
    data.append(np.random.normal(size=10) + np.sin(count * 0.1) * 5)
    if len(data) > 100:
        data.pop(0)
    curve.setData(np.hstack(data))
    count += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
#
class Thread(pg.QtCore.QThread):
    newData = pg.QtCore.Signal(object)
    def run(self):
        ptlaunch()
thread = Thread()
thread.newData.connect(update)
thread.start()
#
QtGui.QApplication.instance().exec_()









from rp import *
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

app=QtGui.QApplication([])# Weird...a callable module...

win=pg.GraphicsLayoutWidget()## Create window with GraphicsView widget
win.show()## show widget alone in its own window
win.setWindowTitle('pyqtgraph example: ImageItem')

img=pg.ImageItem(border='w')

view=win.addViewBox()
view.setAspectLocked(True)
view.addItem(img)

funcs=[lambda:img.setImage(load_image_from_webcam(1))]
def update():
    seq(funcs)
class Thread(pg.QtCore.QThread):
    newData = pg.QtCore.Signal(object)
    def run(self):
        pseudo_terminal(globals())
thread=Thread()
thread.newData.connect(update)
thread.start(50)

QtGui.QApplication.instance().exec_()
