import csv
import io
import math
from datetime import timedelta
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import sys

OPENFLIGHTS_BASE = "https://raw.githubusercontent.com/jpatokal/openflights/master/data"
AIRPORTS_URL = f"{OPENFLIGHTS_BASE}/airports.dat"
ROUTES_URL = f"{OPENFLIGHTS_BASE}/routes.dat"
AIRLINES_URL = f"{OPENFLIGHTS_BASE}/airlines.dat"


def download_openflights_file(url, verbose=False):
    if verbose:
        print(f"Downloading {url}...", file=sys.stderr)
    request = Request(url, headers={"User-Agent": "Bookaro OpenFlights Importer"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8", errors="replace")
            if verbose:
                print(f"Downloaded {len(payload)} bytes", file=sys.stderr)
            return payload
    except HTTPError as exc:
        raise RuntimeError(f"OpenFlights download failed: {exc.code} {exc.reason}")
    except URLError as exc:
        raise RuntimeError(f"OpenFlights download failed: {exc.reason}")


def parse_csv_text(text, delimiter=","):
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    return list(reader)


def normalize_text(value):
    return value.strip().strip('"') if value else ""


def is_iata_code(value):
    value = normalize_text(value)
    return bool(value) and value != "\\N"


def load_airlines(airlines_text):
    airlines = {}
    for row in parse_csv_text(airlines_text):
        if len(row) < 5:
            continue
        airline_id = normalize_text(row[0])
        airline_name = normalize_text(row[1])
        iata = normalize_text(row[3]).upper()
        icao = normalize_text(row[4]).upper()
        if iata and iata != "\\N":
            airlines[iata] = airline_name or iata
        if icao and icao != "\\N":
            airlines[icao] = airline_name or icao
        if airline_id:
            airlines[airline_id] = airline_name or airline_id
    return airlines


def load_airports(airports_text):
    airports = {}
    for row in parse_csv_text(airports_text):
        if len(row) < 8:
            continue
        iata = normalize_text(row[4]).upper()
        if not is_iata_code(iata):
            continue
        name = normalize_text(row[1])
        city = normalize_text(row[2])
        country = normalize_text(row[3])
        latitude = normalize_text(row[6])
        longitude = normalize_text(row[7])
        if not latitude or not longitude:
            continue
        try:
            lat = float(latitude)
            lon = float(longitude)
        except ValueError:
            continue
        airports[iata] = {
            "iata": iata,
            "name": name,
            "city": city,
            "country": country,
            "latitude": lat,
            "longitude": lon,
        }
    return airports


def compute_distance_km(origin, destination):
    lat1, lon1 = math.radians(origin[0]), math.radians(origin[1])
    lat2, lon2 = math.radians(destination[0]), math.radians(destination[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c


def estimate_price_in_inr(distance_km, is_international):
    base_rate = Decimal("2.30") if is_international else Decimal("3.80")
    price = (base_rate * Decimal(distance_km)).quantize(Decimal("1"))
    minimum = Decimal("6500") if is_international else Decimal("2200")
    return max(price, minimum)


def build_flight_descriptor(route_index, airline_code, source_iata, dest_iata, airline_name):
    flight_number = f"{airline_code}{route_index % 9000 + 1000}"
    origin = f"{source_iata} ({source_iata})"
    destination = f"{dest_iata} ({dest_iata})"
    return flight_number, origin, destination, airline_name


def parse_routes(routes_text, airports, airlines):
    unique_routes = []
    seen = set()
    for row in parse_csv_text(routes_text):
        if len(row) < 9:
            continue
        airline_code = normalize_text(row[0]).upper()
        src_iata = normalize_text(row[2]).upper()
        dst_iata = normalize_text(row[4]).upper()
        if not airline_code or not is_iata_code(src_iata) or not is_iata_code(dst_iata):
            continue
        if src_iata == dst_iata:
            continue
        if src_iata not in airports or dst_iata not in airports:
            continue
        route_key = (airline_code, src_iata, dst_iata)
        if route_key in seen:
            continue
        seen.add(route_key)
        unique_routes.append(route_key)
    return unique_routes


def import_openflights_flights(max_routes=None, skip_existing=False, verbose=False):
    if verbose:
        print("Downloading OpenFlights data files...", file=sys.stderr)
    
    airports_text = download_openflights_file(AIRPORTS_URL, verbose=verbose)
    airlines_text = download_openflights_file(AIRLINES_URL, verbose=verbose)
    routes_text = download_openflights_file(ROUTES_URL, verbose=verbose)

    if verbose:
        print("Parsing airports...", file=sys.stderr)
    airports = load_airports(airports_text)
    if verbose:
        print(f"Loaded {len(airports)} airports", file=sys.stderr)
    
    if verbose:
        print("Parsing airlines...", file=sys.stderr)
    airlines = load_airlines(airlines_text)
    if verbose:
        print(f"Loaded {len(airlines)} airlines", file=sys.stderr)
    
    if verbose:
        print("Parsing routes...", file=sys.stderr)
    route_keys = parse_routes(routes_text, airports, airlines)
    if verbose:
        print(f"Parsed {len(route_keys)} unique routes", file=sys.stderr)

    if max_routes is not None:
        route_keys = route_keys[:max_routes]
        if verbose:
            print(f"Limited to {max_routes} routes", file=sys.stderr)

    from django.utils import timezone
    from Services.models import Flight

    created = 0
    updated = 0
    skipped = 0

    now = timezone.now()
    if verbose:
        print(f"Creating flight records...", file=sys.stderr)
    
    for index, (airline_code, src_iata, dst_iata) in enumerate(route_keys, start=1):
        source = airports[src_iata]
        destination = airports[dst_iata]
        origin_name = f"{source['city']}, {source['country']} ({src_iata})"
        dest_name = f"{destination['city']}, {destination['country']} ({dst_iata})"
        is_international = source["country"] != destination["country"]
        distance_km = compute_distance_km((source["latitude"], source["longitude"]), (destination["latitude"], destination["longitude"]))
        price = estimate_price_in_inr(distance_km, is_international)
        airline_name = airlines.get(airline_code, airline_code)
        flight_number = f"{airline_code}{index % 9000 + 1000}"
        departure_offset = timedelta(hours=(index % 240), days=(index // 240) % 14)
        departure_time = (now + departure_offset).replace(minute=0, second=0, microsecond=0)

        defaults = {
            "airline": airline_name,
            "origin": origin_name,
            "destination": dest_name,
            "departure_time": departure_time,
            "price": price,
            "is_international": is_international,
        }

        flight, created_flag = Flight.objects.get_or_create(
            airline=airline_name,
            origin=origin_name,
            destination=dest_name,
            flight_number=flight_number,
            defaults=defaults,
        )

        if created_flag:
            created += 1
        else:
            if not skip_existing:
                Flight.objects.filter(pk=flight.pk).update(**defaults)
                updated += 1
            else:
                skipped += 1

        if verbose and index % 500 == 0:
            print(f"Processed {index}/{len(route_keys)} routes: created={created} updated={updated} skipped={skipped}", file=sys.stderr)

    return created, updated, skipped, len(route_keys)
