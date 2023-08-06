__author__ = "Christian Kongsgaard"
__license__ = "MIT"
__version__ = "0.0.1"

# -------------------------------------------------------------------------------------------------------------------- #
# Imports

# Module imports
import cmf
from datetime import datetime
from datetime import timedelta
import numpy as np
import xml.etree.ElementTree as ET
import os
import xmltodict
import pymesh as pm

# Livestock imports

# -------------------------------------------------------------------------------------------------------------------- #
# CMF Functions and Classes


class CMFModel:

    def __init__(self, folder):
        self.folder = folder
        self.mesh_path = None
        self.weather_dict = {}
        self.trees_dict = {}
        self.ground_dict = {}
        self.boundary_dict = {}
        self.solver_settings = None
        self.outputs = None
        self.solved = False
        self.results = {}

    def load_cmf_files(self, delete_after_load=True):

        def load_weather(folder, delete):

            # look for file
            if os.path.isfile(folder + '/weather.xml'):
                weather_path = folder + '/weather.xml'
            else:
                raise FileNotFoundError('Cannot find weather.xml in folder: ' + str(folder))

            # Parse file
            weather_tree = ET.tostring(ET.parse(weather_path).getroot())
            weather = xmltodict.parse(weather_tree)
            weather_dict = {}

            # convert to correct format
            for w_key in weather['weather'].keys():
                lst0 = eval(weather['weather'][w_key])
                if isinstance(lst0, dict):
                    lst1 = {}
                    for dict_key in lst0.keys():
                        lst1[dict_key] = [float(i) for i in lst0[dict_key]]
                else:
                    lst1 = lst0

                weather_dict[w_key] = lst1

            # delete file
            if delete:
                os.remove(weather_path)

            return weather_dict

        def load_tree(folder, delete):

            # look for file
            if os.path.isfile(folder + '/trees.xml'):
                tree_path = folder + '/trees.xml'
            else:
                tree_path = None

            if not tree_path:
                return None

            else:
                # Parse file
                tree_tree = ET.tostring(ET.parse(tree_path).getroot())
                trees = xmltodict.parse(tree_tree)
                tree_dict = {}

                # convert to correct format
                for tree_key in trees['tree'].keys():
                    tree_dict[str(tree_key)] = {}

                    for t in trees['tree'][str(tree_key)].keys():
                        tree_dict[str(tree_key)][str(t)] = eval(trees['tree'][str(tree_key)][str(t)])

                # delete file
                if delete:
                    os.remove(tree_path)

                return tree_dict

        def load_ground(folder, delete):

            # look for file
            if os.path.isfile(folder + '/ground.xml'):
                ground_path = folder + '/ground.xml'
            else:
                raise FileNotFoundError('Cannot find ground.xml in folder: ' + str(folder))

            # Parse file
            ground_tree = ET.tostring(ET.parse(ground_path).getroot())
            grounds = xmltodict.parse(ground_tree)
            ground_dict = {}

            # convert to correct format
            for ground in grounds['ground'].keys():
                ground_dict[str(ground)] = {}

                for g in grounds['ground'][ground]:
                    try:
                        ground_dict[str(ground)][str(g)] = eval(grounds['ground'][ground][g])
                    except NameError:
                        ground_dict[str(ground)][str(g)] = grounds['ground'][ground][g]

            # delete file
            if delete:
                os.remove(ground_path)

            return ground_dict

        def load_mesh(folder):

            # look for file
            if os.path.isfile(folder + '/mesh.obj'):
                mesh_path = folder + '/mesh.obj'
            else:
                raise FileNotFoundError('Cannot find mesh.obj in folder: ' + str(folder))

            return mesh_path

        def load_outputs(folder, delete):

            # look for file
            if os.path.isfile(folder + '/outputs.xml'):
                output_path = folder + '/outputs.xml'
            else:
                raise FileNotFoundError('Cannot find outputs.xml in folder: ' + str(folder))

            # Parse file
            output_tree = ET.tostring(ET.parse(output_path).getroot())
            outputs = xmltodict.parse(output_tree)
            output_dict = {}

            # convert to correct format
            for out in outputs['output'].keys():
                output_dict[str(out)] = eval(outputs['output'][out])

            # delete file
            if delete:
                os.remove(output_path)

            return output_dict

        def load_solver_info(folder, delete):

            # look for file
            if os.path.isfile(folder + '/solver.xml'):
                solver_path = folder + '/solver.xml'
            else:
                raise FileNotFoundError('Cannot find solver.xml in folder: ' + str(folder))

            # Parse file
            solver_tree = ET.tostring(ET.parse(solver_path).getroot())
            solver = xmltodict.parse(solver_tree)
            solver_dict = {}

            # convert to correct format
            for setting in solver['solver']:
                solver_dict[setting] = eval(solver['solver'][setting])

            # delete file
            if delete:
                os.remove(solver_path)

            return solver_dict

        def load_boundary(folder, delete):

            # look for file
            if os.path.isfile(folder + '/boundary_condition.xml'):
                boundary_path = folder + '/boundary_condition.xml'
            else:
                boundary_path = None

            if not boundary_path:
                return None

            else:
                # Parse file
                boundary_tree = ET.tostring(ET.parse(boundary_path).getroot())
                boundaries = xmltodict.parse(boundary_tree)
                boundary_dict = {}

                # convert to correct format
                for bc_key in boundaries['boundary_conditions'].keys():
                    boundary_dict[str(bc_key)] = {}

                    for bc in boundaries['boundary_conditions'][bc_key]:
                        if bc == 'flux':
                            fluxes = list(float(flux)
                                          for flux in boundaries['boundary_conditions'][bc_key][bc].split(','))
                            boundary_dict[bc_key][bc] = fluxes
                        else:
                            boundary_dict[bc_key][bc] = boundaries['boundary_conditions'][bc_key][bc]

                # delete file
                if delete:
                    os.remove(boundary_path)

                #print('load', boundary_dict)
                return boundary_dict

        # Load files and assign data to variables
        self.weather_dict = load_weather(self.folder, delete_after_load)
        self.trees_dict = load_tree(self.folder, delete_after_load)
        self.ground_dict = load_ground(self.folder, delete_after_load)
        self.mesh_path = load_mesh(self.folder)
        self.outputs = load_outputs(self.folder, delete_after_load)
        self.solver_settings = load_solver_info(self.folder, delete_after_load)
        self.boundary_dict = load_boundary(self.folder, delete_after_load)

        return True

    def mesh_to_cells(self, cmf_project, mesh_path, delete_after_load=True):
        """
        Takes a mesh and converts it into CMF cells
        :param mesh_path: Path to mesh file
        :param cmf_project: CMF project object
        :return: True
        """

        # Load mesh
        mesh = pm.load_mesh(mesh_path)
        mesh.enable_connectivity()

        # Initialize mesh data
        mesh.add_attribute('face_centroid')
        mesh.add_attribute('face_index')
        mesh.add_attribute('face_area')
        cen_pts = mesh.get_attribute('face_centroid')
        face_index = mesh.get_attribute('face_index')
        face_area = mesh.get_attribute('face_area')
        faces = mesh.faces
        vertices = mesh.vertices

        # Helper functions
        def face_vertices(face_index):
            """
            Returns the vertices of a face
            :param face_index: Face index (int)
            :return: v0, v1, v2
            """

            face = faces[int(face_index)]
            v0 = vertices[face[0]]
            v1 = vertices[face[1]]
            v2 = vertices[face[2]]

            return v0, v1, v2

        def face_face_edge(face0, face1):
            """
            Returns the width of the edge between to faces
            :param face0: Face index
            :param face1: Face index
            :return: float value with the edge with
            """

            # Get vertices
            v = []
            v0 = face_vertices(int(face0))
            v1 = face_vertices(int(face1))

            # Find out which edge is shared
            for vertex in v0:
                equal = np.equal(vertex, v1)
                if np.sum(equal) > 0:
                    v.append(vertex)
                else:
                    pass

            # Compute the width of the edge
            dx = abs(v[0][0] - v[1][0])
            dy = abs(v[0][1] - v[1][1])
            dz = abs(v[0][2] - v[1][2])
            edge_width = np.sqrt(dx**2 + dy**2 + dz**2)

            return edge_width

        # Construct centroid list
        centroids = []
        i = 0
        while i < len(cen_pts):
            for j in range(0, len(face_index)):
                centroids.append([face_index[j], np.array([cen_pts[i], cen_pts[i+1], cen_pts[i+2]])])
                i += 3

        # Create cells
        for i in range(0, len(centroids)):
            x, y, z = centroids[i][1]
            a = float(face_area[i])
            cmf_project.NewCell(x=float(x), y=float(y), z=float(z), area=a, with_surfacewater=True)

        # Connect cells
        for face in face_index:
            adjacent_faces = mesh.get_face_adjacent_faces(int(face))

            for adj in adjacent_faces:
                width = face_face_edge(face, adj)
                if width:
                    cmf_project[face].topology.AddNeighbor(cmf_project[adj], width)
                else:
                    pass

        if delete_after_load:
            os.remove(mesh_path)

        return True

    def add_tree(self, cmf_project, cell_index, property_dict):
        """Adds a tree to the model"""

        cell = cmf_project.cells[int(cell_index)]
        self.set_vegetation_properties(cell, property_dict)
        name = 'canopy_'+str(cell_index)
        cell.add_storage(name, 'C')

        cmf.Rainfall(cell.canopy, cell, False, True)
        cmf.Rainfall(cell.surfacewater, cell, True, False)
        cmf.RutterInterception(cell.canopy, cell.surfacewater, cell)
        cmf.CanopyStorageEvaporation(cell.canopy, cell.evaporation, cell)

        return True

    def set_vegetation_properties(self, cell_: cmf.Cell, property_dict: dict):
        cell_.vegetation.Height = float(property_dict['height'])
        cell_.vegetation.LAI = float(property_dict['lai'])
        cell_.vegetation.albedo = float(property_dict['albedo'])
        cell_.vegetation.CanopyClosure = float(property_dict['canopy_closure'])
        cell_.vegetation.CanopyParExtinction = float(property_dict['canopy_par'])
        cell_.vegetation.CanopyCapacityPerLAI = float(property_dict['canopy_capacity'])
        cell_.vegetation.StomatalResistance = float(property_dict['stomatal_res'])
        cell_.vegetation.RootDepth = float(property_dict['root_depth'])
        cell_.vegetation.fraction_at_rootdepth = float(property_dict['root_fraction'])
        cell_.vegetation.LeafWidth = float(property_dict['leaf_width'])

        return True

    def configure_cells(self, cmf_project: cmf.project, cell_properties_dict: dict):
        """Configure the cells"""

        # Helper functions
        def install_connections(cell_, evapotranspiration_method):

            # Install connections
            cell_.install_connection(cmf.Richards)
            cell_.install_connection(cmf.GreenAmptInfiltration)

            if evapotranspiration_method == 'penman_monteith':
                # Install Penman & Monteith method to calculate evapotranspiration_potential
                cell_.install_connection(cmf.PenmanMonteithET)

            elif evapotranspiration_method == 'shuttleworth_wallace':
                # Install Shuttleworth-Wallace method to calculate evapotranspiration
                cell_.install_connection(cmf.ShuttleworthWallace)

            return True

        def retention_curve(r_curve_: dict):
            """
            Converts a dict of retention curve parameters into a CMF van Genuchten-Mualem retention curve.
            :param r_curve_: dict
            :return: CMF retention curve
            """

            curve = cmf.VanGenuchtenMualem(r_curve_['K_sat'], r_curve_['phi'], r_curve_['alpha'], r_curve_['n'],
                                           r_curve_['m'])
            curve.l = r_curve_['l']

            return curve

        # Convert retention curve parameters into CMF retention curve
        r_curve = retention_curve(cell_properties_dict['retention_curve'])

        for cell_index in cell_properties_dict['face_indices']:
            cell = cmf_project.cells[int(float(cell_index))]

            # Add layers
            for i in range(0, len(cell_properties_dict['layers'])):
                cell.add_layer(float(cell_properties_dict['layers'][i]), r_curve)

            install_connections(cell, cell_properties_dict['et_method'])

            self.set_vegetation_properties(cell, cell_properties_dict['vegetation_properties'])

            if cell_properties_dict['manning']:
                cell.surfacewater.set_nManning(float(cell_properties_dict['manning']))

            if cell_properties_dict['puddle_depth']:
                cell.surfacewater.puddledepth = cell_properties_dict['puddle_depth']

            # Set initial saturation
            cell.saturated_depth = cell_properties_dict['saturated_depth']

        # Connect fluxes
        cmf.connect_cells_with_flux(cmf_project, cmf.Darcy)
        cmf.connect_cells_with_flux(cmf_project, cmf.KinematicSurfaceRunoff)

        return True

    def create_stream(self, shape, shape_param, outlet):
        """Create a stream"""
        # ShapeParam(Tri) = [length, bankSlope, x, y, z, intialWaterDepth]
        # ShapeParam(Rec) = [length, width, x, y, z, intialWaterDepth]
        reaches = []

        # Create stream
        if shape == 0:
            for i in range(len(shape_param)):
                reach_shape = cmf.TriangularReach(shape_param[i][0],shape_param[i][1])
                reaches.append([self.project.NewReach(shape_param[i][2], shape_param[i][3], shape_param[i][4], reach_shape, False)])
                reaches[-1].depth(shape_param[5])

                # Connect reaches
                if not reaches:
                    pass
                elif len(reaches) == len(shape_param):
                    channel_out = self.project.NewOutlet(outlet[0], outlet[1], outlet[2])
                    reaches[-1].set_downstream(channel_out)
                else:
                    reaches[-2].set_downstream(reaches[-1])

        elif shape == 1:
            for i in range(len(shape_param)):
                reach_shape = cmf.RectangularReach(shape_param[i][0],shape_param[i][1])
                reaches.append([self.project.NewReach(shape_param[i][2], shape_param[i][3], shape_param[i][4], reach_shape, False)])
                reaches[-1].depth(shape_param[5])

                # Connect reaches
                if not reaches:
                    pass
                elif len(reaches) == len(shape_param):
                    channel_out = self.project.NewOutlet(outlet[0], outlet[1], outlet[2])
                    reaches[-1].set_downstream(channel_out)
                else:
                    reaches[-2].set_downstream(reaches[-1])
        else:
            return None

    def create_weather(self, cmf_project):
        """Creates weather for the project"""

        # Helper functions
        def create_time_series(analysis_length, time_step=1.0):

            # Start date is the 1st of January 2017 at 00:00
            start = cmf.Time(1, 1, 2017, 0, 0)
            step = cmf.h * time_step

            # Create time series
            return cmf.timeseries(begin=start, step=step, count=analysis_length)

        def weather_to_time_series(weather):

            # Create time series
            t_series = create_time_series(self.solver_settings['analysis_length'])
            w_series = create_time_series(self.solver_settings['analysis_length'])
            rh_series = create_time_series(self.solver_settings['analysis_length'])
            sun_series = create_time_series(self.solver_settings['analysis_length'])
            rad_series = create_time_series(self.solver_settings['analysis_length'])
            rain_series = create_time_series(self.solver_settings['analysis_length'])
            ground_temp_series = create_time_series(self.solver_settings['analysis_length'])

            # add data
            for i in range(len(weather['temp'])):
                t_series[i] = (weather['temp'][i])
                w_series[i] = (weather['wind'][i])
                rh_series[i] = (weather['rel_hum'][i])
                sun_series[i] = (weather['sun'][i])
                rad_series[i] = (weather['rad'][i])
                rain_series[i] = (weather['rain'][i])
                ground_temp_series[i] = (weather['ground_temp'][i])

            return {'temp': t_series, 'wind': w_series, 'rel_hum': rh_series, 'sun': sun_series, 'rad': rad_series,
                    'rain': rain_series, 'ground_temp': ground_temp_series}

        def get_weather_for_cell(cell_id, project_weather_dict):
            # Initialize
            cell_weather_dict_ = {}
            location_dict = {}

            # Find weather matching cell ID
            for weather_type in project_weather_dict.keys():
                # Try for weather type having the same weather for all cells
                try:
                    cell_weather_dict_[weather_type] = project_weather_dict[weather_type]['all']

                # Accept that some have one for each cell
                except KeyError:
                    cell_weather_dict_[weather_type] = project_weather_dict[weather_type]['cell_' + str(cell_id)]

                # Accept latitude, longitude and time zone
                except TypeError:
                    location_dict[weather_type] = project_weather_dict[weather_type]

            # Convert to time series
            cell_weather_series = weather_to_time_series(cell_weather_dict_)

            return cell_weather_series, location_dict

        def create_weather_station(cmf_project_, cell_id, weather, location):
            # Add cell rainfall station to the project
            rain_station = cmf_project_.rainfall_stations.add(Name='cell_' + str(cell_id) + ' rain',
                                                              Data=weather['rain'],
                                                              Position=(0, 0, 0))

            # Add cell meteo station to the project
            meteo_station = cmf_project_.meteo_stations.add_station(name='cell_' + str(cell_id) + ' weather',
                                                                    position=(0, 0, 0),
                                                                    latitude=location['latitude'],
                                                                    longitude=location['longitude'],
                                                                    tz=location['time_zone'])

            meteo_station.T = weather['temp']
            meteo_station.Tmax = meteo_station.T.reduce_max(meteo_station.T.begin, cmf.day)
            meteo_station.Tmin = meteo_station.T.reduce_min(meteo_station.T.begin, cmf.day)
            meteo_station.Windspeed = weather['wind']
            meteo_station.rHmean = weather['rel_hum']
            meteo_station.Sunshine = weather['sun']
            meteo_station.Rs = weather['rad']
            meteo_station.Tground = weather['ground_temp']

            return rain_station, meteo_station

        def connect_weather_to_cells(cell_, rain_station, meteo_station):
            rain_station.use_for_cell(cell_)
            meteo_station.use_for_cell(cell_)

        # Run create weather helper functions
        for cell_index in range(0, len(cmf_project.cells)):
            cell = cmf_project.cells[cell_index]

            cell_weather_dict, project_location = get_weather_for_cell(cell_index, self.weather_dict)
            cell_rain, cell_meteo = create_weather_station(cmf_project, cell_index, cell_weather_dict, project_location)
            connect_weather_to_cells(cell, cell_rain, cell_meteo)

    def create_boundary_conditions(self, cmf_project):

        # Helper functions
        def set_inlet(boundary_condition_, cmf_project_):

            # Get the correct cell and layer
            if int(boundary_condition_['layer']) == 0:
                cell_layer = cmf_project_.cells[int(boundary_condition_['cell'])].surfacewater
            else:
                cell_layer = cmf_project_.cells[
                                                int(boundary_condition_['cell'])].layers[
                                                int(boundary_condition_['layer'])]

            # Create inlet
            inlet = cmf.NeumannBoundary.create(cell_layer)
            #print('set_inlet', inlet)

            # if flux is a list then convert to time series
            if len(boundary_condition_['flux']) > 1:
                inlet_flux = np.array(list(float(flux)
                                           for flux in boundary_condition_['flux']))

                inlet.set_flux(cmf.timeseries.from_array(begin=datetime(2017, 1, 1),
                                                         step=timedelta(hours=1),
                                                         data=inlet_flux))
            else:
                inlet.flux = boundary_condition_['flux'][0]

        def set_outlet(boundary_condition_, index_, cmf_project_):
            x, y, z = boundary_condition_['location'].split(',')
            outlet = cmf_project_.NewOutlet('outlet_' + str(index_), float(x), float(y), float(z))
            cell = cmf_project_.cells[int(boundary_condition_['cell'])]

            if boundary_condition_['layer'] == 'all':
                for l in cell.layers:
                    # create a Darcy connection with 10m flow width between each soil layer and the outlet
                    cmf.Darcy(l, outlet, FlowWidth=float(boundary_condition_['flow_width']))
                cmf.KinematicSurfaceRunoff(cell.surfacewater, outlet, float(boundary_condition_['flow_width']))
            elif boundary_condition_['layer'] == 0:
                cmf.KinematicSurfaceRunoff(cell.surfacewater, outlet, float(boundary_condition_['flow_width']))
            else:
                layer = cell.layers[int(boundary_condition_['layer'])]
                cmf.Darcy(layer, outlet, FlowWidth=float(boundary_condition_['flow_width']))

        def set_boundary_condition(boundary_condition_, bc_index, cmf_project_):
            print('set_boundary_condition', boundary_condition_)
            if boundary_condition_['type'] == 'inlet':
                set_inlet(boundary_condition_, cmf_project_)
            elif boundary_condition_['type'] == 'outlet':
                set_outlet(boundary_condition_, bc_index, cmf_project_)
            else:
                raise ValueError('Boundary type should be either inlet or outlet. Given value was: '
                                 + str(boundary_condition_['type']))

        # Loop through the boundary conditions and assign them
        for index, boundary_condition in enumerate(self.boundary_dict.keys()):
            #print('\nloop')
            #print(index)
            #print(boundary_condition)
            set_boundary_condition(self.boundary_dict[boundary_condition], index, cmf_project)

    def config_outputs(self, cmf_project):
        """Function to set up result gathering dictionary"""

        out_dict = {}

        for cell_index in range(0, len(cmf_project.cells)):
            cell_name = 'cell_' + str(cell_index)
            out_dict[cell_name] = {}

            # Set all cell related outputs
            for cell_output in self.outputs['cell']:
                out_dict[cell_name][str(cell_output)] = []

            for layer_index in range(0, len(cmf_project.cells[cell_index].layers)):
                layer_name = 'layer_' + str(layer_index)
                out_dict[cell_name][layer_name] = {}

                # Set all layer related outputs
                for layer_output in self.outputs['layer']:
                    out_dict[cell_name][layer_name][str(layer_output)] = []

        self.results = out_dict

    def gather_results(self, cmf_project, time):

        for cell_index in range(0, len(cmf_project.cells)):
            cell_name = 'cell_' + str(cell_index)

            for out_key in self.results[cell_name].keys():

                # Collect cell related results
                if out_key == 'evaporation':
                    evap = cmf_project.cells[cell_index].evaporation

                    flux_at_time = 0
                    for flux, node in evap.fluxes(time):
                        flux_at_time += flux

                    self.results[cell_name][out_key].append(flux_at_time)

                    # sw = cmf.ShuttleworthWallace(cmf_project.cells[cell_index])
                    # sw.refresh(time)

                    # evap_sum = sw.AIR + sw.GER + sw.GIR
                    # self.results[cell_name][out_key].append(evap_sum)

                if out_key == 'transpiration':
                    transp = cmf_project.cells[cell_index].transpiration

                    flux_at_time = 0
                    for flux, node in transp.fluxes(time):
                        flux_at_time += flux

                    self.results[cell_name][out_key].append(flux_at_time)
                    # self.results[cell_name][out_key].append(cmf_project.cells[cell_index].transpiration)
                    # self.results[cell_name][out_key].append(cmf.ShuttleworthWallace(cmf_project.cells[cell_index]).ATR_sum)

                if out_key == 'surface_water_volume':
                    volume = cmf_project.cells[cell_index].get_surfacewater().volume
                    self.results[cell_name][out_key].append(volume)

                if out_key == 'surface_water_flux':
                    water = cmf_project.cells[cell_index].get_surfacewater()

                    flux_and_node = []
                    for flux, node in water.fluxes(time):
                        flux_and_node.append((flux, node))

                    self.results[cell_name][out_key].append(flux_and_node)

                if out_key == 'heat_flux':
                    self.results[cell_name][out_key].append(cmf_project.cells[cell_index].heat_flux(time))

                if out_key == 'aerodynamic_resistance':
                    self.results[cell_name][out_key].append(
                        cmf_project.cells[cell_index].get_aerodynamic_resistance(time))

            for layer_index in range(0, len(cmf_project.cells[cell_index].layers)):
                layer_name = 'layer_' + str(layer_index)

                for out_key in self.results[cell_name][layer_name].keys():

                    # Collect layer related results

                    if out_key == 'potential':
                        self.results[cell_name][layer_name][out_key].append(
                            cmf_project.cells[cell_index].layers[layer_index].potential)

                    if out_key == 'theta':
                        self.results[cell_name][layer_name][out_key].append(
                            cmf_project.cells[cell_index].layers[layer_index].theta)

                    if out_key == 'volumetric_flux':
                        layer = cmf_project.cells[cell_index].layers[layer_index].get_3d_flux(time)

                        """
                        flux_and_node = []
                        for flux, node in layer.fluxes(time):
                            flux_and_node.append((flux, node))
                        """

                        self.results[cell_name][layer_name][out_key].append(layer)

                    if out_key == 'volume':
                        self.results[cell_name][layer_name][out_key].append(
                            cmf_project.cells[cell_index].layers[layer_index].volume)

                    if out_key == 'wetness':
                        self.results[cell_name][layer_name][out_key].append(
                            cmf_project.cells[cell_index].layers[layer_index].wetness)

                    # else:
                    #    raise ValueError('Unknown result to collect. Result to collect was: ' + str(out_key))

    def print_solver_time(self, solver_time, start_time, last_time, step):

        if self.solver_settings['verbosity']:
            now = datetime.now()
            elapsed_time = now - start_time
            time_per_step = elapsed_time.total_seconds()/(step+1)
            time_left = timedelta(seconds=(time_per_step * (self.solver_settings['analysis_length'] - step)))

            # Print statements:
            solver_timer_print = 'Solver Time: ' + str(solver_time)
            elapsed_time_print = 'Elapsed Time: ' + str(elapsed_time)
            current_time_step_print = 'Current Time Step: ' + str(now - last_time)
            estimated_time_left_print = 'Estimated Time Left: ' + str(time_left)
            print(solver_timer_print, '\t',
                  elapsed_time_print, '\t',
                  current_time_step_print, '\t',
                  estimated_time_left_print)

            return now

        else:
            if step == 0:
                print('Simulation started')

            elif step == self.solver_settings['analysis_length']:
                print('Simulation ended')

    def solve(self, cmf_project, tolerance):
        """Solves the model"""

        # Create solver, set time and set up results
        solver = cmf.CVodeIntegrator(cmf_project, tolerance)
        solver.t = cmf.Time(1, 1, 2017)
        self.config_outputs(cmf_project)

        # Save initial conditions to results
        self.gather_results(cmf_project, solver.t)

        # Set timer
        start_time = datetime.now()
        step = 0
        last = start_time

        # Run solver and save results at each time step
        for t in solver.run(solver.t,
                            solver.t + timedelta(hours=self.solver_settings['analysis_length']),
                            timedelta(hours=float(self.solver_settings['time_step']))):

            self.gather_results(cmf_project, t)
            last = self.print_solver_time(t, start_time, last, step)
            step += 1

        self.solved = True
        return True

    def save_results(self):
        """Saves the computed results to a xml file"""

        if not self.solved:
            print('Project not solved!')
            return None

        else:
            result_root = ET.Element('result')

            for cell in self.results.keys():
                cell_tree = ET.SubElement(result_root, str(cell))

                for result_key in self.results[cell].keys():
                    if result_key.startswith('layer'):
                        layer_tree = ET.SubElement(cell_tree, str(result_key))

                        for layer_result_key in self.results[cell][result_key].keys():
                            data = ET.SubElement(layer_tree, str(layer_result_key))
                            data.text = str(self.results[cell][result_key][layer_result_key])

                    else:
                        data = ET.SubElement(cell_tree, str(result_key))
                        data.text = str(self.results[cell][result_key])

            result_tree = ET.ElementTree(result_root)
            result_tree.write(self.folder + '/results.xml', xml_declaration=True)

            return True

    def run_model(self):
        """Runs the model with everything"""

        # Initialize project
        project = cmf.project()
        self.load_cmf_files()

        # Add cells and properties to them
        self.mesh_to_cells(project, self.mesh_path)

        for key in self.ground_dict.keys():
            self.configure_cells(project, self.ground_dict[str(key)])

        if self.trees_dict:
            for key in self.trees_dict.keys():
                self.add_tree(project,
                              self.trees_dict[str(key)]['face_index'],
                              self.trees_dict[str(key)]['property'])

        # Create the weather
        self.create_weather(project)

        # Create boundary conditions
        if self.boundary_dict:
            self.create_boundary_conditions(project)

        # Run solver
        self.solve(project, self.solver_settings['tolerance'])

        # Save the results
        self.save_results()

        return project
