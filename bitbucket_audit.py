#!/usr/bin/python3

# pip install pandas json
import requests
import json
import csv
import sys, getopt
from datetime import datetime
import configparser

def main(argv):
   global inifile,outfile,reportfile
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["inifile=","outfile="])
   except getopt.GetoptError:
      print ('bitbucket_audit.py -i <inifile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('bitbucket_audit.py -i <inifile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--inifile"):
         inifile = arg
      elif opt in ("-o", "--outfile"):
         outfile = arg
    # Get today's date in YYYYMMDD format
   date_stamp = datetime.today().strftime('%Y%m%d')
   reportfile = f"{outfile}_{date_stamp}.csv"

#   if debug:
#      print ('Input file is ', inifile)
#      print ('Output file is ', filename)


def get_projects():
 #   if debug:
 #       print(BITBUCKET_WORKSPACE_URL)
    url = f'{BITBUCKET_WORKSPACE_URL}/projects'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()

    return response.json()['values']

def get_projects_page2():
    url = f'{BITBUCKET_API_URL}/repositories/{MYWORKSPACE}/projects'
    response = requests.get(url, params=PARAMSPAGE2, headers=HEADERS)
    response.raise_for_status()

    return response.json()['values']

def get_repositories(project_key):
    myparams = f'q=project.key%3D%22{project_key}%22'
    url = f'{BITBUCKET_API_URL}/repositories/{MYWORKSPACE}'
    response = requests.get(url, params=myparams, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def get_project_permissions(project_key):
    url = f'{BITBUCKET_WORKSPACE_URL}/projects/{project_key}/permissions'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def get_project_groups_permissions(project_key):
    url = f'{BITBUCKET_WORKSPACE_URL}/projects/{project_key}/permissions-config/groups'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def get_project_users_permissions(project_key):
    url = f'{BITBUCKET_WORKSPACE_URL}/projects/{project_key}/permissions-config/users'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def get_repository_groups_permissions(repo_slug):
    url = f'{BITBUCKET_API_URL}/repositories/{MYWORKSPACE}/{repo_slug}/permissions-config/groups'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def get_repository_users_permissions(repo_slug):
    url = f'{BITBUCKET_API_URL}/repositories/{MYWORKSPACE}/{repo_slug}/permissions-config/users'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def get_repository_permissions(repo_slug):
    url = f'{BITBUCKET_API_URL}/repositories/{repo_slug}/permissions'
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    response.raise_for_status()
    return response.json()['values']

def create_bitbucketdata():
    bitbucketdata = []

    # used to make sure we have a list of unique projects
    myprojects = []
  
    projects = get_projects()
    for project in projects:

# Print to see what we are getting
#       if debug:
#        print(project['key'])
#           p = project['project']['name']
#           p = project['name']
#        if p not in projects:
#            projects.append(p)
        
        project_key = project['key']
        project_name = project['name']
        if debug:
            print(f"Current project name is {project_name}")
        
# Get project permissions
        project_groups_permissions = get_project_groups_permissions(project_key)
        for p in project_groups_permissions:
            if debug:
                group_name = p['group']['name']
#                print(p['group']['name'])
                print(f"Current group name is {group_name}")
        project_users_permissions = get_project_users_permissions(project_key)
        repositories = get_repositories(project_key)
        
        for repo in repositories:
            repo_name = repo['name']
            repo_slug = repo['slug']
            if debug:
                print(f"Current repo name is {repo_name}")
#                print(repo['name'])
            repo_groups_permissions = get_repository_groups_permissions(repo_slug)
#            if debug:
#                for p in repo_groups_permissions:
#                    print(p['group']['name'])
            repo_users_permissions = get_repository_users_permissions(repo_slug)

            # Add project and repository details to bitbucketdata
        bitbucketdata.append({
            'project_name': project_name,
            'project_groups_permissions': project_groups_permissions,
            'project_users_permissions': project_users_permissions,
            'repo_name': repo_name,
            'repo_groups_permissions': repo_groups_permissions,
            'repo_users_permissions': repo_users_permissions,
        })

    return bitbucketdata

def write_to_csv(data,filename):
    # Get today's date in YYYYMMDD format
    # date_stamp = datetime.today().strftime('%Y%m%d')
    # filename = f'bitbucket_access_audit_{date_stamp}.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(['Project Name', 'Repository Name', 'Type', 'User/Group', 'Access Level', 'Permission Scope'])

        # Write the data
        for item in data:
            project_name = item['project_name']
            repo_name = item['repo_name']

            permissions = []

            # Write project group permissions
            for perm in item['project_groups_permissions']:
                group = perm['group']['name']
                permission_level = perm['permission']
                scope = 'Project'
                type = 'Group'
                permissions.append([project_name, repo_name, type, group, permission_level, scope])
            
            # Write project user permissions
            for perm in item['project_users_permissions']:
                user = perm['user']['display_name']
                permission_level = perm['permission']
                scope = 'Project'
                type = 'User'
                permissions.append([project_name, repo_name, type, user, permission_level, scope])

            # Write repository group permissions
            for perm in item['repo_groups_permissions']:
                group = perm['group']['name']
                permission_level = perm['permission']
                scope = 'Repository'
                type = 'Group'
                permissions.append([project_name, repo_name, type, group, permission_level, scope])

            # Write repository user permissions
            for perm in item['repo_users_permissions']:
                user = perm['user']['display_name']
                permission_level = perm['permission']
                scope = 'Repository'
                type = 'User'
                permissions.append([project_name, repo_name, type, user, permission_level, scope])

            sorted_permissions =  sorted(permissions, key=lambda x: x[4])
            for perm in sorted_permissions:
                writer.writerow(perm)

if __name__ == '__main__':
    main(sys.argv[1:])
    global debug
    debug = True
    config = configparser.ConfigParser()
    config.read(inifile)
    AUTHORIZATION = config.get('request', 'authorization')
    BITBUCKET_API_URL = config.get('bitbucket', 'bitbucket_api_url')
    MYWORKSPACE = config.get('bitbucket', 'myworkspace')
    if debug:
        print (BITBUCKET_API_URL)
        print (MYWORKSPACE)

# Bitbucket API variables used for requests
#BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'
#MYWORKSPACE = 'asteralabs'
#AUTHORIZATION = API_KEY
    BITBUCKET_WORKSPACE_URL = f'{BITBUCKET_API_URL}/workspaces/{MYWORKSPACE}'
    HEADERS = { "Authorization": AUTHORIZATION, "Content-Type": "application/json" }
    PARAMS = {'pagelen': '100'}
    PARAMSPAGE2 = {'pagelen': '100', 'page': '2'}
    if debug:
        print (BITBUCKET_WORKSPACE_URL)
        print (HEADERS)
    bitbucketdata = create_bitbucketdata()
    write_to_csv(bitbucketdata,reportfile)
    print(f"CSV file {reportfile} created successfully.")
