import requests
from requests.auth import HTTPBasicAuth

# Replace these with your Bitbucket credentials
BITBUCKET_USERNAME = 'your_username'
BITBUCKET_APP_PASSWORD = 'your_app_password'

# Bitbucket API base URL
BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'

def get_projects():
    url = f'{BITBUCKET_API_URL}/projects'
    response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()
    return response.json()['values']

def get_repositories(project_key):
    url = f'{BITBUCKET_API_URL}/repositories/{project_key}'
    response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()
    return response.json()['values']

def get_project_permissions(project_key):
    url = f'{BITBUCKET_API_URL}/projects/{project_key}/permissions'
    response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()
    return response.json()['values']

def get_repository_permissions(repo_slug):
    url = f'{BITBUCKET_API_URL}/repositories/{repo_slug}/permissions'
    response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()
    return response.json()['values']

def create_structure():
    structure = {}

    projects = get_projects()

    for project in projects:
        project_key = project['key']
        project_name = project['name']
        
        # Create project entry with permissions
        structure[project_name] = {
            'permissions': get_project_permissions(project_key),
            'repositories': {}
        }

        repositories = get_repositories(project_key)

        for repo in repositories:
            repo_name = repo['name']
            repo_slug = repo['slug']
            
            # Add repository entry with permissions
            structure[project_name]['repositories'][repo_name] = {
                'details': repo,
                'permissions': get_repository_permissions(repo_slug)
            }

    return structure

if __name__ == '__main__':
    bitbucket_structure = create_structure()
    print(bitbucket_structure)
