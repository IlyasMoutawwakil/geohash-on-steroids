import numpy as np
# import numba as nb
from numba import njit, types
from math import log10

@njit(fastmath=True)
def base32_to_int(s: types.char) -> types.uint8:
    """
    Returns the equivalent value of a base 32 character.
    Surprisingly, on Numba this approach is faster than all the others.
    """
    res = ord(s) - 48
    if res > 9: res -= 40
    if res > 16: res -= 1
    if res > 18: res -= 1
    if res > 20: res -= 1
    return res

@njit(fastmath=True)
def nb_decode_exactly(geohash: types.string) -> types.Tuple:
    """
    Decode the geohash to its exact values, including the error
    margins of the result.  Returns four float values: latitude,
    longitude, the plus/minus error for latitude (as a positive
    number) and the plus/minus error for longitude (as a positive
    number).
    """

    lat_interval_neg, lat_interval_pos, lon_interval_neg, lon_interval_pos = -90, 90, -180, 180
    lat_err, lon_err = 90, 180
    is_even = True
    for c in geohash:
        cd = base32_to_int(c)
        for mask in (16, 8, 4, 2, 1):
            if is_even:  # adds longitude info
                lon_err /= 2
                if cd & mask:
                    lon_interval_neg = (lon_interval_neg +
                                        lon_interval_pos) / 2
                else:
                    lon_interval_pos = (lon_interval_neg +
                                        lon_interval_pos) / 2
            else:  # adds latitude info
                lat_err /= 2
                if cd & mask:
                    lat_interval_neg = (lat_interval_neg +
                                        lat_interval_pos) / 2
                else:
                    lat_interval_pos = (lat_interval_neg +
                                        lat_interval_pos) / 2
            is_even = not is_even
    lat = (lat_interval_neg + lat_interval_pos) / 2
    lon = (lon_interval_neg + lon_interval_pos) / 2
    return lat, lon, lat_err, lon_err

@njit(fastmath=True)
def nb_point_decode(geohash: types.string) -> types.Tuple:
    """
    Decode geohash, returning two float with latitude and longitude containing only relevant digits.
    """

    lat, lon, lat_err, lon_err = nb_decode_exactly(geohash)
    # Format to the number of decimals that are known
    lat_dec = max(1, round(-log10(lat_err))) - 1
    lon_dec = max(1, round(-log10(lon_err))) - 1
    lat = round(lat, lat_dec)
    lon = round(lon, lon_dec)

    return lat, lon

@njit(fastmath=True, parallel=True)
def nb_vector_decode(geohashes: types.Array) -> types.Tuple:
    """
    Decode geohashes, returning two Arrays of floats with latitudes and longitudes containing only relevant digits.
    """

    n = len(geohashes)
    lats = np.empty(n)
    lons = np.empty(n)
    for i, geohash in enumerate(geohashes):
        lat, lon, lat_err, lon_err = nb_decode_exactly(str(geohash))
        # Format to the number of decimals that are known
        lat_dec = max(1, round(-log10(lat_err))) - 1
        lon_dec = max(1, round(-log10(lon_err))) - 1
        lats[i] = round(lat, lat_dec)
        lons[i] = round(lon, lon_dec)

    return lats, lons