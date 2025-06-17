import io
import json
import shutil
import zipfile


import requests

import io
from IPython.display import display
from PIL import Image
import Exceptions
import basicFunction
import os
import matplotlib.pyplot as plt
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
                        print(f"{commit_id}: {commit_value['message']}: {commit_value['name']}:{commit_value['push']}")
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


    @staticmethod
    def push():
        find_path=False
        folders_to_push=[]
        path=os.path.join(os.getcwd(), ".wit")
        if not basicFunction.is_exist(path,"commit"):
            print("fatal: The current branch master has no commits yet")
            return
        else:
            repository_data = basicFunction.load_repository_data_json()
            for rep in repository_data['repository_data']:
                if rep['path'] == path:
                    find_path=True
                    commits = rep.get("commit", {})
                    if commits=={}:
                        print("fatal: The current branch master has no commits yet")
                        return
                    for commit_id, commit_data in commits.items():
                        if commit_data.get("push") == False:
                            folders_to_push.append(commit_data.get("name"))
                            commit_data["push"]=True

                    break
            basicFunction.dump_repository_data_json(repository_data)
            if find_path==False:
                raise Exception.witNotExistsError(
                    "fatal: not a wit repository (or any of the parent directories): .wit")
            if folders_to_push==[]:
                print("Everything up-to-date")
                return
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder_to_push in folders_to_push:
              full_path_folder_to_push=os.path.join(path,"commit",folder_to_push)
              if os.path.isdir(full_path_folder_to_push):
                for root, dirs, files in os.walk(full_path_folder_to_push):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if os.path.samefile(root, full_path_folder_to_push):
                            arcname = file
                        else:
                            arcname = os.path.relpath(full_path, start=full_path_folder_to_push)
                        zipf.write(full_path,arcname=arcname)
              else:
                zipf.write(folder_to_push,arcname=os.path.basename(full_path_folder_to_push))
        zip_buffer.seek(0)
        data = {
            "target_path":path
        }
        files = {
            "file": ("code.zip", zip_buffer.getvalue(), "application/zip")
        }

        alerts = "http://localhost:8001/alerts"
        analyze="http://localhost:8001/analyze"
        try:
           response_alerts = requests.post(alerts, data=data,files=files)
           response_analyze=requests.post(analyze,data=data,files=files)
        except Exception as e:
          print("Error sending requests:", e)
          return

        print("Alerts status code:", response_alerts.status_code)
        try:
            print(json.dumps(response_alerts.json(), indent=4, ensure_ascii=False))
        except:
            print("Alerts response not JSON")

        if response_analyze.status_code != 200:
            print("Analyze response failed (status code:", response_analyze.status_code, ")")
            return

        else:
            image_bytes = io.BytesIO(response_analyze.content)
            img = Image.open(image_bytes)
            img.load()
            plt.imshow(img)
            plt.axis('off')
            plt.tight_layout()
            plt.show()














