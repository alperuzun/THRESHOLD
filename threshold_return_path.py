import os
current_script_path = os.path.abspath(__file__)
path = current_script_path[:-24]
print(path)

with open("path.txt", "w") as file:
    pass

with open("path.txt", "w") as file:
    file.write(path)
