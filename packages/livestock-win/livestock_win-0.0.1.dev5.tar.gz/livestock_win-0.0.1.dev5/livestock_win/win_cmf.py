__author__ = "Christian Kongsgaard"
__license__ = "MIT"
__version__ = "0.0.1"

# -------------------------------------------------------------------------------------------------------------------- #
# Imports

# Module imports
import os
import xml.etree.ElementTree as ET
import xmltodict
import numpy as np
import ast
import json

# Livestock imports


# -------------------------------------------------------------------------------------------------------------------- #
# Livestock Windows Misc Functions


def cmf_results(path):
    files = os.listdir(path)
    result_path = None
    lookup_path = None

    for f in files:
        if f.startswith('results'):
            result_path = path + '/' + f
        elif f.startswith('result_lookup'):
            lookup_path = path + '/' + f

    # Read look up file
    file_obj = open(lookup_path, 'r')
    line = file_obj.readline()
    lookup_dict = eval(line)

    for lookup_key in lookup_dict.keys():
        if lookup_key.startswith('cell'):
            cell_results(lookup_dict[lookup_key], result_path, path)
        elif lookup_key.startswith('layer'):
            layer_results(lookup_dict[lookup_key], result_path, path)

    return True


def cell_results(looking_for, result_file, folder):
    """Processes cell results"""

    # Initialize
    result_tree = ET.tostring(ET.parse(result_file).getroot())
    results = xmltodict.parse(result_tree)
    results_to_save = []

    # Find results
    for cell in results['result'].keys():
        if looking_for == 'evapotranspiration':
            evapo = np.array(eval(results['result'][cell]['evaporation']))
            transp = np.array(eval(results['result'][cell]['transpiration']))
            evapotransp = evapo + transp
            results_to_save.append(list(evapotransp))

        else:
            for result in results['result'][cell]:
                if result == looking_for:
                    if result == 'heat_flux':
                        # Covert heat flux from MJ/(m2*day) to W/m2h
                        flux_mj = np.array(eval(results['result'][cell][result]))
                        flux_wh = flux_mj/0.0864
                        results_to_save.append(list(flux_wh))

                    else:
                        results_to_save.append(eval(results['result'][cell][result]))

    # Write files
    file_path = folder + '/' + looking_for + '.csv'
    csv_file = open(file_path, 'w')
    for result_ in results_to_save:
        csv_file.write(','.join(str(r)
                                for r in result_)+'\n')
    csv_file.close()

    return True


def layer_results(looking_for, result_file, folder):
    """Processes layer results"""

    # Initialize
    result_tree = ET.tostring(ET.parse(result_file).getroot())
    results = xmltodict.parse(result_tree)
    results_to_save = []

    # find results
    for cell in results['result'].keys():

        for cell_result in results['result'][cell].keys():
            if cell_result.startswith('layer'):
                for layer_result in results['result'][cell][cell_result]:
                    if layer_result == looking_for:
                        if layer_result == 'volumetric_flux':
                            results_to_save.append(convert_cmf_points(results['result']
                                                                      [cell]
                                                                      [cell_result]
                                                                      [layer_result]))

                        else:
                            results_to_save.append(eval(results['result'][cell][cell_result][layer_result]))

        results_to_save.append([cell])

    # Write files
    file_path = folder + '/' + looking_for + '.csv'
    csv_file = open(file_path, 'w')
    for result_ in results_to_save:
        csv_file.write(','.join(str(r) for r in result_)+'\n')
    csv_file.close()

    return True


def convert_cmf_points(points):
    # convert to list
    point_list = points[1:-1]
    point_tuples = []

    for tup in point_list.split(' '):
        try:
            tup1 = ast.literal_eval(tup[9:-1])
        except SyntaxError:
            tup1 = ast.literal_eval(tup[9:])
        point_tuples.append(' '.join(str(e) for e in tup1))

    return point_tuples


