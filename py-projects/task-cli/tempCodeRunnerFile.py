arguements = sys.argv

# script_name = sys.argv[0]
# task_type = sys.argv[1]
# task_content = sys.argv[2]

# with open('./data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# if(task_type == "add"):
#     if(len(data) == 0):
#         next_id = 1
#     else:
#         next_id = data[-1]["id"] + 1
#     data.append({
#         "id" : next_id,
#         "description" : task_content,
#         "createdAt" : datetime.now().isoformat(),
#         "updatedAt" : datetime.now().isoformat()
#     })