"""
    This file is part of gempy.

    gempy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with gempy.  If not, see <http://www.gnu.org/licenses/>.


Module with classes and methods to perform implicit regional modelling based on
the potential field method.
Tested on Ubuntu 14

Created on 10/10 /2016

@author: Miguel de la Varga

"""
import os
from os import path
import sys

# This is for sphenix to find the packages
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import numpy as _np

# --DEP-- import pandas as _pn
import copy
from gempy.Visualization import PlotData2D, steano3D, vtkVisualization
from gempy.DataManagement import InputData, InterpolatorInput, GridClass
from gempy.sequential_pile import StratigraphicPile
from gempy.Topology import topology_analyze, topology_check_adjacency
import gempy.UncertaintyAnalysisPYMC2 # So far we use this type of import because the other one makes a copy and blows up some asserts


def data_to_pickle(geo_data, path=False):
    """
     Save InputData object to a python pickle (serialization of python). Be aware that if the dependencies
     versions used to export and import the pickle differ it may give problems
     Args:
         path (str): path where save the pickle

     Returns:
         None
     """
    geo_data.data_to_pickle(path)


def read_pickle(path):
    """
    Read InputData object from python pickle.
    Args:
       path (str): path where save the pickle

    Returns:
        gempy.DataManagement.InputData: Input Data object
    """
    import pickle
    with open(path, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)
        return data


def get_series(geo_gata):
    """
    Args:
         geo_data (gempy.DataManagement.InputData object)

    Returns:
        Pandas.DataFrame: Return series and formations relations
    """
    return geo_gata.series


def get_grid(geo_data):
    """
     Args:
          geo_data (gempy.DataManagement.InputData object)

     Returns:
         numpy.array: Return series and formations relations
     """
    return geo_data.grid.grid


def get_resolution(geo_data):
    return geo_data.resolution


def get_extent(geo_data):
    return geo_data.extent


def get_data(geo_data, dtype='all', numeric=False, verbosity=0):
    """
        Method that returns the interfaces and foliations pandas Dataframes. Can return both at the same time or only
        one of the two
        Args:
            itype: input data type, either 'foliations', 'interfaces' or 'all' for both.
            verbosity (int): Number of properties shown
        Returns:
            pandas.core.frame.DataFrame: Data frame with the raw data

        """
    return geo_data.get_data(itype=dtype, numeric=numeric, verbosity=verbosity)


def create_data(extent, resolution=[50, 50, 50], **kwargs):
    """
    Method to create a InputData object. It is analogous to gempy.InputData()

    Args:
        extent (list or array):  [x_min, x_max, y_min, y_max, z_min, z_max]. Extent for the visualization of data
         and default of for the grid class.
        resolution (list or array): [nx, ny, nz]. Resolution for the visualization of data
         and default of for the grid class.

    Keyword Args:
        Resolution ((Optional[list])): [nx, ny, nz]. Defaults to 50
        path_i: Path to the data bases of interfaces. Default os.getcwd(),
        path_f: Path to the data bases of foliations. Default os.getcwd()

    Returns:
        GeMpy.DataManagement: Object that encapsulate all raw data of the project


        dep: self.Plot(GeMpy_core.PlotData): Object to visualize data and results
    """

    return InputData(extent, resolution, **kwargs)


def i_set_data(geo_data, dtype="foliations", action="Open"):
    """
    Method to have interactive pandas tables in jupyter notebooks. The idea is to use this method to interact with
    the table and i_close_set_data to recompute the parameters that depend on the changes made. I did not find a
    easier solution than calling two different methods. After editing a dataframe is recommended to call
     i_set_data(action= 'close') to recompute dependent variables
    Args:
        itype: input data type, either 'foliations' or 'interfaces'

    Returns:
        pandas.core.frame.DataFrame: Data frame with the changed data on real time
    """
    if action == 'Close':
        geo_data.i_close_set_data()

    if action == 'Open':
        geo_data.i_open_set_data(itype=dtype)


