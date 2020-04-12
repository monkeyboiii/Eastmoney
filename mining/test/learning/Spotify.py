import requests


url = "https://api.spotify.com/v1/search?q=Trap&type=track&market=US"

payload = {}
headers = {
    'Authorization': 'Bearer '
                     'BQC6cJmlEkhTe5U53eGHOdYwQOLTNq8_PgHATFWVD9O9pz-eH9peX17hQ7R_6n0XK8RKy2UzCeNv8ikM9cZtE0pbJnXm_HOP-kdZk1b1FYQGmOhArgfN5VEUt6taQnNrEJtdvp85kRWdJEa1M7QJ3pY0i8VPCH727yE'
}

response = requests.request("GET", url, headers=headers, data=payload)

file = open('SpotifyTemp.txt', mode='w')
file.write(response.text)
