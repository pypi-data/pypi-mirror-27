# -*- coding: utf-8 -*-
#
# Copyright (c) 2014, 2015, 2017
#
# Author(s):
#
#   Panu Lahtinen <panu.lahtinen@fmi.fi>
#   Martin Raspaud <martin.raspaud@smhi.se>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''Helper functions for Trollduction
'''

import numpy as np
import os
import xml_read
import datetime as dt
import re
import logging
from ConfigParser import ConfigParser
import errno
import shutil

from mpop.projector import get_area_def
from pyresample.geometry import Boundary

LOGGER = logging.getLogger(__name__)


def read_config_file(fname, config_item=None):
    '''Read config file to dictionary.
    '''

    endswith = os.path.splitext(fname)[1]
    if endswith == ".xml":
        return xml_read.parse_xml(xml_read.get_root(fname))
    elif endswith in ['.ini', '.cfg']:
        config = ConfigParser()
        config.read(fname)
        conf_dict = dict(config.items(config_item))
        conf_dict["config_file"] = fname
        conf_dict["config_item"] = config_item
        return conf_dict
    else:
        raise NotImplementedError("Can only parse xml and .ini config files"
                                  "for now")


def get_maximum_extent(area_def_names):
    '''Get maximum extend needed to produce all defined areas.
    '''
    maximum_area_extent = [None, None, None, None]
    for area in area_def_names:
        extent = get_area_def(area)

        if maximum_area_extent[0] is None:
            maximum_area_extent = list(extent.area_extent)
        else:
            if maximum_area_extent[0] > extent.area_extent[0]:
                maximum_area_extent[0] = extent.area_extent[0]
            if maximum_area_extent[1] > extent.area_extent[1]:
                maximum_area_extent[1] = extent.area_extent[1]
            if maximum_area_extent[2] < extent.area_extent[2]:
                maximum_area_extent[2] = extent.area_extent[2]
            if maximum_area_extent[3] < extent.area_extent[3]:
                maximum_area_extent[3] = extent.area_extent[3]

    return maximum_area_extent


def get_maximum_extent_ll(area_def_names):
    '''Get maximum extend needed to produce all the defined areas
    given in *area_def_names*.
    '''
    maximum_area_extent = [None, None, None, None]

    for area in area_def_names:
        area_def = get_area_def(area['definition'])

        lons, lats = get_area_boundaries(area_def)
        left_lon, down_lat, right_lon, up_lat = \
            np.min(lons.side4), \
            np.min(lats.side3), \
            np.max(lons.side2), \
            np.max(lats.side1)

        if maximum_area_extent[0] is None:
            maximum_area_extent = [left_lon, down_lat, right_lon, up_lat]
        else:
            if maximum_area_extent[0] > left_lon:
                maximum_area_extent[0] = left_lon
            if maximum_area_extent[1] > down_lat:
                maximum_area_extent[1] = down_lat
            if maximum_area_extent[2] < right_lon:
                maximum_area_extent[2] = right_lon
            if maximum_area_extent[3] < up_lat:
                maximum_area_extent[3] = up_lat

    return maximum_area_extent


def get_maximum_ll_borders(area_def_names):
    '''Get maximum extend needed to produce all the defined areas
    given in *area_def_names*.
    '''
    maximum_area_extent = [None, None, None, None]

    for area in area_def_names:
        area_def = get_area_def(area['definition'])

        lons, lats = get_area_boundaries(area_def)
        left_lon, down_lat, right_lon, up_lat = \
            np.min(lons.side4), \
            np.min(lats.side3), \
            np.max(lons.side2), \
            np.max(lats.side1)

        if maximum_area_extent[0] is None:
            maximum_area_extent = [left_lon, down_lat, right_lon, up_lat]
        else:
            if maximum_area_extent[0] > left_lon:
                maximum_area_extent[0] = left_lon
            if maximum_area_extent[1] > down_lat:
                maximum_area_extent[1] = down_lat
            if maximum_area_extent[2] < right_lon:
                maximum_area_extent[2] = right_lon
            if maximum_area_extent[3] < up_lat:
                maximum_area_extent[3] = up_lat

    return maximum_area_extent


def get_area_boundaries(area_def):
    '''Get area boundaries from area definition.
    '''

    # upper boundary
    lonlat = np.array([area_def.get_lonlat(0, i)
                       for i in range(area_def.x_size)])
    up_lons = lonlat[:, 0]
    up_lats = lonlat[:, 1]

    # lower boundary
    lonlat = np.array([area_def.get_lonlat(area_def.y_size - 1, i)
                       for i in range(area_def.x_size)])
    down_lons = lonlat[:, 0]
    down_lats = lonlat[:, 1]

    # left boundary
    lonlat = np.array([area_def.get_lonlat(i, 0)
                       for i in range(area_def.y_size)])
    left_lons = lonlat[:, 0]
    left_lats = lonlat[:, 1]

    # right boundary
    lonlat = np.array([area_def.get_lonlat(i, area_def.x_size - 1)
                       for i in range(area_def.y_size)])
    right_lons = lonlat[:, 0]
    right_lats = lonlat[:, 1]

    return (Boundary(up_lons, right_lons, down_lons, left_lons),
            Boundary(up_lats, right_lats, down_lats, left_lats))


def get_indices_from_boundaries(boundary_lons, boundary_lats,
                                lons, lats, radius_of_influence):
    """Find relevant indices from grid boundaries using the
    winding number theorem"""

    valid_index = _get_valid_index(boundary_lons.side1, boundary_lons.side2,
                                   boundary_lons.side3, boundary_lons.side4,
                                   boundary_lats.side1, boundary_lats.side2,
                                   boundary_lats.side3, boundary_lats.side4,
                                   lons, lats, radius_of_influence)

    return valid_index


def get_angle_sum(lons_side1, lons_side2, lons_side3, lons_side4):
    '''Calculate angle sum for winding number theorem.  Note that all
    the sides need to be connected, that is:

    lons_side[-1] == lons_side2[0],
    ...
    lons_side4[-1] == lons_side1[0]
    '''
    angle_sum = 0
    for side in (lons_side1, lons_side2, lons_side3, lons_side4):
        side_diff = np.sum(np.diff(side))
        idxs, = np.where(np.abs(side_diff) > 180)
        if idxs:
            side_diff[idxs] = (np.abs(side_diff[idxs]) - 360) * \
                np.sign(side_diff[idxs])
        angle_sum += np.sum(side_diff)

    return angle_sum


def _get_valid_index(lons_side1, lons_side2, lons_side3, lons_side4,
                     lats_side1, lats_side2, lats_side3, lats_side4,
                     lons, lats, radius_of_influence):
    """Find relevant indices from grid boundaries using the
    winding number theorem"""

    earth_radius = 6370997.0

    # Coarse reduction of data based on extrema analysis of the boundary
    # lon lat values of the target grid
    illegal_lons = (((lons_side1 < -180) | (lons_side1 > 180)).any() or
                    ((lons_side2 < -180) | (lons_side2 > 180)).any() or
                    ((lons_side3 < -180) | (lons_side3 > 180)).any() or
                    ((lons_side4 < -180) | (lons_side4 > 180)).any())

    illegal_lats = (((lats_side1 < -90) | (lats_side1 > 90)).any() or
                    ((lats_side2 < -90) | (lats_side2 > 90)).any() or
                    ((lats_side3 < -90) | (lats_side3 > 90)).any() or
                    ((lats_side4 < -90) | (lats_side4 > 90)).any())

    if illegal_lons or illegal_lats:
        # Grid boundaries are not safe to operate on
        return np.ones(lons.size, dtype=np.bool)

    # Find sum angle sum of grid boundary
    angle_sum = get_angle_sum(lons_side1, lons_side2,
                              lons_side3[::-1], lons_side4[::-1])

    # Buffer min and max lon and lat of interest with radius of interest
    lat_min = min(lats_side1.min(), lats_side2.min(),
                  lats_side3.min(), lats_side4.min())
    lat_min_buffered = lat_min - np.degrees(float(radius_of_influence) /
                                            earth_radius)
    lat_max = max(lats_side1.max(), lats_side2.max(), lats_side3.max(),
                  lats_side4.max())
    lat_max_buffered = lat_max + np.degrees(float(radius_of_influence) /
                                            earth_radius)

    max_angle_s2 = max(abs(lats_side2.max()), abs(lats_side2.min()))
    max_angle_s4 = max(abs(lats_side4.max()), abs(lats_side4.min()))
    lon_min_buffered = lons_side4.min() - \
        np.degrees(float(radius_of_influence) /
                   (np.sin(np.radians(max_angle_s4)) * earth_radius))

    lon_max_buffered = lons_side2.max() + \
        np.degrees(float(radius_of_influence) /
                   (np.sin(np.radians(max_angle_s2)) * earth_radius))

    # From the winding number theorem follows:
    # angle_sum possiblilities:
    # -360: area covers north pole
    #  360: area covers south pole
    #    0: area covers no poles
    # else: area covers both poles
    if round(angle_sum) == -360:
        LOGGER.debug("Area covers north pole")
        # Covers NP
        valid_index = (lats >= lat_min_buffered)
    elif round(angle_sum) == 360:
        LOGGER.debug("Area covers south pole")
        # Covers SP
        valid_index = (lats <= lat_max_buffered)
    elif round(angle_sum) == 0:
        LOGGER.debug("Area covers no poles")
        # Covers no poles
        valid_lats = (lats >= lat_min_buffered) * (lats <= lat_max_buffered)

        if lons_side2.min() > lons_side4.max():
            # No date line crossing
            valid_lons = (lons >= lon_min_buffered) * \
                (lons <= lon_max_buffered)
        else:
            # Date line crossing
            seg1 = (lons >= lon_min_buffered) * (lons <= 180)
            seg2 = (lons <= lon_max_buffered) * (lons >= -180)
            valid_lons = seg1 + seg2

        valid_index = valid_lats * valid_lons
    else:
        LOGGER.debug("Area covers both poles")
        # Covers both poles, don't reduce
        return True
        # valid_index = np.ones(lons.size, dtype=np.bool)

    return valid_index


def overlapping_timeinterval(start_end_times, timelist):
    """From a list of start and end times check if the current time interval
    overlaps with one or more"""

    starttime, endtime = start_end_times
    for tstart, tend in timelist:
        if ((tstart <= starttime and tend > starttime) or
                (tstart < endtime and tend >= endtime)):
            return tstart, tend
        elif (tstart >= starttime and tend <= endtime):
            return tstart, tend

    return False


def _conv_datetime(stri, convdef, transform):
    """
    Convert the string *stri* to the given datetime
    conversion definition *convdef*.
    Do some transformation of the parsed data when
    *transform* is defined
    """
    result = dt.datetime.strptime(stri, convdef)
    if transform:
        params = _parse_align_time_transform(transform)
        if params:
            result = align_time(result,
                                dt.timedelta(minutes=params[0]),
                                dt.timedelta(minutes=params[1]),
                                params[2])
    return result


def create_aligned_datetime_var(var_pattern, info_dict):
    """
    uses *var_patterns* like "{time:%Y%m%d%H%M|align(15)}"
    to new datetime including support for temporal
    alignment (Ceil/Round a datetime object to a multiple of a timedelta.
    Useful to equalize small time differences in name of files
    belonging to the same timeslot)
    """
    mtch = re.match(
        '{(.*?)(!(.*?))?(\\:(.*?))?(\\|(.*?))?}',
        var_pattern)

    if mtch is None:
        return None

    # parse date format pattern
    key = mtch.groups()[0]
    # format_spec = mtch.groups()[4]
    transform = mtch.groups()[6]
    date_val = info_dict[key]

    if not isinstance(date_val, dt.datetime):
        return None

    # only for datetime types
    res = date_val
    if transform:
        align_params = _parse_align_time_transform(transform)
        if align_params:
            res = align_time(
                date_val,
                dt.timedelta(minutes=align_params[0]),
                dt.timedelta(minutes=align_params[1]),
                align_params[2])

    return res


def _parse_align_time_transform(transform_spec):
    """
    Parse the align-time transformation string "align(15,0,-1)"
    and returns *(steps, offset, intv_add)*
    """
    match = re.search('align\\((.*)\\)', transform_spec)
    if match:
        al_args = match.group(1).split(',')
        steps = int(al_args[0])
        if len(al_args) > 1:
            offset = int(al_args[1])
        else:
            offset = 0
        if len(al_args) > 2:
            intv_add = int(al_args[2])
        else:
            intv_add = 0
        return (steps, offset, intv_add)
    else:
        return None


def align_time(input_val, steps=dt.timedelta(minutes=5),
               offset=dt.timedelta(minutes=0), intervals_to_add=0):
    """
    Ceil/Round a datetime object to a multiple of a timedelta.
    Useful to equalize small time differences in name of files
    belonging to the same timeslot
    """
    try:
        stepss = steps.total_seconds()
    # Python 2.6 compatibility hack
    except AttributeError:
        stepss = steps.days * 86400. + \
            steps.seconds + steps.microseconds * 1e-6
    val = input_val - offset
    vals = (val - val.min).seconds
    result = val - dt.timedelta(seconds=(vals - (vals // stepss) * stepss))
    result = result + (intervals_to_add * steps)
    return result


def parse_aliases(config):
    '''Parse aliases from the config.

    Aliases are given in the config as:

    {'alias_<name>': 'value:alias'}, or
    {'alias_<name>': 'value1:alias1|value2:alias2'},

    where <name> is the name of the key which value will be
    replaced. The later form is there to support several possible
    substitutions (eg. '2' -> '9' and '3' -> '10' in the case of MSG).

    '''
    aliases = {}

    for key in config:
        if 'alias' in key:
            alias = config[key]
            new_key = key.replace('alias_', '')
            if '|' in alias or ':' in alias:
                parts = alias.split('|')
                aliases2 = {}
                for part in parts:
                    key2, val2 = part.split(':')
                    aliases2[key2] = val2
                alias = aliases2
            aliases[new_key] = alias
    return aliases


def eval_default(expression, default_res=None):
    """Calls eval on expression and returns default_res if it throws
    exceptions
    """
    if default_res is None:
        default_res = expression
    try:
        return eval(expression)
    except:
        pass
    return default_res


def get_uri_from_message(msg, area_def_names=None):
    """Get URI from posttroll message."""

    if msg.type == "file":
        uri = msg.data['uri']
    elif msg.type == "dataset":
        uri = [mda['uri'] for mda in msg.data['dataset']]
    elif msg.type == 'collection':
        if not msg.data['collection_area_id'] in area_def_names:
            LOGGER.warning('Collection does not contain data for '
                           'current areas: %s', str(area_def_names))
            return None
        if 'dataset' in msg.data['collection'][0]:
            uri = []
            for dataset in msg.data['collection']:
                uri.extend([mda['uri'] for mda in dataset['dataset']])
        else:
            uri = [mda['uri'] for mda in msg.data['collection']]
    else:
        LOGGER.warning("Can't run on %s messages", msg.type)
        return None
    # TODO collections and collections of datasets

    return uri


def get_file_format(fname):
    """Get fileformat from the filename ending"""
    # we should have more info on format...
    fformat = os.path.splitext(fname)[1][1:]
    if fformat.startswith("tif"):
        fformat = "TIFF"
    elif fformat.startswith("png"):
        fformat = "PNG"
    elif fformat.startswith("jp"):
        fformat = "JPEG"
    elif fformat.startswith("nc"):
        fformat = "NetCDF4"
    elif fformat in ["hdf", "h5"]:
        fformat = "HDF5"

    return fformat


def add_fformat_metadata(info, fformat, obj_info):
    """Add metadata to *info* dict based on the file format *fformat*"""
    if fformat not in ["NetCDF4", "HDF5", "TIFF"]:
        info["format"] = "raster"
        info["data_processing_level"] = "2"
        info["product_name"] = obj_info["product_name"]
    elif fformat == "TIFF":
        info["format"] = "GeoTIFF"
        info["data_processing_level"] = "2"
        info["product_name"] = obj_info["product_name"]
    elif fformat == "NetCDF4":
        info["format"] = "CF"
        info["data_processing_level"] = "1b"
        info["product_name"] = "dump"
    elif fformat == "HDF5":
        info["format"] = "PPS"
        info["data_processing_level"] = "3"
        info["product_name"] = "cloudproduct"

    return info


def link_or_copy(src, dst, tmpdst=None, retry=1):
    """Create a hardlink from *src* to *dst*, or if that fails, copy.
    """
    if src == dst:
        LOGGER.warning("Trying to copy a file over itself: %s", src)
        return
    try:
        os.link(src, dst)
        if tmpdst is not None:
            os.remove(tmpdst)
    except OSError as err:
        if err.errno not in [errno.EXDEV]:
            LOGGER.exception("Could not link: %s -> %s", src, dst)
            return
        try:
            if tmpdst is not None:
                shutil.copy(src, tmpdst)
                os.rename(tmpdst, dst)
            else:
                shutil.copy(src, dst)
        except shutil.Error:
            LOGGER.exception("Something went wrong in copying a file")
        except IOError as err:
            LOGGER.info("Error copying file: %s", str(err))
            if retry:
                LOGGER.info("Retrying...")
                link_or_copy(src, dst, tmpdst, retry - 1)
            else:
                LOGGER.exception("Could not copy: %s -> %s", src, dst)


def thumbnail(filename, thname, size, fformat):
    """Create a thumbnail image and save it.
    """
    from PIL import Image
    img = Image.open(filename)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(thname, fformat)


def hash_color(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#':
        colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    r_col, g_col, b_col = colorstring[:2], colorstring[2:4], colorstring[4:]
    r_col, g_col, b_col = [int(n, 16) for n in (r_col, g_col, b_col)]
    return (r_col, g_col, b_col)
