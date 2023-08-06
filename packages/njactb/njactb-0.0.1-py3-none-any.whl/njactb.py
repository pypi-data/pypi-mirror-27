#!/usr/bin/env python3

import re
import json
import requests
import lxml.html
from urllib.parse import urljoin

__version__ = "0.0.1"

BASE_URL = 'http://tax1.co.monmouth.nj.us/cgi-bin/'

COUNTIES = {
    "ATLANTIC": "0101",
    "BERGEN": "0201",
    "BURLINGTON": "0301",
    "CAMDEN": "0401",
    "CAPE MAY": "0501",
    "CUMBERLAND": "0601",
    "ESSEX": "0701",
    "GLOUCESTER": "0801",
    "HUDSON": "0901",
    "HUNTERDON": "1001",
    "MERCER": "1101",
    "MIDDLESEX": "1201",
    "MONMOUTH": "1301",
    "MORRIS": "1401",
    "PASSAIC": "1601",
    "SALEM": "1701",
    "SOMERSET": "1801",
    "SUSSEX": "1901",
    "UNION": "2001",
    "WARREN": "2101"
}

DISTRICTS = {
    "ATLANTIC": {
        "ABSECON": "0101",
        "ATLANTIC CITY": "0102",
        "BRIGANTINE": "0103",
        "BUENA": "0104",
        "BUENA VISTA": "0105",
        "CORBIN": "0106",
        "EGG HARBOR CITY": "0107",
        "EGG HARBOR TWP": "0108",
        "ESTELL MANOR": "0109",
        "FOLSOM": "0110",
        "GALLOWAY": "0111",
        "HAMILTON": "0112",
        "HAMMONTON": "0113",
        "LINWOOD": "0114",
        "LONGPORT": "0115",
        "MARGATE": "0116",
        "MULLICA": "0117",
        "NORTHFIELD": "0118",
        "PLEASANTVILLE": "0119",
        "PORT REPUBLIC": "0120",
        "SOMERS POINT": "0121",
        "VENTNOR": "0122",
        "WEYMOUTH": "0123",
        "ALL": "0100"
    },
    "BERGEN": {
        "ALLENDALE": "0201",
        "ALPINE": "0202",
        "BERGENFIELD": "0203",
        "BOGOTA": "0204",
        "CARLSTADT": "0205",
        "CLIFFSIDE": "0206",
        "CLOSTER": "0207",
        "CRESSKILL": "0208",
        "DEMAREST": "0209",
        "DUMONT": "0210",
        "EAST RUTHERFORD": "0212",
        "EDGEWATER": "0213",
        "ELMWOOD PARK": "0211",
        "EMERSON": "0214",
        "ENGLEWOOD": "0215",
        "ENGLEWOOD CLIFFS": "0216",
        "FAIR LAWN": "0217",
        "FAIRVIEW": "0218",
        "FORT LEE": "0219",
        "FRANKLIN LAKES": "0220",
        "GARFIELD": "0221",
        "GLEN ROCK": "0222",
        "HACKENSACK": "0223",
        "HARRINGTON": "0224",
        "HASBROUCK HEIGHTS": "0225",
        "HAWORTH": "0226",
        "HILLSDALE": "0227",
        "HOHOKUS": "0228",
        "LEONIA": "0229",
        "LITTLE FERRY": "0230",
        "LODI": "0231",
        "LYNDHURST": "0232",
        "MAHWAH": "0233",
        "MAYWOOD": "0234",
        "MIDLAND PARK": "0235",
        "MONTVALE": "0236",
        "MOONACHIE": "0237",
        "NEW MILFORD": "0238",
        "NORTH ARLINGTON": "0239",
        "NORTHVALE": "0240",
        "NORWOOD": "0241",
        "OAKLAND": "0242",
        "OLD TAPPAN": "0243",
        "ORADELL": "0244",
        "PALISADES PARK": "0245",
        "PARAMUS": "0246",
        "PARK RIDGE": "0247",
        "RAMSEY": "0248",
        "RIDGEFIELD": "0249",
        "RIDGEFIELD PARK": "0250",
        "RIDGEWOOD": "0251",
        "RIVER EDGE": "0252",
        "RIVERVALE": "0253",
        "ROCHELLE PARK": "0254",
        "ROCKLEIGH": "0255",
        "RUTHERFORD": "0256",
        "SADDLE BROOK": "0257",
        "SADDLE RIVER": "0258",
        "SOUTH HACKENSACK": "0259",
        "TEANECK": "0260",
        "TENAFLY": "0261",
        "TETERBORO": "0262",
        "UPPER SADDLE RIVER": "0263",
        "WALDWICK": "0264",
        "WALLINGTON": "0265",
        "WASHINGTON": "0266",
        "WESTWOOD": "0267",
        "WOODCLIFF LAKE": "0268",
        "WOOD RIDGE": "0269",
        "WYCKOFF": "0270",
        "ALL": "0200"
    },
    "BURLINGTON": {
        "BASS RIVER": "0301",
        "BEVERLY": "0302",
        "BORDENTOWN CITY": "0303",
        "BORDENTOWN TWP": "0304",
        "BURLINGTON CITY": "0305",
        "BURLINGTON TWP": "0306",
        "CHESTERFIELD": "0307",
        "CINNAMINSON": "0308",
        "DELANCO": "0309",
        "DELRAN": "0310",
        "EASTAMPTON": "0311",
        "EDGEWATER PARK": "0312",
        "EVESHAM": "0313",
        "FIELDSBORO": "0314",
        "FLORENCE": "0315",
        "HAINESPORT": "0316",
        "LUMBERTON": "0317",
        "MANSFIELD": "0318",
        "MAPLE SHADE": "0319",
        "MEDFORD TWP": "0320",
        "MEDFORD LAKES": "0321",
        "MOORESTOWN": "0322",
        "MOUNT HOLLY": "0323",
        "MOUNT LAUREL": "0324",
        "NEW HANOVER": "0325",
        "NORTH HANOVER": "0326",
        "PALMYRA": "0327",
        "PEMBERTON BORO": "0328",
        "PEMBERTON TWP": "0329",
        "RIVERSIDE": "0330",
        "RIVERTON": "0331",
        "SHAMONG": "0332",
        "SOUTHAMPTON": "0333",
        "SPRINGFIELD": "0334",
        "TABERNACLE": "0335",
        "WASHINGTON": "0336",
        "WESTAMPTON": "0337",
        "WILLINGBORO": "0338",
        "WOODLAND": "0339",
        "WRIGHTSTOWN": "0340",
        "ALL": "0300"
    },
    "CAMDEN": {
        "AUDUBON": "0401",
        "AUDUBON PARK": "0402",
        "BARRINGTON": "0403",
        "BELLMAWR": "0404",
        "BERLIN BOROUGH": "0405",
        "BERLIN TOWNSHIP": "0406",
        "BROOKLAWN": "0407",
        "CAMDEN CITY": "0408",
        "CHERRY HILL": "0409",
        "CHESILHURST": "0410",
        "CLEMENTON": "0411",
        "COLLINGSWOOD": "0412",
        "GIBBSBORO": "0413",
        "GLOUCESTER CITY": "0414",
        "GLOUCESTER TOWNSHIP": "0415",
        "HADDON TOWNSHIP": "0416",
        "HADDONFIELD": "0417",
        "HADDON HEIGHTS": "0418",
        "HI NELLA": "0419",
        "LAUREL SPRINGS": "0420",
        "LAWNSIDE": "0421",
        "LINDENWOLD": "0422",
        "MAGNOLIA": "0423",
        "MERCHANTVILLE": "0424",
        "MOUNT EPHRAIM": "0425",
        "OAKLYN": "0426",
        "PENNSAUKEN": "0427",
        "PINE HILL": "0428",
        "PINE VALLEY": "0429",
        "RUNNEMEDE": "0430",
        "SOMERDALE": "0431",
        "STRATFORD": "0432",
        "TAVISTOCK": "0433",
        "VOORHEES": "0434",
        "WATERFORD": "0435",
        "WINSLOW": "0436",
        "WOODLYNNE": "0437",
        "ALL": "0400"
    },
    "CAPE MAY": {
        "AVALON": "0501",
        "CAPE MAY CITY": "0502",
        "CAPE MAY POINT": "0503",
        "DENNIS TOWNSHIP": "0504",
        "LOWER TOWNSHIP": "0505",
        "MIDDLE TOWNSHIP": "0506",
        "NORTH WILDWOOD": "0507",
        "OCEAN CITY": "0508",
        "SEA ISLE CITY": "0509",
        "STONE HARBOR": "0510",
        "UPPER TOWNSHIP": "0511",
        "WEST CAPE MAY": "0512",
        "WEST WILDWOOD": "0513",
        "WILDWOOD": "0514",
        "WILDWOOD CREST": "0515",
        "WOODBINE": "0516",
        "ALL": "0500"
    },
    "CUMBERLAND": {
        "BRIDGETON": "0601",
        "COMMERCIAL": "0602",
        "DEERFIELD": "0603",
        "DOWNE": "0604",
        "FAIRFIELD": "0605",
        "GREENWICH": "0606",
        "HOPEWELL": "0607",
        "LAWRENCE": "0608",
        "MAURICE RIVER": "0609",
        "MILLVILLE": "0610",
        "SHILOH": "0611",
        "STOW CREEK": "0612",
        "UPPER DEERFIELD": "0613",
        "VINELAND": "0614",
        "ALL": "0600"
    },
    "ESSEX": {
        "BELLEVILLE": "0701",
        "BLOOMFIELD": "0702",
        "CALDWELL BORO": "0703",
        "CEDAR GROVE": "0704",
        "EAST ORANGE": "0705",
        "ESSEX FELLS": "0706",
        "FAIRFIELD": "0707",
        "GLEN RIDGE": "0708",
        "IRVINGTON": "0709",
        "LIVINGSTON": "0710",
        "MAPLEWOOD": "0711",
        "MILLBURN": "0712",
        "MONTCLAIR": "0713",
        "NEWARK": "0714",
        "NORTH CALDWELL": "0715",
        "NUTLEY": "0716",
        "ORANGE": "0717",
        "ROSELAND": "0718",
        "SOUTH ORANGE": "0719",
        "VERONA": "0720",
        "WEST CALDWELL": "0721",
        "WEST ORANGE": "0722",
        "ALL": "0700"
    },
    "GLOUCESTER": {
        "CLAYTON": "0801",
        "DEPTFORD": "0802",
        "EAST GREENWICH": "0803",
        "ELK": "0804",
        "FRANKLIN": "0805",
        "GLASSBORO": "0806",
        "GREENWICH": "0807",
        "HARRISON": "0808",
        "LOGAN": "0809",
        "MANTUA": "0810",
        "MONROE": "0811",
        "NATIONAL PARK": "0812",
        "NEWFIELD": "0813",
        "PAULSBORO": "0814",
        "PITMAN": "0815",
        "SOUTH HARRISON": "0816",
        "SWEDESBORO": "0817",
        "WASHINGTON": "0818",
        "WENONAH": "0819",
        "WEST DEPTFORD": "0820",
        "WESTVILLE": "0821",
        "WOODBURY CITY": "0822",
        "WOODBURY HEIGHTS": "0823",
        "WOOLWICH": "0824",
        "ALL": "0800"
    },
    "HUDSON": {
        "BAYONNE": "0901",
        "EAST NEWARK": "0902",
        "GUTTENBERG": "0903",
        "HARRISON": "0904",
        "HOBOKEN": "0905",
        "JERSEY CITY": "0906",
        "KEARNY": "0907",
        "NORTH BERGEN": "0908",
        "SECAUCUS": "0909",
        "UNION CITY": "0910",
        "WEEHAWKEN": "0911",
        "WEST NEW YORK": "0912",
        "ALL": "0900"
    },
    "HUNTERDON": {
        "ALEXANDRIA": "1001",
        "BETHLEHEM": "1002",
        "BLOOMSBURY": "1003",
        "CALIFON": "1004",
        "CLINTON TOWN": "1005",
        "CLINTON TOWNSHIP": "1006",
        "DELAWARE": "1007",
        "EAST AMWELL": "1008",
        "FLEMINGTON": "1009",
        "FRANKLIN": "1010",
        "FRENCHTOWN": "1011",
        "GLEN GARDNER": "1012",
        "HAMPTON": "1013",
        "HIGH BRIDGE": "1014",
        "HOLLAND": "1015",
        "KINGWOOD": "1016",
        "LAMBERTVILLE": "1017",
        "LEBANON BOROUGH": "1018",
        "LEBANON TOWNSHIP": "1019",
        "MILFORD": "1020",
        "RARITAN TOWNSHIP": "1021",
        "READINGTON": "1022",
        "STOCKTON": "1023",
        "TEWKSBURY": "1024",
        "UNION TOWNSHIP": "1025",
        "WEST AMWELL": "1026",
        "ALL": "1000"
    },
    "MERCER": {
        "EAST WINDSOR": "1101",
        "EWING": "1102",
        "HAMILTON": "1103",
        "HIGHTSTOWN": "1104",
        "HOPEWELL BOROUGH": "1105",
        "HOPEWELL TOWNSHIP": "1106",
        "LAWRENCE": "1107",
        "PENNINGTON": "1108",
        "PRINCETON BOROUGH": "1109",
        "PRINCETON TOWNSHIP": "1110",
        "TRENTON": "1111",
        "ROBBINSVILLE TOWNSHIP": "1112",
        "WEST WINDSOR": "1113",
        "PRINCETON": "1114",
        "ALL": "1100"
    },
    "MIDDLESEX": {
        "CARTERET": "1201",
        "CRANBURY": "1202",
        "DUNELLEN": "1203",
        "EAST BRUNSWICK": "1204",
        "EDISON": "1205",
        "HELMETTA": "1206",
        "HIGHLAND": "1207",
        "JAMESBURG": "1208",
        "METUCHEN": "1209",
        "MIDDLESEX": "1210",
        "MILLTOWN": "1211",
        "MONROE": "1212",
        "NEW BRUNSWICK": "1213",
        "NORTH BRUNSWICK": "1214",
        "OLD BRIDGE": "1215",
        "PERTH AMBOY": "1216",
        "PISCATAWAY": "1217",
        "PLAINSBORO": "1218",
        "SAYREVILLE": "1219",
        "SOUTH AMBOY": "1220",
        "SOUTH BRUNSWICK": "1221",
        "SOUTH PLAINFIELD": "1222",
        "SOUTH RIVER": "1223",
        "SPOTSWOOD": "1224",
        "WOODBRIDGE": "1225",
        "ALL": "1200"
    },
    "MONMOUTH": {
        "ABERDEEN": "1301",
        "ALLENHURST": "1302",
        "ALLENTOWN": "1303",
        "ASBURY PARK": "1304",
        "ATLANTIC HIGHLANDS": "1305",
        "AVON-BY-THE-SEA": "1306",
        "BELMAR": "1307",
        "BRADLEY BEACH": "1308",
        "BRIELLE": "1309",
        "COLTS NECK": "1310",
        "DEAL": "1311",
        "EATONTOWN": "1312",
        "ENGLISHTOWN": "1313",
        "FAIR HAVEN": "1314",
        "FARMINGDALE": "1315",
        "FREEHOLD BORO": "1316",
        "FREEHOLD TOWNSHIP": "1317",
        "HAZLET": "1318",
        "HIGHLANDS": "1319",
        "HOLMDEL": "1320",
        "HOWELL": "1321",
        "INTERLAKEN": "1322",
        "KEANSBURG": "1323",
        "KEYPORT": "1324",
        "LITTLE SILVER": "1325",
        "LOCH ARBOUR": "1326",
        "LONG BRANCH": "1327",
        "MANALAPAN": "1328",
        "MANASQUAN": "1329",
        "MARLBORO": "1330",
        "MATAWAN": "1331",
        "MIDDLETOWN": "1332",
        "MILLSTONE": "1333",
        "MONMOUTH BEACH": "1334",
        "NEPTUNE TOWNSHIP": "1335",
        "NEPTUNE CITY": "1336",
        "OCEAN TOWNSHIP": "1337",
        "OCEANPORT": "1338",
        "RED BANK": "1339",
        "ROOSEVELT": "1340",
        "RUMSON": "1341",
        "SEA BRIGHT": "1342",
        "SEA GIRT": "1343",
        "SHREWSBURY BORO": "1344",
        "SHREWSBURY TOWNSHIP": "1345",
        "LAKE COMO BORO": "1346",
        "SPRING LAKE BORO": "1347",
        "SPRING LAKE HEIGHTS": "1348",
        "TINTON FALLS": "1349",
        "UNION BEACH": "1350",
        "UPPER FREEHOLD": "1351",
        "WALL TOWNSHIP": "1352",
        "WEST LONG BRANCH": "1353",
        "ALL": "1300"
    },
    "MORRIS": {
        "BOONTON TOWN": "1401",
        "BOONTON TOWNSHIP": "1402",
        "BUTLER": "1403",
        "CHATHAM BOROUGH": "1404",
        "CHATHAM TOWNSHIP": "1405",
        "CHESTER BOROUGH": "1406",
        "CHESTER TOWNSHIP": "1407",
        "DENVILLE": "1408",
        "DOVER": "1409",
        "EAST HANOVER": "1410",
        "FLORHAM PARK": "1411",
        "HANOVER": "1412",
        "HARDING": "1413",
        "JEFFERSON": "1414",
        "KINNELON": "1415",
        "LINCOLN PARK": "1416",
        "LONG HILL": "1430",
        "MADISON": "1417",
        "MENDHAM BOROUGH": "1418",
        "MENDHAM TOWNSHIP": "1419",
        "MINE HILL": "1420",
        "MONTVILLE": "1421",
        "MORRIS PLAINS": "1423",
        "MORRIS TOWNSHIP": "1422",
        "MORRISTOWN": "1424",
        "MOUNTAIN LAKES": "1425",
        "MT ARLINGTON": "1426",
        "MT OLIVE": "1427",
        "NETCONG": "1428",
        "PARSIPPANY": "1429",
        "PEQUANNOCK": "1431",
        "RANDOLPH": "1432",
        "RIVERDALE": "1433",
        "ROCKAWAY BOROUGH": "1434",
        "ROCKAWAY TOWNSHIP": "1435",
        "ROXBURY": "1436",
        "VICTORY GARDENS": "1437",
        "WASHINGTON": "1438",
        "WHARTON": "1439",
        "ALL": "1400"
    },
    "PASSAIC": {
        "BLOOMINGDALE": "1601",
        "CLIFTON": "1602",
        "HALEDON": "1603",
        "HAWTHORNE": "1604",
        "LITTLE FALLS": "1605",
        "NORTH HALEDON": "1606",
        "PASSAIC": "1607",
        "PATERSON": "1608",
        "POMPTON LAKES": "1609",
        "PROSPECT PARK": "1610",
        "RINGWOOD": "1611",
        "TOTOWA": "1612",
        "WANAQUE": "1613",
        "WAYNE": "1614",
        "WEST MILFORD": "1615",
        "WEST PATERSON": "1616",
        "ALL": "1600"
    },
    "SALEM": {
        "ALLOWAY": "1701",
        "CARNEYS POINT": "1702",
        "ELMER": "1703",
        "ELSINBORO": "1704",
        "LOWER ALLOWAYS CREEK": "1705",
        "MANNINGTON": "1706",
        "OLDMANS": "1707",
        "PENNS GROVE": "1708",
        "PENNSVILLE": "1709",
        "PILESGROVE": "1710",
        "PITTSGROVE": "1711",
        "QUINTON": "1712",
        "SALEM CITY": "1713",
        "UPPER PITTSGROVE": "1714",
        "WOODSTOWN": "1715",
        "ALL": "1700"
    },
    "SOMERSET": {
        "BEDMINSTER": "1801",
        "BERNARDS": "1802",
        "BERNARDSVILLE": "1803",
        "BOUND BROOK": "1804",
        "BRANCHBURG": "1805",
        "BRIDGEWATER": "1806",
        "FAR HILLS": "1807",
        "FRANKLIN": "1808",
        "GREEN BROOK": "1809",
        "HILLSBOROUGH": "1810",
        "MANVILLE": "1811",
        "MILLSTONE": "1812",
        "MONTGOMERY": "1813",
        "NORTH PLAINFIELD": "1814",
        "PEAPACK-GLADSTONE": "1815",
        "RARITAN": "1816",
        "ROCKY HILL": "1817",
        "SOMERVILLE": "1818",
        "SOUTH BOUND": "1819",
        "WARREN": "1820",
        "WATCHUNG": "1821",
        "ALL": "1800"
    },
    "SUSSEX": {
        "ANDOVER BOROUGH": "1901",
        "ANDOVER TOWNSHIP": "1902",
        "BRANCHVILLE": "1903",
        "BYRAM": "1904",
        "FRANKFORD": "1905",
        "FRANKLIN": "1906",
        "FREDON": "1907",
        "GREEN": "1908",
        "HAMBURG": "1909",
        "HAMPTON": "1910",
        "HARDYSTON": "1911",
        "HOPATCONG": "1912",
        "LAFAYETTE": "1913",
        "MONTAGUE": "1914",
        "NEWTON": "1915",
        "OGDENSBURG": "1916",
        "SANDYSTON": "1917",
        "SPARTA": "1918",
        "STANHOPE": "1919",
        "STILLWATER": "1920",
        "SUSSEX": "1921",
        "VERNON": "1922",
        "WALPACK": "1923",
        "WANTAGE": "1924",
        "ALL": "1900"
    },
    "UNION": {
        "BERKELEY HEIGHTS": "2001",
        "CLARK": "2002",
        "CRANFORD": "2003",
        "ELIZABETH": "2004",
        "FANWOOD": "2005",
        "GARWOOD": "2006",
        "HILLSIDE": "2007",
        "KENILWORTH": "2008",
        "LINDEN": "2009",
        "MOUNTAINSIDE": "2010",
        "NEW PROVIDENCE": "2011",
        "PLAINFIELD": "2012",
        "RAHWAY": "2013",
        "ROSELLE BOROUGH": "2014",
        "ROSELLE PARK BORO": "2015",
        "SCOTCH PLAINS": "2016",
        "SPRINGFIELD": "2017",
        "SUMMIT": "2018",
        "UNION": "2019",
        "WESTFIELD": "2020",
        "WINFIELD": "2021",
        "ALL": "2000"
    },
    "WARREN": {
        "ALLAMUCHY": "2101",
        "ALPHA": "2102",
        "BELVIDERE": "2103",
        "BLAIRSTOWN": "2104",
        "FRANKLIN": "2105",
        "FRELINGHUYSEN": "2106",
        "GREENWICH": "2107",
        "HACKETTSTOWN": "2108",
        "HARDWICK": "2109",
        "HARMONY": "2110",
        "HOPE": "2111",
        "INDEPENDENCE": "2112",
        "KNOWLTON": "2113",
        "LIBERTY": "2114",
        "LOPATCONG": "2115",
        "MANSFIELD": "2116",
        "OXFORD": "2117",
        "PHILLIPSBURG": "2119",
        "POHATCONG": "2120",
        "WASHINGTON BOROUGH": "2121",
        "WASHINGTON TOWNSHIP": "2122",
        "WHITE": "2123",
        "ALL": "2100"
    }
}

