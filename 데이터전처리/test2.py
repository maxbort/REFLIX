# import csv
# import requests

# API_KEY = "d0a643cc2040e40a659bcbc851013426"

# def get_ott_sites(tmdb_id):
#     url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers?api_key={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         ott_sites = []
#         if 'results' in data and 'KR' in data['results']:
#             korean_providers = data['results']['KR']
#             flatrate_providers = korean_providers.get('flatrate', [])
#             for provider in flatrate_providers:
#                 if 'provider_name' in provider and 'link' in provider:
#                     provider_name = provider['provider_name']
#                     link = provider['link']
#                     ott_sites.append({'provider_name': provider_name, 'link': link})
#         return ott_sites
#     return []

# def update_csv_with_ott_sites(input_csv_file, output_csv_file, num_samples=30):
#     updated_rows = []

#     with open(input_csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         fieldnames = reader.fieldnames + ['OTT Provider', 'OTT Link']
#         updated_rows.append(fieldnames)

#         for i, row in enumerate(reader):
#             if i >= num_samples:
#                 break

#             tmdb_id = row['tmdbId']
#             ott_sites = get_ott_sites(tmdb_id)
#             ott_providers = ', '.join([site['provider_name'] for site in ott_sites])
#             ott_links = ', '.join([site['link'] for site in ott_sites])
#             row['OTT Provider'] = ott_providers
#             row['OTT Link'] = ott_links
#             updated_rows.append(list(row.values()))  # Convert row from dictionary to list

#     with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerows(updated_rows)

#     print(f"OTT sites saved to '{output_csv_file}' for {num_samples} samples.")

# # Example usage
# update_csv_with_ott_sites("데이터전처리\_SELect_DISTINCT_ck_keyword1_ck_keyword2_ck_keyword3_ck_keyword4_202305240230.csv", "test_output.csv", num_samples=30)

import csv
import requests
from tqdm import tqdm
API_KEY = "d0a643cc2040e40a659bcbc851013426"

def get_ott_sites(tmdb_id):
    url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/watch/providers?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ott_sites = []
        if 'results' in data and 'KR' in data['results']:
            korean_providers = data['results']['KR']
            flatrate_providers = korean_providers.get('flatrate', [])
            for provider in flatrate_providers:
                if 'provider_name' in provider:
                    provider_name = provider['provider_name']
                    provider_logo = provider['logo_path']
                    link = korean_providers['link']
                    ott_sites.append({'provider_name': provider_name, 'link': link})
        return ott_sites
    return []

def update_csv_with_ott_sites(input_csv_file, output_csv_file, num_samples=100000):
    updated_rows = []

    with open(input_csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['OTT Provider', 'OTT Link']
        updated_rows.append(fieldnames)

        for i, row in tqdm(enumerate(reader)):
            if i >= num_samples:
                break

            tmdb_id = row['tmdbId']
            ott_sites = get_ott_sites(tmdb_id)
            ott_providers = ', '.join([site['provider_name'] for site in ott_sites])
            ott_links = ', '.join([site['link'] for site in ott_sites])

            row['OTT Provider'] = ott_providers
            row['OTT Link'] = ott_links
            updated_rows.append(list(row.values()))

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    print(f"OTT sites saved to '{output_csv_file}' for {num_samples} samples.")

# Example usage
update_csv_with_ott_sites("all_content_final.csv", "test_output3.csv", num_samples=100000)
