import sys
sys.path.append("..")
import json
from pathlib import Path
from utils.file_utils import remove_file

session_path=Path("/media/dataset-harddisk/sumit/zspeech/tasks/annotation/zvoice_call_recordings_30/review_sessions/sessions")

all_files={}
for i in range(1,6):
    session=session_path/f"session{i}"/"completions"
    json_files=list(session.glob("*.json"))
    files_to_remove=[]
    for file in json_files:
        try:
            with open(file)as fp:
                data=json.load(fp)
            if len(data)==0:
                files_to_remove.append(str(file))
        except:
            files_to_remove.append(str(file))
    all_files[session.parent.name]=files_to_remove
    
for k,v in all_files.items():
    for file in v:
        print(file)
        # remove_file(file)