import csv
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

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

def create_bitbucketdata():
    bitbucketdata = []

    projects = get_projects()

    for project in projects:
        project_key = project['key']
        project_name = project['name']
        
        # Get project permissions
        project_permissions = get_project_permissions(project_key)

        repositories = get_repositories(project_key)

        for repo in repositories:
            repo_name = repo['name']
            repo_slug = repo['slug']
            
            # Get repository permissions
            repo_permissions = get_repository_permissions(repo_slug)
            
            # Add project and repository details to bitbucketdata
            bitbucketdata.append({
                'project_name': project_name,
                'repo_name': repo_name,
                'project_permissions': project_permissions,
                'repo_permissions': repo_permissions
            })

    return bitbucketdata

def write_to_csv(data):
    # Get today's date in YYYYMMDD format
    date_stamp = datetime.today().strftime('%Y%m%d')
    filename = f'bitbucket_access_audit_{date_stamp}.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['Project Name', 'Repository Name', 'User/Group', 'Permission Level', 'Scope'])
        
        # Write the data
        for item in data:
            project_name = item['project_name']
            repo_name = item['repo_name']

            # Write project permissions
            for perm in item['project_permissions']:
                user_or_group = perm['user']['display_name'] if 'user' in perm else perm['group']['name']
                permission_level = perm['permission']
                scope = 'Project'
                writer.writerow([project_name, repo_name, user_or_group, permission_level, scope])

            # Write repository permissions
            for perm in item['repo_permissions']:
                user_or_group = perm['user']['display_name'] if 'user' in perm else perm['group']['name']
                permission_level = perm['permission']
                scope = 'Repository'
                writer.writerow([project_name, repo_name, user_or_group, permission_level, scope])

if __name__ == '__main__':
    bitbucketdata = create_bitbucketdata()
    write_to_csv(bitbucketdata)
    print("CSV file created successfully.")
