import json
import shutil

import Exceptions
import basicFunction
import os

from abstractWit import abstractWit


class wit(abstractWit):

    @staticmethod
    def init():
        folderPath = os.path.join(os.getcwd(), '.wit')
        if not basicFunction.is_exist(os.getcwd(), '.wit'):
            basicFunction.create_folder(os.getcwd(), '.wit')
            repository_data = basicFunction.load_repository_data_json()
            # create new ropository
            new_rep = {
                "path": folderPath,
                "version_hash_code": "",
                "commit": {}
            }
            # insert repository to json
            repository_data['repository_data'].append(new_rep)
            basicFunction.dump_repository_data_json(repository_data)
        else:
            # wit folder is exist
            raise Exceptions.FileExistsError("Reinitialized existing wit repository.")

    @staticmethod
    def add(name):
        full_pase_wit = os.path.join(os.getcwd(), '.wit')
        full_pase_name = os.path.join(os.getcwd(), name)
        if not basicFunction.is_exist(os.getcwd(), '.wit'):
            # adition directory/file  without wit folder is not valid
            raise Exception.witNotExistsError("fatal: not a wit repository (or any of the parent directories): .wit")
        if not basicFunction.is_exist(os.getcwd(), name):
            # try to add file/folder that not exist in this project
            raise Exception.notValidPathSpec("pathspec" + name + "didnt match any file")
        if not basicFunction.is_exist(full_pase_wit, 'stagingArea'):
            basicFunction.create_folder(full_pase_wit, 'stagingArea')
        if os.path.isdir(full_pase_name):
            if basicFunction.is_exist(os.path.join(full_pase_wit, 'stagingArea'), name):
                # if  file/folder exist delete before add it
                shutil.rmtree(os.path.join(full_pase_wit, 'stagingArea', name))
            shutil.copytree(full_pase_name, os.path.join(full_pase_wit, 'stagingArea', name))
        else:
            if os.path.isfile(full_pase_name):
                basicFunction.create_file(os.getcwd(), name)
            else:
                # if invalid extension
                raise Exceptions.InvalidFileExtension("file extension is not valid")

    @staticmethod
    def commit_m_message(message):
        # commit action before stagingArea folder exist
        if not basicFunction.is_exist(os.path.join(os.getcwd(), '.wit'), 'stagingArea'):
            print("nothing added to commit but untracked files present (use wit add to track)")
        else:
            # calling to a function that add version to commit
            basicFunction.add_version_to_commit_list(os.path.join(os.getcwd(), ".wit"), message)
            # delete the dtagingArea folder  becouse there is no new  changes now
            shutil.rmtree(os.path.join(os.getcwd(), '.wit', 'stagingArea'))

    @staticmethod
    def log():
        if not basicFunction.is_exist(os.path.join(os.getcwd(), '.wit'), 'commit'):
            print("fatal: your current branch 'master' does not have any commits yet")
        else:
            repository_data = basicFunction.load_repository_data_json()
            # moving on the commit dictionery and print all versiens
            for rep in repository_data['repository_data']:
                if rep['path'] == os.path.join(os.getcwd(), '.wit'):
                    for commit_id, commit_value in rep['commit'].items():
                        print(f"{commit_id}: {commit_value['message']}: {commit_value['name']}")
                    break

    @staticmethod
    def status():
        # if the stagingArea folder is empty
        if not basicFunction.is_exist(os.path.join(os.getcwd(), '.wit'), 'stagingArea'):
            print("Use 'wit add <file/directory>...' to include in what will be committed.")
        else:
            # print stagingArea folder
            for i in os.listdir(os.path.join(os.getcwd(), '.wit', 'stagingArea')):
                print(i)

    @staticmethod
    def check_out(commit_id):
        # calling to function that loading the data json
        repository_data = basicFunction.load_repository_data_json()
        # moving on repository_data list and update the version_hash_code
        for rep in repository_data['repository_data']:
            if rep['path'] == os.path.join(os.getcwd(), '.wit'):
                sorted_keys = sorted(map(int, rep['commit'].keys()))
                last_hash_code = str(sorted_keys[-1])
                # if commit id greater than the last commit id or less that zero
                if last_hash_code < commit_id or commit_id < 0:
                    raise Exceptions.InvalidCommitId("commit id is not valid")
                rep['version_hash_code'] = rep['commit'][commit_id]['name']
                #calling to a function that update the data json
        basicFunction.dump_repository_data_json(repository_data)