def select_series(geo_data, series):
    """
    Return the formations of a given serie in string
    :param series: list of int or list of str
    :return: formations of a given serie in string separeted by |
    """
    new_geo_data = copy.deepcopy(geo_data)

    if type(series) == int or type(series[0]) == int:
        new_geo_data.interfaces = geo_data.interfaces[geo_data.interfaces['order_series'].isin(series)]
        new_geo_data.foliations = geo_data.foliations[geo_data.foliations['order_series'].isin(series)]
    elif type(series[0]) == str:
        new_geo_data.interfaces = geo_data.interfaces[geo_data.interfaces['series'].isin(series)]
        new_geo_data.foliations = geo_data.foliations[geo_data.foliations['series'].isin(series)]

    # Count faults
    new_geo_data.set_faults(new_geo_data.count_faults())

    # Change the dataframe with the series
    new_geo_data.series = new_geo_data.series[new_geo_data.interfaces['series'].unique()]
    new_geo_data.set_formation_number()
    return new_geo_data


def set_series(geo_data, series_distribution=None, order_series=None, order_formations=None,
               update_p_field=True, verbose=1):
    """
    Method to define the different series of the project.

    Args:
        series_distribution (dict): with the name of the serie as key and the name of the formations as values.
        order(Optional[list]): order of the series by default takes the dictionary keys which until python 3.6 are
           random. This is important to set the erosion relations between the different series

    Returns:
        self.series: A pandas DataFrame with the series and formations relations
        self.interfaces: one extra column with the given series
        self.foliations: one extra column with the given series
    """
    geo_data.set_series(series_distribution=series_distribution, order=order_series)
    geo_data.order_table()
    if order_formations is not None:
        geo_data.set_formation_number(order_formations)
    # DEP
    if verbose > 0:
         return get_sequential_pile(geo_data)
    else:
        return None

def set_order_formations(geo_data, order_formations):
    geo_data.set_formation_number(order_formations)

def set_interfaces(geo_data, interf_Dataframe, append=False):
    """
     Method to change or append a Dataframe to interfaces in place.
     Args:
         interf_Dataframe: pandas.core.frame.DataFrame with the data
         append: Bool: if you want to append the new data frame or substitute it
     """
    geo_data.set_interfaces(interf_Dataframe, append=append)
    # --DEP--
    # # To update the interpolator parameters without calling a new object
    # try:
    #     geo_data.interpolator._data = geo_data
    #     geo_data.interpolator._grid = geo_data.grid
    #
    #     if update_p_field:
    #         geo_data.interpolator.compute_potential_fields()
    # except AttributeError:
    #     pass


def set_foliations(geo_data, foliat_Dataframe, append=False, update_p_field=True):
    """
    Method to change or append a Dataframe to foliations in place.  A equivalent Pandas Dataframe with
    ['X', 'Y', 'Z', 'dip', 'azimuth', 'polarity', 'formation'] has to be passed.
    Args:
        interf_Dataframe: pandas.core.frame.DataFrame with the data
        append: Bool: if you want to append the new data frame or substitute it
    """

    geo_data.set_foliations(foliat_Dataframe, append=append)
    # To update the interpolator parameters without calling a new object
    # try:
    #     geo_data.interpolator._data = geo_data
    #     geo_data.interpolator._grid = geo_data.grid
    #   #  geo_data.interpolator._set_constant_parameteres(geo_data, geo_data.interpolator._grid)
    #     if update_p_field:
    #         geo_data.interpolator.compute_potential_fields()
    # except AttributeError:
    #     pass

