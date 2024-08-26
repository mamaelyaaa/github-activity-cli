import requests
import sys


def getUserActivity(username):
    response = requests.get(f'https://api.github.com/users/{username}/events')

    if response.status_code == 404:
        raise Exception('User not found :/')

    for event in response.json():
        if event['type'] == 'PushEvent':
            commit = event['payload']['commits'][0]['message']
            print(f'- Pushed new commit to {event["repo"]["name"]}: {commit}')

        elif event['type'] == 'CreateEvent':
            if event['payload']['ref'] is None:
                continue
            print(f'- Created {event["repo"]["name"]}')

        elif event['type'] == 'DeleteEvent':
            print(f'- Deleted {event["repo"]["name"]}')

        elif event['type'] == 'WatchEvent':
            print(f'- Starred {event["repo"]["name"]}')

        elif event['type'] == 'IssuesEvent':
            print(f'- Created issue in {event["repo"]["name"]}: {event["payload"]["issue"]["title"]}')

        else:
            print(f'Error fetching events for {username}: {response.status_code}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        getUserActivity(sys.argv[1])
    else:
        getUserActivity(input('Please write a GitHub username: '))