import requests

url = "https://api.themoviedb.org/3/tv/1429/watch/providers"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMGE2NDNjYzIwNDBlNDBhNjU5YmNiYzg1MTAxMzQyNiIsInN1YiI6IjYzZmU2ZjdmOTMzODhiMDBiNzgyMjVmYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iIRliOoES_GhAcpnBvefVwI6i3zETk4u1TuHqrlvNH8"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    results = data.get('results', {})
    korean_providers = results.get('KR', {}).get('flatrate', [])
    provider_link = results['KR']['link']    
    
    if korean_providers:
        for provider in korean_providers:
            provider_name = provider.get('provider_name', 'Unknown')
            print(f"{provider_name}: {provider_link}")
    else:
        print("한국에서 시청 가능한 OTT 사이트가 없습니다.")
else:
    print("API 요청에 실패했습니다.")