#DEP?
# def set_grid(geo_data, new_grid=None, extent=None, resolution=None, grid_type="regular_3D", **kwargs):
#     """
#     Method to initialize the class new_grid. So far is really simple and only has the regular new_grid type
#
#     Args:
#         grid_type (str): regular_3D or regular_2D (I am not even sure if regular 2D still working)
#         **kwargs: Arbitrary keyword arguments.
#
#     Returns:
#         self.new_grid(GeMpy_core.new_grid): Object that contain different grids
#     """
#     if new_grid is not None:
#         assert new_grid.shape[1] is 3 and len(new_grid.shape) is 2, 'The shape of new grid must be (n,3) where n is' \
#                                                                     'the number of points of the grid'
#         geo_data.grid.grid = new_grid
#     else:
#         if not extent:
#             extent = geo_data.extent
#         if not resolution:
#             resolution = geo_data.resolution
#
#         geo_data.grid = geo_data.GridClass(extent, resolution, grid_type=grid_type, **kwargs)


def plot_data(geo_data, direction="y", data_type = 'all', series="all", legend_font_size=6, **kwargs):
    """
    Plot the projection of the raw data (interfaces and foliations) in 2D following a
    specific directions

    Args:
        direction(str): xyz. Caartesian direction to be plotted
        series(str): series to plot
        **kwargs: seaborn lmplot key arguments. (TODO: adding the link to them)

    Returns:
        None
    """
    plot = PlotData2D(geo_data)
    plot.plot_data(direction=direction, data_type=data_type, series=series, legend_font_size=legend_font_size, **kwargs)
    # TODO saving options


def plot_section(geo_data, block, cell_number, direction="y", **kwargs):
    """
    Plot a section of the block model

    Args:
        cell_number(int): position of the array to plot
        direction(str): xyz. Caartesian direction to be plotted
        interpolation(str): Type of interpolation of plt.imshow. Default 'none'.  Acceptable values are 'none'
        ,'nearest', 'bilinear', 'bicubic',
        'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser',
        'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc',
        'lanczos'
       **kwargs: imshow keywargs

    Returns:
        None
    """
    plot = PlotData2D(geo_data)
    plot.plot_block_section(cell_number, block=block, direction=direction, **kwargs)
    # TODO saving options


def plot_potential_field(geo_data, potential_field, cell_number, N=20,
                         direction="y", plot_data=True, series="all", *args, **kwargs):
    """
    Plot a potential field in a given direction.

    Args:
        cell_number(int): position of the array to plot
        potential_field(str): name of the potential field (or series) to plot
        n_pf(int): number of the  potential field (or series) to plot
        direction(str): xyz. Caartesian direction to be plotted
        serie: *Deprecated*
        **kwargs: plt.contour kwargs

    Returns:
        None
    """
    plot = PlotData2D(geo_data)
    plot.plot_potential_field(potential_field, cell_number, N=N,
                              direction=direction,  plot_data=plot_data, series=series,
                              *args, **kwargs)


def plot_data_3D(geo_data):
    """
    Plot in vtk all the input data of a model
    Args:
        geo_data (gempy.DataManagement.InputData): Input data of the model

    Returns:
        None
    """
    vv = vtkVisualization(geo_data)
    vv.set_interfaces()
    vv.set_foliations()
    vv.render_model()
    return None

def get_sequential_pile(geo_data):
    """
    Visualize an interactive stratigraphic pile to move around the formations and the series. IMPORTANT NOTE:
    To have the interactive properties it is necessary the use of qt as interactive backend. (In notebook use:
    %matplotlib qt5)
    Args:
        geo_data: gempy.DataManagement.InputData object

    Returns:
        interactive Matplotlib figure
    """
    return StratigraphicPile(geo_data)


