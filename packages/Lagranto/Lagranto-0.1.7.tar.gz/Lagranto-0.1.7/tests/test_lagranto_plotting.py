from PIL import Image
from lagranto import Tra
from path import Path
from lagranto.plotting import _get_segments, plot_trajs
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

plt.switch_backend('agg')

testdatadir = Path.dirname(Path(__file__)).joinpath('test_data')
netcdffile = testdatadir / 'lsl_lagranto2_0.nc'


def test_segments():
    trajs = Tra()
    trajs.load_netcdf(netcdffile)
    segments = _get_segments(trajs[0, :])
    np.testing.assert_array_equal(segments[0, :, 0], trajs['lon'][0, :2])
    np.testing.assert_array_equal(segments[-1, :, 1], trajs['lat'][0, -2:])


def test_plot_trajs():
    picfile = testdatadir.joinpath('test_plot_trajs.png')
    if picfile.isfile():
        ctrl_array = np.array(Image.open(picfile))
    trajs = Tra()
    trajs.load_netcdf(netcdffile)
    figure = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([0, 20, 40, 50])
    lc = plot_trajs(ax, trajs[:10], 'z')
    if picfile.isfile():
        npicfile = picfile.replace(picfile.ext, '_test' + picfile.ext)
        figure.savefig(npicfile)
        test_array = np.array(Image.open(npicfile))
        np.testing.assert_almost_equal(ctrl_array, test_array)
        Path(npicfile).remove()
    else:
        figure.savefig(picfile)
