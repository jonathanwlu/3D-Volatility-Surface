import numpy as np
from scipy.interpolate import griddata
import pandas as pd
import pyodbc
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_symbol(sym):
    with open('spec/VolSurf.sql', "r") as f:
        sql = f.read()
    split = sql.split('SPY')
    sql = split[0]
    for i in split[1:]:
        sql += sym + i
    cnxn = pyodbc.connect("Driver={SQL Server};Server=[server];UID=[user];PWD=[pw];Database=stocks;")
    data = pd.read_sql_query(sql, cnxn)
    cnxn.close()

    dtes = data['TDTE'].unique()
    strikes = data['Strike'].unique()
    dtes.sort()
    strikes.sort()

    X, Y = np.meshgrid(dtes, strikes)
    Z = griddata((data['TDTE'].values, data['Strike'].values), data['IV'].values, (X, Y), method='nearest')
    Z[Z < 0] = np.nan
    Z[Z > 100] = np.nan

    plt.cla()
    surf = ax.plot_surface(X, Y, Z, vmin=np.nanmin(data['IV']), vmax=np.nanmax(data['IV']))  # , cmap=cm.rainbow)
    px = data['sPx'][0]
    for i in range(min(dtes), max(dtes), 10):
        ax.plot([i, i], [px, px], [np.nanmin(data['IV']), np.nanmax(data['IV'])], 'k:', alpha=0.5, linewidth=1)
    ax.set_xlabel('DTE')
    ax.set_ylabel('Strike')
    ax.set_zlabel('IV')
    plt.tight_layout()

fig = plt.figure()
ax = fig.gca(projection='3d')

# control panel #
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


def update():
    textbox.selectAll()
    textbox.setFocus()
    try:
        plot_symbol(textbox.text())
        print('updating')
        fig.canvas.draw()
    except Exception:
        print('invalid symbol')

root = fig.canvas.manager.window
panel = QtWidgets.QWidget()
hbox = QtWidgets.QHBoxLayout(panel)
textbox = QtWidgets.QLineEdit(parent=panel)
textbox.returnPressed.connect(update)
hbox.addWidget(textbox)
panel.setLayout(hbox)

dock = QtWidgets.QDockWidget("Symbol", root)
dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
root.addDockWidget(Qt.BottomDockWidgetArea, dock)
dock.setWidget(panel)

toolbar = root.findChild(QtWidgets.QToolBar)
toolbar.setVisible(False)

textbox.setText('SPY')
textbox.selectAll()
textbox.setFocus()
######################

plot_symbol('SPY')
plt.show()