def set_interpolation_data(geo_data, **kwargs):
    """
    InterpolatorInput is a class that contains all the preprocessing operations to prepare the data to compute the model.
    Also is the object that has to be manipulated to vary the data without recompile the modeling function.

    Args:
        geo_data(gempy.DataManagement.InputData): All values of a DataManagement object
        compile_theano (bool): select if the theano function is compiled during the initialization. Default: True
        compute_all (bool): If true the solution gives back the block model of lithologies, the potential field and
         the block model of faults. If False only return the block model of lithologies. This may be important to speed
          up the computation. Default True
        u_grade (list): grade of the polynomial for the universal part of the Kriging interpolations. The value has to
        be either 0, 3 or 9 (number of equations) and the length has to be the number of series. By default the value
        depends on the number of points given as input to try to avoid singular matrix. NOTE: if during the computation
        of the model a singular matrix is returned try to reduce the u_grade of the series.
        rescaling_factor (float): rescaling factor of the input data to improve the stability when float32 is used. By
        defaut the rescaling factor is calculated to obtein values between 0 and 1.

    Keyword Args:
         dtype ('str'): Choosing if using float32 or float64. This is important if is intended to use the GPU
         See Also InterpolatorClass kwargs

    Attributes:
        geo_data: Original gempy.DataManagement.InputData object
        geo_data_res: Rescaled data. It has the same structure has gempy.InputData
        interpolator: Instance of the gempy.DataManagement.InterpolaorInput.InterpolatorClass. See Also
         gempy.DataManagement.InterpolaorInput.InterpolatorClass docs
         th_fn: Theano function which compute the interpolation
        dtype:  type of float

    """
    in_data = InterpolatorInput(geo_data, **kwargs)
    return in_data


def plot_surfaces_3D(geo_data, vertices_l, simplices_l,
                     #formations_names_l, formation_numbers_l,
                     alpha=1, plot_data=True,
                     size=(1920, 1080), fullscreen=False):
    """
    Plot in vtk the surfaces. For getting vertices and simplices See gempy.get_surfaces
    Args:
        vertices_l (numpy.array): 2D array (XYZ) with the coordinates of the points
        simplices_l (numpy.array): 2D array with the value of the vertices that form every single triangle
        formations_names_l (list): Name of the formation of the surfaces
        formation_numbers_l (list): Formation numbers (int)
        alpha (float): Opacity
        plot_data (bool): Default True
        size (tuple): Resolution of the window
        fullscreen (bool): Launch window in full screen or not
    Returns:
        None
    """
    w = vtkVisualization(geo_data)
    w.set_surfaces(vertices_l, simplices_l,
                   #formations_names_l, formation_numbers_l,
                    alpha)

    if plot_data:
        w.set_interfaces()
        w.set_foliations()
    w.render_model(size=size, fullscreen=fullscreen)
    return w

def export_vtk_rectilinear(geo_data, block, path=None):
    """
    Export data to a vtk file for posterior visualizations
    Args:
        geo_data(gempy.InputData): All values of a DataManagement object
        block(numpy.array): 3D array containing the lithology block
        path (str): path to the location of the vtk

    Returns:
        None
    """
    vtkVisualization.export_vtk_lith_block(geo_data, block, path)

# =====================================
# Functions for the InterpolatorData
# =====================================
# TODO check that is a interp_data object and if not try to create within the function one from the geo_data


def get_kriging_parameters(interp_data, verbose=0):
    """
    Print the kringing parameters
    Args:
        interp_data (gempy.DataManagement.InterpolatorInput)
        verbose (int): if > 0 print all the shape values as well.

    Returns:
        None
    """
    return interp_data.interpolator.get_kriging_parameters(verbose=verbose)


def get_th_fn(interp_data, compute_all=True):
    """
    Get theano function
    Args:
        interp_data (gempy.DataManagement.InterpolatorInput): Rescaled data.
         compute_all (bool): If true the solution gives back the block model of lithologies, the potential field and
         the block model of faults. If False only return the block model of lithologies. This may be important to speed
          up the computation. Default True

    Returns:
        theano.function: Compiled function if C or CUDA which computes the interpolation given the input data
            (XYZ of dips, dip, azimuth, polarity, XYZ ref interfaces, XYZ rest interfaces)
    """

    return interp_data.compile_th_fn(compute_all=compute_all)