SEARCH_TYPES = {
    'Current Owners/Assmt List': '1',
    'Deed/Sr1a List': '2',
}

SEARCH_FORMATS = {
    'Simple Search': '1',
    'Advanced Search': '2',
}

OUTPUT_TYPES = {
    'Single Line List Format': '1',
    'Multi Line List Format': '2',
    'Excel File Format': '3',
}

def search_inner(
    county,
    district='ALL',
    location='',
    owner='',
    block='',
    lot='',
    qualifier='',
    search_type=SEARCH_TYPES['Current Owners/Assmt List'],
    search_format=SEARCH_FORMATS['Simple Search'],
    output_type=OUTPUT_TYPES['Single Line List Format'],
    per_page=50,
    zero_indexed_page=0):

    county_id = COUNTIES[county]
    district_id = DISTRICTS[county][district]

    if search_type not in SEARCH_TYPES.values():
        raise ValueError(f"search_type of {search_type} is invalid. must in {SEARCH_TYPES.values()}. See: {SEARCH_TYPES}")

    params = {
        'ms_user': 'monm',
        'passwd': 'data',
        'srch_type': search_type,
        'select_cc': county_id,
        'district': district_id,
        'adv': search_format,
        'out_type': output_type,
        'ms_ln': str(per_page),
        'p_loc': location,
        'owner': owner,
        'block': block,
        'lot': lot,
        'qual': qualifier,
        'pageno': str(zero_indexed_page)
    }

    response = requests.post(urljoin(BASE_URL, 'inf.cgi'), data=params)

    return response

