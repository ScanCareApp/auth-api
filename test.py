import requests

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJlNzgyM2VmMDFiZDRkMmI5NjI3NDE2NThkMjA4MDdlZmVlNmRlNWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2NhbmNhcmUtY2Fwc3RvbmUtMWRkYmMiLCJhdWQiOiJzY2FuY2FyZS1jYXBzdG9uZS0xZGRiYyIsImF1dGhfdGltZSI6MTcwMjI3MzA2NywidXNlcl9pZCI6Ik5KOUs3UU1sMGxPVjZ2RmZBdXpBcDBZNU9UQTIiLCJzdWIiOiJOSjlLN1FNbDBsT1Y2dkZmQXV6QXAwWTVPVEEyIiwiaWF0IjoxNzAyMjczMDY3LCJleHAiOjE3MDIyNzY2NjcsImVtYWlsIjoiYkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYkBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.N9eDJyiNe3C2xQYjkT0bV63WOccCejVlqSiAeTu5vhIeGHIeV9w7d-KLu9b6h2jhvTU6-L8jQBHDXvBzMGu-nLLUTN6ittS4OPeypCQvKeYM_s7FTOVTNDSFdMyxUNPAqbtMq28PrZBI0NEKVaDfh7NVLL7MWYBuY4nySL0-Zm7c2uSSj739xnxreJFCq38XR3MsGzkD072ZNIL8WMJ_syXvL0-JDKzqG-1xZwSUz-H_46_yjmhJfvhXL2dlQ9jZ9HOKDYo35jyWNQmfoUcgf9ItjD4AOXdXrAqAnMcv3HNb3nZW9-w1YJEVXNfXczU5V6lxKfsW1lidf_bZQn2Tfg"


# belum seleasai, tpi ini gapapa

def test_validate_endpoint():
    headers = {
        'authorization': token
    }
    response = requests.post(
        "http://127.0.0.1:8000/ping"
    )

    return response.text