def compute_model(interp_data, output='geology', u_grade=None, get_potential_at_interfaces=False):
    """
    Compute the geological model
    Args:
        interp_data (gempy.DataManagement.InterpolatorInput): Rescaled data.
        u_grade (list): grade of the polynomial for the universal part of the Kriging interpolations. The value has to
        be either 0, 3 or 9 (number of equations) and the length has to be the number of series. By default the value
        depends on the number of points given as input to try to avoid singular matrix. NOTE: if during the computation
        of the model a singular matrix is returned try to reduce the u_grade of the series.
        get_potential_at_interfaces (bool): Get potential at interfaces

    Returns:
        numpy.array: if compute_all was chosen in gempy.DataManagement.InterpolatorInput, the first
        row will be the lithology block model, the second the potential field and the third the fault
        network block. if compute_all was False only the lithology block model will be computed. In
        addition if get_potential_at_interfaces is True, the value of the potential field at each of
        the interfaces is given as well
    """
    if not getattr(interp_data, 'th_fn', None):
        interp_data.compile_th_fn()

    i = interp_data.get_input_data(u_grade=u_grade)

    if output is 'geology':
        lith_matrix, fault_matrix, potential_at_interfaces = interp_data.th_fn(*i)
        # TODO check if this is necessary yet
        if len(lith_matrix.shape) < 3:
            _np.expand_dims(lith_matrix, 0)
            _np.expand_dims(fault_matrix, 0)

        interp_data.potential_at_interfaces = potential_at_interfaces

        if get_potential_at_interfaces:
            return lith_matrix, fault_matrix, interp_data.potential_at_interfaces
        else:
            return lith_matrix, fault_matrix

    # TODO this should be a flag read from the compilation I guess
    if output is 'gravity':
        # TODO make asserts
        lith_matrix, fault_matrix, potential_at_interfaces, grav = interp_data.th_fn(*i)
        if len(lith_matrix.shape) < 3:
            _np.expand_dims(lith_matrix, 0)
            _np.expand_dims(fault_matrix, 0)

        interp_data.potential_at_interfaces = potential_at_interfaces

        if get_potential_at_interfaces:
            return lith_matrix, fault_matrix, grav, interp_data.potential_at_interfaces
        else:
            return lith_matrix, fault_matrix, grav