def parse_search(response):

    def parse_row(row):
        return {
            'url': urljoin(BASE_URL, row.cssselect('td:nth-child(1) a')[0].get('href')),
            'district': row.cssselect('td:nth-child(2) font')[0].text,
            'block': row.cssselect('td:nth-child(3) font')[0].text,
            'lot': row.cssselect('td:nth-child(4) font')[0].text.replace('\xa0', ''),
            'qualifier': row.cssselect('td:nth-child(5) font')[0].text.replace('\xa0', ''),
            'location': row.cssselect('td:nth-child(6) font')[0].text,
            'owner': row.cssselect('td:nth-child(7) font')[0].text,
        }

    doc = lxml.html.fromstring(response.content)

    num_records = int(re.search(r"(\d+) Records Found", response.text).groups()[0])
    current_page = int(re.search(r"Page: (\d+)", response.text).groups()[0])
    has_next = bool(doc.cssselect('form input[value="Next"]'))

    meta = {
        "num_records": num_records,
        "current_page": current_page,
        "has_next": has_next
    }

    records = [parse_row(row) for row in doc.cssselect('table tr:not(:first-child)')]

    return meta, records

def search(**kwargs):
    zero_indexed_page = 0
    while True:
        response = search_inner(**kwargs, zero_indexed_page=zero_indexed_page)
        meta, records = parse_search(response)
        for record in records: yield meta, record
        if not meta['has_next']: break
        zero_indexed_page += 1