def surface_flux_results(path):

    # Helper functions
    def read_files(path_):

        # get flux configuration file
        if os.path.isfile(path_ + '/flux_config.txt'):
            file_obj = open(path_ + '/flux_config.txt', 'r')
            flux_lines = file_obj.readlines()
            file_obj.close()
            os.remove(path_ + '/flux_config.txt')

            flux = {'run_off': ast.literal_eval(flux_lines[0].strip()),
                    'rain': ast.literal_eval(flux_lines[1].strip()),
                    'evapotranspiration': ast.literal_eval(flux_lines[2].strip()),
                    'infiltration': ast.literal_eval(flux_lines[3].strip())
                    }
        else:
            raise FileNotFoundError('Cannot find flux_config.txt in folder: ' + str(path_))

        # get center points file
        if os.path.isfile(path_ + '/center_points.txt'):
            file_obj = open(path_ + '/center_points.txt', 'r')
            point_lines = file_obj.readlines()
            file_obj.close()
            os.remove(path_ + '/center_points.txt')

            # process points
            center_points_ = []
            for line in point_lines:
                point = []
                for p in line.strip().split(','):
                    point.append(float(p))
                center_points_.append(np.array(point))

        else:
            raise FileNotFoundError('Cannot find center_points.txt in folder: ' + str(path_))

        return flux, center_points_

    def get_flux_result(path_: str)-> dict:

        # helper
        def convert_to_list(string_: str)-> list:

            time_steps = []
            current_time = []
            flux_pair = []
            for element in string_[1:-1].split(','):
                if element.startswith('['):
                    flux_pair.append(float(element[2:]))

                elif element.startswith(' ['):
                    flux_pair.append(float(element[3:]))

                elif element.startswith(' ('):
                    flux_pair.append(float(element[2:]))

                elif element.endswith(')'):
                    flux_pair.append(element[1:-1])
                    current_time.append(flux_pair)
                    flux_pair = []

                elif element.endswith(']'):
                    flux_pair.append(element[1:-2])
                    current_time.append(flux_pair)
                    time_steps.append(current_time)
                    current_time = []
                    flux_pair = []

            return time_steps

        result_file = path_ + '/results.xml'

        # make check for file
        if not os.path.isfile(result_file):
            raise FileNotFoundError('Cannot find results.xml in folder: ' + str(path_))

        # Initialize
        result_tree = ET.tostring(ET.parse(result_file).getroot())
        results = xmltodict.parse(result_tree)
        results_to_save = {}

        # find results
        for cell_ in results['result'].keys():
            results_to_save[cell_] = convert_to_list(str(results['result'][cell_]['surface_water_flux']))

        return results_to_save

    def process_flux(flux_dict_: dict, flux_config_: dict, center_points_: list)-> dict:

        # helper functions
        def get_wanted_fluxes(flux_tuple: list, center_points__)-> np.array:
            # delete entries where the flux is 0
            if flux_tuple[0] == 0:
                return np.array([])

            else:
                # delete entries that we don't want, if flux is not zero
                if flux_tuple[1].startswith('{Rain'):
                    if not flux_config_['rain']:
                        return np.array([])
                    else:
                        return np.array([0, 0, flux_tuple[0]])

                elif flux_tuple[1].startswith('{Evapo'):
                    if not flux_config_['evapotranspiration']:
                        return np.array([])
                    else:
                         return np.array([0, 0, flux_tuple[0]])

                elif flux_tuple[1].startswith('{Layer'):
                    if not flux_config_['infiltration']:
                        return np.array([])
                    else:
                        return np.array([0, 0, -flux_tuple[0]])

                elif flux_tuple[1].startswith('{Surface'):
                    if not flux_config_['run_off']:
                        return np.array([])
                    else:
                        if flux_tuple[0] > 0:
                            return np.array([])
                        else:
                            destination_cell = int(flux_tuple[1].split('#')[1][:-1])
                            local_cell = int(cell_.split('_')[1])
                            vector_ = center_points__[destination_cell] - center_points__[local_cell]
                            normalized_vector = vector_ / np.linalg.norm(vector_)
                            return normalized_vector * abs(flux_tuple[0])

        cell_vectors = {}
        for cell_ in flux_dict_.keys():
            time_vectors = []
            for time_step in range(0, len(flux_dict_[cell_])):
                vectors = []

                for flux in flux_dict_[cell_][time_step]:
                    vector = get_wanted_fluxes(flux, center_points_)
                    if len(vector) > 0:
                        vectors.append(vector)

                # Compute average vector
                if not vectors:
                    # if no vectors return [0, 0, 0]
                    time_vectors.append([0, 0, 0])
                else:
                    time_vectors.append(list(np.average(vectors, axis=0)))

            # add time vectors to cell
            cell_vectors[cell_] = time_vectors

        return cell_vectors

    # load files
    flux_config, center_points = read_files(path)
    flux_results = get_flux_result(path)

    processed_vectors = process_flux(flux_results, flux_config, center_points)

    # write file
    result_obj = open(path + '/surface_flux_result.txt', 'w')
    for cell in processed_vectors.keys():
        line = ''
        for point in processed_vectors[cell]:
            line += ','.join([str(p) for p in point]) + '\t'
        result_obj.write(line + '\n')

    result_obj.close()

    return True
