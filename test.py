import os
path = r"C:\Dev\the_snake\the_snake.py"
assert os.path.isfile(path)
with open(path, "r") as f:
    pass