import sys
import json
from datetime import datetime

arguements = sys.argv

script_name = sys.argv[0]
task_type = sys.argv[1]


with open('./data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

if(task_type == "add"):
    task_content = sys.argv[2]
    if(len(data) == 0):
        next_id = 1
    else:
        next_id = data[-1]["id"] + 1
    data.append({
        "id" : next_id,
        "description" : task_content,
        "createdAt" : datetime.now().isoformat(),
        "updatedAt" : datetime.now().isoformat()
    })
    with open('./data.json','w') as file:
        json.dump(data,file,indent=4)

if(task_type == "update"):
    cur_task_id = sys.argv[2]
    task_update_content = sys.argv[3]
    for i in range(0,len(data)):
        if(data[i]["id"] == int(cur_task_id)):
            data[i]["description"] = task_update_content
            data[i]["updatedAt"] = datetime.now().isoformat()
    with open('./data.json','w') as file:
        json.dump(data,file,indent=4)

if(task_type == "delete"):
    to_delete_task_id = sys.argv[2]

print(data)