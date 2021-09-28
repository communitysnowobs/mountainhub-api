from collections import OrderedDict
from datetime import datetime, timezone
import time

import requests
import pandas as pd

_MHAPI_URL = 'https://api.mountainhub.com/timeline'


def _remove_empty_params(dict):
    """Returns copy of dictionary with empty values removed.

    Keyword arguments:
    dict -- Dictionary to process
    """
    return {k: v for k, v in dict.items() if v is not None}


def _make_bbox(bbox):
    """Formats bounding box for use in MountainHub API.

    Keyword arguments:
    box -- Dictionary used to construct bounding box
    """
    if bbox is None:
        return {}
    return {
        'north_east_lat': bbox['latmax'],
        'north_east_lng': bbox['lonmax'],
        'south_west_lat': bbox['latmin'],
        'south_west_lng': bbox['lonmin']
    }


def datetime_to_timestampms(dt):
    """Converts datetime object to unix timestamp in milliseconds.

    Keyword arguments:
    date -- Datetime object to convert
    """
    if dt is None:
        return dt
    # TODO: Verify that this conversion is correct (assumes UTC, not local time)
    return int(time.mktime(dt.timetuple())) * 1000


def timestampms_to_datetime(timestamp):
    """Converts unix timestamp in milliseconds to timezone-aware UTC datetime object.

    Keyword arguments:
    timestamp -- Timestamp to convert
    """
    if timestamp is None:
        return timestamp
    return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)


def parse_snow(record):
    """Parses results record returned by MountainHub API.
     Returns standard OrderedDict dictionary.

    Keyword arguments:
    record -- results record from JSON returned by MountainHub API
    """
    obs = record['observation']
    actor = record['actor']
    details = obs.get('details', [{}])
    snow_depth_str = (details[0].get('snowpack_depth')
                      if (len(details) > 0 and details[0] is not None)
                      else None)
    snow_depth = (float(snow_depth_str)
                  if (snow_depth_str is not None and snow_depth_str != 'undefined')
                  else None)
    description = (obs['description']
                   if ('description' in obs and obs['description'] is not None)
                   else '')
    
    # Remap record structure
    return OrderedDict(
        id=obs['_id'],
        # reported_at is an epoch timestamp, in UTC
        datetime_utc=timestampms_to_datetime(int(obs['reported_at'])),
        latitude=obs['location'][1],
        longitude=obs['location'][0],
        author_name=actor.get('full_name') or actor.get('fullName'),
        obs_type=obs['type'],
        snow_depth=snow_depth,
        description=description
    )


def snow_data(publisher='all', obs_type='snow_conditions,snowpack_test',
              limit=1000, start=None, end=None, bbox=None, filter=True):
    """Retrieves snow depth data (cm) from MountainHub API.

    Arguments:
        publisher -- 'all', 'pro' (professional submitters), etc
        obs_type -- Filters to only specific observation types.
            Can be an individual value or a comma-separated string of multiple values.
            Only snow depth values are processed, but accepted obs_type values are:
            snowpack_test, snow_conditions, weather, camera, dangerous_wildlife,
            other_hazard, point_of_interest, water_hazard, trail_conditions,
            trip_report, incident, avalanche
        limit -- Maximum number of records to return (default 1000)
        start -- Start datetime to return results from, as datetime object
        end -- End datetime to return results from, as datetime object
        box -- Bounding box to restrict results, specified as dictionary with items
            latmax, lonmax, latmin, lonmin
        filter -- Flag indicating whether entries with no snow depth data
            should be filtered out.

    Returns:
        df -- Pandas DataFrame with these columns: observation id,
            datetime_utc, latitude, longitude, author_name,
            obs_type, snow_depth (in cm), description
    """
    # TODO: Confirm that start and end should be in UTC

    # Build API request, then make request
    header = {'Accept-version': '1'}
    params = _remove_empty_params({
        'publisher': publisher,
        'obs_type': obs_type,
        'limit': limit,
        'since': datetime_to_timestampms(start),
        'before': datetime_to_timestampms(end),
        **_make_bbox(bbox)
    })

    response = requests.get(_MHAPI_URL, params=params, headers=header)
    data = response.json()

    if 'results' not in data or len(data['results']) == 0:
        print("No results found.")
        return None

    # Parse request
    records = data['results']
    parsed = [parse_snow(record) for record in records]

    # Convert to Pandas dataframe and optionally drop (filter out) results
    # with no snow depth data
    df = pd.DataFrame.from_records(parsed)
    if filter:
        df = df.dropna(subset=['snow_depth'])

    # Filtered dataframe has no numeric snow_depth values
    if len(df) == 0:
        print("No snow_depth results found.")
        return None

    return df