def search_and_get(**kwargs):
    for meta, record in search(**kwargs):
        detailed_record = parse_get(get_inner(record['url']))
        yield meta, {**record, **detailed_record}

def get(**kwargs):
    response = search_inner(**kwargs)
    meta, records = parse_search(response)
    if len(records) > 1:
        raise Exception(f"returned {len(records)} records. expected to get only 1")
    record = records[0]

    response = get_inner(record['url'])
    detailed_record = parse_get(response)

    return {**record, **detailed_record}

def get_inner(url):
    response = requests.get(url)
    return response

def parse_get(response):
    doc = lxml.html.fromstring(response.content)

    try:
        sqft = int([x for x in doc.cssselect('table td font') if x.text.strip() == "Square Ft:"][0].getparent().getnext().text_content().strip())
    except Exception as e:
        sqft = None

    if sqft == 0:
        sqft = None

    return {
        "sqft": sqft
    }

if __name__ == "__main__":
    from itertools import islice

    print(f"get single record")
    record = get(county='PASSAIC', district='CLIFTON', location='115 Dumont Ave')
    print(record)
    
    print(f"get record list")
    for meta, record in islice(search(county='PASSAIC', per_page=5), 10):
        print(meta, record)

    print(f"get multiple record details")
    for meta, record in islice(search_and_get(county='PASSAIC', per_page=5), 10):
        print(meta, record)
