import json
import urllib.request
import urllib.parse
from django.shortcuts import render

def index(request):
    query = request.GET.get('query', '').strip()
    country_data = None
    error_message = None

    if query:
        # URL encode the query to handle spaces and special characters
        encoded_query = urllib.parse.quote(query)
        url = f"https://restcountries.com/v3.1/name/{encoded_query}"
        
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if isinstance(data, list) and len(data) > 0:
                        # Find an exact match if possible, otherwise use the first element
                        country_info = data[0]
                        for country in data:
                            if country.get('name', {}).get('common', '').lower() == query.lower():
                                country_info = country
                                break
                        
                        # Extract and format the details nicely
                        name_info = country_info.get('name', {})
                        common_name = name_info.get('common', '')
                        official_name = name_info.get('official', '')
                        
                        # Population formatting
                        pop = country_info.get('population', 0)
                        formatted_pop = f"{pop:,}"
                        
                        # Languages
                        langs_dict = country_info.get('languages', {})
                        languages = list(langs_dict.values())
                        
                        # Currencies
                        currencies_dict = country_info.get('currencies', {})
                        currencies = []
                        for code, details in currencies_dict.items():
                            curr_name = details.get('name', 'N/A')
                            curr_symbol = details.get('symbol', '')
                            if curr_symbol:
                                currencies.append(f"{curr_name} ({code}, {curr_symbol})")
                            else:
                                currencies.append(f"{curr_name} ({code})")
                        
                        # Flag & Coat of Arms
                        flag_url = country_info.get('flags', {}).get('png', '')
                        flag_alt = country_info.get('flags', {}).get('alt', f"Flag of {common_name}")
                        coat_of_arms = country_info.get('coatOfArms', {}).get('png', '')
                        
                        # Capital
                        capitals = country_info.get('capital', [])
                        capital = ", ".join(capitals) if capitals else 'N/A'
                        
                        # Regions
                        region = country_info.get('region', 'N/A')
                        subregion = country_info.get('subregion', 'N/A')
                        
                        # Maps
                        map_url = country_info.get('maps', {}).get('googleMaps', '')
                        
                        # Timezones
                        timezones = country_info.get('timezones', [])
                        
                        # Borders
                        borders = country_info.get('borders', [])
                        
                        country_data = {
                            'common_name': common_name,
                            'official_name': official_name,
                            'population': formatted_pop,
                            'languages': languages,
                            'currencies': currencies,
                            'flag_url': flag_url,
                            'flag_alt': flag_alt,
                            'coat_of_arms': coat_of_arms,
                            'capital': capital,
                            'region': region,
                            'subregion': subregion,
                            'map_url': map_url,
                            'timezones': timezones,
                            'borders': borders,
                        }
                    else:
                        error_message = f"No details found for '{query}'."
                else:
                    error_message = f"Error fetching details (Status: {response.status})."
        except urllib.error.HTTPError as e:
            if e.code == 404:
                error_message = f"Country '{query}' not found. Please check the spelling and try again."
            else:
                error_message = f"REST Countries API returned an error (HTTP {e.code})."
        except urllib.error.URLError as e:
            error_message = "Unable to reach the REST Countries API. Please check your internet connection."
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            
    return render(request, 'explorer/index.html', {
        'query': query,
        'country_data': country_data,
        'error_message': error_message
    })
