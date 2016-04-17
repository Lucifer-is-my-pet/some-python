from PIL import Image
import os
# import time
import sys

# ----------------------------------------------------------------------------------------------------
# имя папки пишется в двойных кавычках после названия скрипта, использовать "\", в конце "\" не нужон!
# ----------------------------------------------------------------------------------------------------

work_dir = sys.argv[1]
filenames = os.listdir(work_dir)
# t = time.localtime()
# print(str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec))

full_filenames = [work_dir + "\\" + x for x in filenames]

for name in full_filenames:
    img = Image.open(name)
    size = img.size
    new_name = name[:-4] + "_new.png"
    if size[0] > 3000:
        new_img = img.resize((int(size[0] * 0.4), int(size[1] * 0.4)), Image.ANTIALIAS)
    else:
        new_img = img.resize((int(size[0] * 0.5), int(size[1] * 0.5)), Image.ANTIALIAS)
    img.close()
    new_img.save(new_name)

# t = time.localtime()
# print(str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec))