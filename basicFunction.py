import datetime
import json
import os
import shutil

#update repository data json
def dump_repository_data_json(repository_data):
    with open(r'C:\Users\This User\Desktop\python\pythonProject\repository_data.json', 'w',
              encoding='utf-8') as data:
        updated_json_data = json.dumps(repository_data, indent=2)
        data.write(updated_json_data)


def create_folder(path, name_folder):
    new_path = os.path.join(path, name_folder)
    os.makedirs(new_path)
    if name_folder == ".wit":
        os.system('attrib +h "' + new_path + '"')

#function to check if aspecitic file/folder exist
def is_exist(path, folder_name):
    folderPath = os.path.join(path, folder_name)
    return os.path.exists(folderPath)

#function to create new folder
def create_file(path, file_name):
    with open(os.path.join(path, '.wit', 'stagingArea', file_name), 'w',encoding="utf-8") as file:
        with open(os.path.join(path, file_name), "r",encoding="utf-8") as readingFile:
            file.write(readingFile.read())

#function to add new version to commit
def add_version_to_commit_list(path, commit_message):
    repository_data = load_repository_data_json()
    #moving on repository data list
    for i in repository_data['repository_data']:
        if i["path"] == path:
            #if the commit dictionery is empty
            if i['commit'] == {}:
                last_hash_code = "-1"
                #create commit folder
                create_folder(path, 'commit')
            else:
                #sort the commit keys
                sorted_keys = sorted(map(int, i['commit'].keys()))
                #get the last key
                last_hash_code = str(sorted_keys[-1])
            #create new version
            i['commit'][str(int(last_hash_code) + 1)] = {
                "message": commit_message,
                "name": str(datetime.date.today()) + " code-" + str(int(last_hash_code) + 1),
                "push":False
            }
            #save the name of the last commit
            last_commit = i['commit'][str(int(last_hash_code) + 1)]['name']
            #save of the folder version to merge
            folder_name_to_merge = i['version_hash_code']
            #if it is the first commit
            if folder_name_to_merge == "":
                create_folder(os.path.join(path, 'commit'), last_commit)
            else:
                directory = os.path.join(path, 'commit', folder_name_to_merge)
                shutil.copytree(directory, os.path.join(path, 'commit', last_commit))
            #calling to func that merge the stagingArea folder to the new version
            merge_spec_version_with_staging_area(os.path.join(path, 'commit', last_commit), path)
            #update the version hash_code to the next version
            i['version_hash_code'] = i['commit'][str(int(last_hash_code) + 1)]['name']
            break
    #calling to func that update the data json
    dump_repository_data_json(repository_data)


def merge_spec_version_with_staging_area(dest_path_to_merge, path):
    staging_area_path = os.path.join(path, 'stagingArea')
    # moving the stagingArea folder
    for i in os.listdir(staging_area_path):
        if os.path.isdir(os.path.join(staging_area_path, i)):
            if is_exist(dest_path_to_merge, i):
                #delete exist folder
                shutil.rmtree(os.path.join(dest_path_to_merge, i))
            shutil.copytree(os.path.join(staging_area_path, i), os.path.join(dest_path_to_merge, i))
        else:
            if is_exist(dest_path_to_merge, i):
                #delete exist file
                os.remove(os.path.join(dest_path_to_merge, i))
            shutil.copy(os.path.join(staging_area_path, i), os.path.join(dest_path_to_merge, i))

#return repository data json
def load_repository_data_json():
    with open(r'C:\Users\This User\Desktop\python\pythonProject\repository_data.json', 'r',
              encoding='utf-8') as data:
        return json.load(data)
