# gTaskList = ["[ ] Do this", "[x] Do that", "[ ] Don't do this", "[ ] A quick brown fox jumps over a lazy dog"]
gTaskList = []

class MyColors():
    SUPERGREY = "#121212"
    ULTRAGREY = "#090909"

def readFile():
    try: open("random_task_list.txt", "r")
    except:
        with open("random_task_list.txt", "w") as f: pass
    with open("random_task_list.txt", "r") as f:
        for line in f.readlines():
            gTaskList.append(line[:-1])
        # print(gTaskList)

def writeFile(content: list):
    full_string = ""
    for item in content: full_string = full_string + item + "\n"
    with open("random_task_list.txt", "w") as f:
        f.write(full_string[:-1])
        # f.writelines(content)
