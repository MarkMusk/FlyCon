import requests

def readMETAR(lat=False, lon=False, ICAO=False) -> False or dict:
    """
    Reads METAR data from METAR-TAF using a ICAO registered airport, if ICAO is a valid airport.
    Reads METAR data from METAR-TAF using nearest ICAO registered airport to (lat, lon), if (lat, lon) is a valid location.
    If error occurs -> False
    """
    TOKEN = 'BxqbOVGBtbgRohXpncK4CWhCmU18f1sQ'
    LANG = 'en-US'

    if not(lat and lon) and not(ICAO):
        return False
    elif lat and lon:
        response = requests.get(f"https://api.metar-taf.com/metar?api_key={TOKEN}&v=2.3&{LANG}=en-US&latitude={lat}&longitude={lon}")
        response_json = response.json()
        if not(response_json['status']):
            return False
        else:
            return response_json
    elif ICAO:
        response = requests.get(f"https://api.metar-taf.com/metar?api_key={TOKEN}&v=2.3&{LANG}=en-US&id={ICAO}")
        response_json = response.json()
        if not(response_json['status']):
            return False
        else:
            return response_json
    else:
        return False

def formatData(radio='icao', searchTo='cyyz', searchFrom='cyyz', deicing=None) -> dict:
    """
    Returns data in dictionairy format:
    {"contentTo": contentTo, "contentFrom": contentFrom, "warnings": warningsList, "opacities": opacities(v=totalV)}
    """
    print(f"RADIO= {radio}, SEARCHTo= {searchTo}, SEARCHFrom= {searchFrom} ")
    if searchTo != '' and searchFrom != '':
        if radio == 'icao':
            contentTo = readMETAR(ICAO=searchTo)
            contentFrom = readMETAR(ICAO=searchFrom)
            if not(contentTo) or not(contentFrom):
                return False
            elif not(contentTo['metar']) or not(contentFrom['metar']):
                return "NOMETAR"
        elif radio == 'latlon':
            lat1, lon1 = searchTo.replace(' ', '').split(',')
            lat2, lon2 = searchFrom.replace(' ', '').split(',')
            contentTo = readMETAR(lat=lat1, lon=lon1)
            contentFrom = readMETAR(lat=lat2, lon=lon2)
            if not(contentTo) or not(contentFrom):
                return False
        if contentTo == contentFrom:
            warning = warnings(data=contentTo, to=False, airport=contentFrom['airport']['name'])
            warningsList = warning[1]
            totalV = warning[0]
        else:
            warningFrom = warnings(data=contentFrom, to=False, airport=contentFrom['airport']['name'])
            warningTo = warnings(data=contentTo, to=True, airport=contentTo['airport']['name'])
            warningsList = warningFrom[1] + warningTo[1]
            totalV = warningFrom[0] + warningTo[0]
        return {"contentTo": contentTo, "contentFrom": contentFrom, "warnings": warningsList, "opacities": opacities(v=totalV)}

def opacities(v: int or None) -> list:
    o = ['0.3' for i in range(5)]
    if not(v):
        return o
    elif v >= 12:
        o[0] = 1
    elif v >= 9:
        o[1] = 1
    elif v >= 6:
        o[2] = 1
    elif v >= 3:
        o[3] = 1
    elif v == 0:
        o[4] = 1
    return o

def warnings(data: dict, to: bool, airport: str) -> tuple:
    v = 0
    warnings = []
    start, end = "starting location", "ending location"
    location =  f"at {data['airport']['name']} ({data['airport']['iata']}) ({end if to else start})"
    print(f"LOCATION {data}")
    if data['airport']['metar']:
        if not(data['metar']['cavok']):
            v += 6
            warnings.append(f"CAVOK (Clouds and Visibility Ok) is false, clouds + visibility is not ideal {location}")
        if data['metar']['wind_speed'] >= 30:
            warnings.append(f"Wind speed is ≥ 30 kts (wind speed is {data['metar']['wind_speed']} knts)")
        if data['metar']['clouds'][0]['height'] == None:
            v += 0
        elif 5000 <= data['metar']['clouds'][0]['height'] < 6000:
            v += 7
            warnings.append(f"Clouds are over ≥ 5000 m and < 6000 m (clouds are at {data['metar']['clouds'][0]['height']} meters) {location}")
        elif 4000 <= data['metar']['clouds'][0]['height'] < 5000:
            v += 8
            warnings.append(f"Clouds are over ≥ 4000 m and < 5000 m (clouds are at {data['metar']['clouds'][0]['height']} meters) {location}")
        elif 3000 <= data['metar']['clouds'][0]['height'] < 4000:
            v += 9
            warnings.append(f"Clouds are over ≥ 3000 m and < 4000 m (clouds are at {data['metar']['clouds'][0]['height']} meters) {location}")
        elif 2000 <= data['metar']['clouds'][0]['height'] < 3000:
            v += 11
            warnings.append(f"Clouds are over ≥ 2000 m and < 3000 m (clouds are at {data['metar']['clouds'][0]['height']} meters) {location}")
        elif 1000 <= data['metar']['clouds'][0]['height'] < 2000:
            v += 11
            warnings.append(f"Clouds are over ≥ 1000 m and < 2000 m (clouds are at {data['metar']['clouds'][0]['height']} meters) {location}")
        elif 1000 > data['metar']['clouds'][0]['height']:
            v += 12
            warnings.append(f"Clouds are over > 1000 m (clouds are at {data['metar']['clouds'][0]['height']} meters) at {airport} {location}")
        v //= 3
        return (v, warnings)
    else:
        return (6, [f"No METAR available at {airport}"])