def get_surfaces(interp_data, potential_lith=None, potential_fault=None, n_formation='all', step_size=1, original_scale=True):
    """
    compute vertices and simplices of the interfaces for its vtk visualization or further
    analysis
    Args:
        potential_lith (numpy.array): 1D numpy array with the solution of the computation of the model
         containing the scalar field of potentials (second row of solution)
        interp_data (gempy.DataManagement.InterpolatorInput): Interpolator object.
        n_formation (int or 'all'): Positive integer with the number of the formation of which the surface is returned.
         use method get_formation_number() to get a dictionary back with the values
        step_size (int): resolution of the method. This is every how many voxels the marching cube method is applied
        original_scale (bool): choosing if the coordinates of the vertices are given in the original or the rescaled
         coordinates

    Returns:
        vertices, simpleces
    """
    try:
        getattr(interp_data, 'potential_at_interfaces')
    except:
        raise AttributeError('You need to compute the model first')

    def get_surface(potential_block, interp_data, pot_int, n_formation, step_size, original_scale):
        assert n_formation > 0, 'Number of the formation has to be positive'
        # In case the values are separated by series I put all in a vector
        pot_int = interp_data.potential_at_interfaces.sum(axis=0)

        from skimage import measure

        if not potential_block.max() > pot_int[n_formation-1]:
            pot_int[n_formation - 1] = potential_block.max()
            print('Potential field of the surface is outside the block. Probably is due to float errors')

        if not potential_block.min() < pot_int[n_formation - 1]:
            pot_int[n_formation - 1] = potential_block.min()
            print('Potential field of the surface is outside the block. Probably is due to float errors')

        vertices, simplices, normals, values = measure.marching_cubes_lewiner(
            potential_block.reshape(interp_data.geo_data_res.resolution[0],
                                    interp_data.geo_data_res.resolution[1],
                                    interp_data.geo_data_res.resolution[2]),
            pot_int[n_formation-1],
            step_size=step_size,
            spacing=((interp_data.geo_data_res.extent[1] - interp_data.geo_data_res.extent[0]) / interp_data.geo_data_res.resolution[0],
                     (interp_data.geo_data_res.extent[3] - interp_data.geo_data_res.extent[2]) / interp_data.geo_data_res.resolution[1],
                     (interp_data.geo_data_res.extent[5] - interp_data.geo_data_res.extent[4]) / interp_data.geo_data_res.resolution[2]))


        if original_scale:
            vertices = interp_data.rescaling_factor * vertices + _np.array([interp_data._geo_data.extent[0],
                                                                            interp_data._geo_data.extent[2],
                                                                            interp_data._geo_data.extent[4]]).reshape(1, 3)
        else:
            vertices += _np.array([interp_data.geo_data_res.extent[0],
                                   interp_data.geo_data_res.extent[2],
                                   interp_data.geo_data_res.extent[4]]).reshape(1, 3)
        return vertices, simplices

    vertices = []
    simplices = []

    if potential_fault is not None:

        assert len(_np.atleast_2d(potential_fault)) is interp_data.geo_data_res.n_faults, 'You need to pass a potential field per fault'

        pot_int = interp_data.potential_at_interfaces[:interp_data.geo_data_res.n_faults + 1]
        for n in interp_data.geo_data_res.interfaces['formation number'][
            interp_data.geo_data_res.interfaces['isFault']].unique():
            if n == 0:
                continue
            else:
                v, s = get_surface(_np.atleast_2d(potential_fault)[n-1], interp_data, pot_int, n,
                                   step_size=step_size, original_scale=original_scale)
                vertices.append(v)
                simplices.append(s)

    if potential_lith is not None:
        pot_int = interp_data.potential_at_interfaces[interp_data.geo_data_res.n_faults:]

        # Compute the vertices of the lithologies
        if n_formation == 'all':

            for n in interp_data.geo_data_res.interfaces['formation number'][~interp_data.geo_data_res.interfaces['isFault']].unique():
                if n == 0:
                    continue
                else:
                    v, s = get_surface(potential_lith, interp_data, pot_int, n,
                                       step_size=step_size, original_scale=original_scale)
                    vertices.append(v)
                    simplices.append(s)
        else:
            vertices, simplices = get_surface(potential_lith, interp_data, pot_int, n_formation,
                                              step_size=step_size, original_scale=original_scale)


    return vertices, simplices


def export_to_vtk(geo_data, path=None, lith_block=None, vertices=None, simplices=None):
    if lith_block is not None:
        vtkVisualization.export_vtk_lith_block(geo_data, lith_block, path=path)
    if vertices is not None and simplices is not None:
        vtkVisualization.export_vtk_surfaces(vertices, simplices)



