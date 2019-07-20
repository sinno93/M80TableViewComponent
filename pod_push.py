import sys
import os
import re

pod_spec_filename = 'M80TableViewComponent.podspec'

def run():
    new_version = get_new_version()
    old_version = get_old_version()
    print('current version is [' + old_version + ']')
    if new_version is not None and old_version is not None:
        question = 'do u want to upgrade current pod to \'' + new_version + '\' ? (y/n)\n'
        choice = input(question).lower()
        if choice == 'y' or choice == 'yes':
            update(old_version,new_version)

def update(old_version,new_version):

    if run_shell('pod lib lint --no-clean') != 0:
        return

    if update_pod_spec(old_version,new_version) == False:
        return

    git_add         = 'git add .'
    git_commit      = 'git commit . -m " pod version update to ' + new_version + '"'
    git_push        = 'git push'
    git_add_tag     = 'git tag ' + new_version
    git_push_tag    = 'git push --tags'
    pod_push        = 'pod trunk push ' + pod_spec_filename

    command_list = [git_add,git_commit,git_push,git_add_tag,git_push_tag,pod_push]
    for command in command_list:
        run_shell(command)
        

    

def get_old_version():
    old_version = None
    version_pattern = r"\s*s.version\s+=\s+'(\d+.\d+.\d+)'"
    pod_file = './' + pod_spec_filename
    with open(pod_file) as podspec:
        content = podspec.read()
        old_version = re.search(version_pattern,content).group(1)
    return old_version

    
def update_pod_spec(old_version,new_version):
    pod_file = './' + pod_spec_filename
    new_content = None
    with open(pod_file) as podspec:
        content = podspec.read()
        new_content = content.replace(old_version,new_version,1)
    if new_content is not None:
        with open(pod_file,'w') as podspec:
            podspec.write(new_content)
            return True
    return False

    

def run_shell(command):
    return os.system(command)


def get_new_version():
    version = None
    if len(sys.argv) == 2:
        candidate_version = sys.argv[1].strip()
        if is_valid_version(candidate_version):
            version = candidate_version
    else:
        print('version needed')
    return version

def is_valid_version(version):
    valid = False
    components = version.split('.')
    if len(components) >= 3:
        for component in components:
            try:
                num = int(component)
            except:
                print('invalid version: ',version)
                return False
        valid = True
    if valid is False:
        print('invalid version: ',version)
    return valid

if __name__ == '__main__':
    run()