print(formatData())
{'status': True, 'credits': -1, 'airport': {'id': 'CYYZ', 'iata': 'YYZ', 'name': 'Lester B. Pearson International Airport', 'name_translated': 'Lester B. Pearson International Airport', 'city_name': 'Eringate-Centennial-West Deane', 'admin1': 'Ontario', 'admin2': 'Toronto county', 'country_id': 'CA', 'country_name': 'Canada', 'lat': 43.6772, 'lng': -79.6306, 'metar': True, 'taf': True, 'timezone': -14400, 'fir': None, 'elevation': 569, 'type': 15, 'last_notam': 1678455766}, 'metar': {'cavok': False, 'ceiling': 2300, 'ceiling_color': '#0080f0', 'clouds': [{'id': 0, 'height': 2300, 'report': 'Overcast clouds', 'amount': 'OVC'}], 'code': 'MVFR', 'code_color': '#0080f0', 'colour_state': None, 'dewpoint': -6, 'dewpoint_exact': None, 'humidity': 69, 'is_day': True, 'observed': 1678647600, 'qnh': 1014.2, 'raw': 'METAR CYYZ 121900Z 11008KT 15SM OVC023 M01/M06 A2995 RMK SC8 SH DIST NW SLP152', 'recent_weather_report': None, 'remarks': ['SLP152: Sea level pressure is 1015.2 hPa (29.98 inHg)', 'SC8 SH DIST NW'], 'runway_condition': [], 'runway_visibility': [], 'snoclo': False, 'station_id': 'CYYZ', 'sunrise': 1678620953, 'sunset': 1678663238, 'temperature': -1, 'temperature_exact': None, 'trends': [], 'vertical_visibility': None, 'visibility': 24140.1, 'visibility_sign': None, 'visibility_color': '#28a745', 'visibility_min': None, 'visibility_min_direction': None, 'warnings': [], 'weather': 'Overcast', 'weather_image': 'overcast', 'weather_report': None, 'wind_color': '#28a745', 'wind_dir': 110, 'wind_dir_max': None, 'wind_dir_min': None, 'wind_gust': None, 'wind_speed': 8, 'ws_all': None, 'ws_runways': None, 'id': 399111108}, 'runways': [{'id_l': '6L', 'id_h': '24R', 'hdg_l': 57, 'hdg_h': 237, 'in_use': 57, 'xwnd': 6.4, 'hwnd': 4.8}, {'id_l': '6R', 'id_h': '24L', 'hdg_l': 57, 'hdg_h': 237, 'in_use': 57, 'xwnd': 6.4, 'hwnd': 4.8}, {'id_l': '5', 'id_h': '23', 'hdg_l': 57, 'hdg_h': 237, 'in_use': 57, 'xwnd': 6.4, 'hwnd': 4.8}, {'id_l': '15L', 'id_h': '33R', 'hdg_l': 147, 'hdg_h': 327, 'in_use': 147, 'xwnd': -4.8, 'hwnd': 6.4}, {'id_l': '15R', 'id_h': '33L', 'hdg_l': 147, 'hdg_h': 327, 'in_use': 147, 'xwnd': -4.8, 'hwnd': 6.4}, {'id_l': '15', 'id_h': '33', 'hdg_l': 147, 'hdg_h': 327, 'in_use': 147, 'xwnd': -4.8, 'hwnd': 6.4}], 'stations': [{'id': 'CYYZ', 'name': 'Lester B. Pearson International Airport', 'taf': True}, {'id': 'CXTO', 'name': 'Toronto City', 'taf': False}, {'id': 'CYTZ', 'name': 'Billy Bishop Toronto City Centre Airport', 'taf': True}, {'id': 'CWWB', 'name': 'Burlington Piers', 'taf': False}, {'id': 'CXHM', 'name': 'Hamilton Rbg Cs', 'taf': False}, {'id': 'CXVN', 'name': 'Vineland (au8)', 'taf': False}]}