def plot_surfaces_3D_real_time(interp_data, vertices_l, simplices_l,
                     #formations_names_l, formation_numbers_l,
                     alpha=1, plot_data=True, posterior=None, samples=None,
                     size=(1920, 1080), fullscreen=False):
    """
    Plot in vtk the surfaces in real time. Moving the input data will affect the surfaces.
    IMPORTANT NOTE it is highly recommended to have the flag fast_run in the theano optimization. Also note that the
    time needed to compute each model increases linearly with every potential field (i.e. fault or discontinuity). It
    may be better to just modify each potential field individually to increase the speed (See gempy.select_series).
    Args:
        vertices_l (numpy.array): 2D array (XYZ) with the coordinates of the points
        simplices_l (numpy.array): 2D array with the value of the vertices that form every single triangle
        formations_names_l (list): Name of the formation of the surfaces
        formation_numbers_l (list): Formation numbers (int)
        alpha (float): Opacity
        plot_data (bool): Default True
        size (tuple): Resolution of the window
        fullscreen (bool): Launch window in full screen or not
    Returns:
        None
    """
    assert isinstance(interp_data, InterpolatorInput), 'The object has to be instance of the InterpolatorInput'
    w = vtkVisualization(interp_data.geo_data_res, real_time=True)
    w.set_surfaces(vertices_l, simplices_l,
                   #formations_names_l, formation_numbers_l,
                    alpha)

    if posterior is not None:
        assert isinstance(posterior, gempy.UncertaintyAnalysisPYMC2.Posterior), 'The object has to be instance of the Posterior class'
        w.post = posterior
        if samples is not None:
            samp_i = samples[0]
            samp_f = samples[1]
        else:
            samp_i = 0
            samp_f = posterior.n_iter

        w.create_slider_rep(samp_i, samp_f, samp_f)

    w.interp_data = interp_data
    if plot_data:
        w.set_interfaces()
        w.set_foliations()
    w.render_model(size=size, fullscreen=fullscreen)


def topology_compute(geo_data, lith_block, fault_block,
                     cell_number=None, direction=None,
                     compute_areas=False, return_label_block=False):
    """
    Computes model topology and returns graph, centroids and look-up-tables.
    :param geo_data: geo_data object
    :param lith_block: lithology block
    :param fault_block: fault block
    :param cell_number: (int) the slice position
    :param direction: (str) "x", "y", or "z" - the slice direction
    :return: (adjacency Graph object, centroid dict, labels-to-lith LOT dict, lith-to_labels LOT dict)
    """
    fault_block = fault_block[::2].sum(axis=0)

    if cell_number is None or direction is None:  # topology of entire block
        lb = lith_block.reshape(geo_data.resolution)
        fb = fault_block.reshape(geo_data.resolution)
    elif direction == "x":
        lb = lith_block.reshape(geo_data.resolution)[cell_number, :, :]
        fb = fault_block.reshape(geo_data.resolution)[cell_number, :, :]
    elif direction == "y":
        lb = lith_block.reshape(geo_data.resolution)[:, cell_number, :]
        fb = fault_block.reshape(geo_data.resolution)[:, cell_number, :]
    elif direction == "z":
        lb = lith_block.reshape(geo_data.resolution)[:, :, cell_number]
        fb = fault_block.reshape(geo_data.resolution)[:, :, cell_number]

    return topology_analyze(lb, fb, geo_data.n_faults, areas_bool=compute_areas, return_block=return_label_block)


def topology_plot(geo_data, G, centroids, direction="y"):
    "Plot topology graph."
    PlotData2D.plot_topo_g(geo_data, G, centroids, direction=direction)


# =====================================
# Functions for Geophysics
# =====================================
def precomputations_gravity(interp_data, n_chunck=25, densities=None):
    try:
        getattr(interp_data, 'geophy')
    except:
        raise AttributeError('You need to set a geophysical object first. See set_geophysics_obj')

    tz, select = interp_data.geophy.compute_gravity(n_chunck)
    interp_data.interpolator.set_z_comp(tz, select)

    if densities is not None:
        set_densities(interp_data, densities)
    return tz, select


def set_geophysics_obj(interp_data, ai_extent, ai_resolution, ai_z=None, range_max=None):

    assert isinstance(interp_data, InterpolatorInput), 'The object has to be instance of the InterpolatorInput'
    interp_data.set_geophysics_obj(ai_extent, ai_resolution, ai_z=ai_z, range_max=range_max)
    return interp_data.geophy


def set_densities(interp_data, densities):

    interp_data.interpolator.set_densities(densities)