import tempfile
import zipfile

import requests
import json
import os

import shutil

from multiprocessing import Process


def get_repo_root(endpoint, project_id, experiment_id, file_path):
    payload = {'projectId': project_id, "filePath": file_path, 'experimentId':experiment_id}
    r = requests.get(endpoint, params=payload)
    ret_val = json.loads(r.text)

    if "root_path" in ret_val and ret_val["root_path"] is not None:
        return ret_val["root_path"]
    elif "msg" in ret_val:
        raise ValueError(ret_val["msg"])


def compress_py_files(repo_root_path):
    zip_dir = tempfile.mkdtemp()
    zip_path = os.path.join(zip_dir, "repo.zip")

    archive = zipfile.ZipFile(zip_path, 'w')

    for root, dirs, files in os.walk(repo_root_path):
        for afile in files:
            extentsion = os.path.splitext(afile)[-1].lower()
            if extentsion in [".py", ".txt", ".json"]:
                arcname = os.path.join(root.replace(repo_root_path,""),afile)
                archive.write(os.path.join(root, afile),arcname=arcname)
    archive.close()

    return zip_dir, zip_path


def send_zip_file(post_zip_endpoint, experiment_id, project_id, zip_file):
    files = {'file': open(zip_file, 'rb')}
    r = requests.post(post_zip_endpoint, params={"experimentId": experiment_id, "projectId": project_id}, files=files)

    if r.status_code != 200:
        raise ValueError("POSTing zip file failed")


def upload_repo(project_id, experiment_id, file_path, get_path_endpoint, post_zip_endpoint):
    try:
        repo_root_path = get_repo_root(get_path_endpoint, project_id, experiment_id, file_path)

        zip_folder, zip_path = compress_py_files(repo_root_path)

        send_zip_file(post_zip_endpoint, experiment_id, project_id, zip_path)

        # Cleanup temp directory
        shutil.rmtree(zip_folder)
    except ValueError as e:
        print('comet.ml error: repo files would not be synced %s' % e)


def upload_repo_start_process(project_id, experiment_id, file_path, get_path_endpoint, post_zip_endpoint):
    p = Process(target=upload_repo, args=(project_id,experiment_id,file_path,get_path_endpoint,post_zip_endpoint))
    p.start()
    return p