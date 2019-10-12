import os
import re
import sys
import zipfile
from shutil import copy2

def load_class_dictionary(students_file, students_dict):
    with open(students_file, 'r') as source:
        matches = re.findall(r'^"(.+?)"."(.+?)"."(\d+?)"', source.read(), re.MULTILINE)

    for (last_name, first_name, student_id) in matches:
        if student_id in students_dict:
            raise RuntimeError("Student ID appears twice in class list.")
        students_dict[student_id] = last_name + " " + first_name


def get_id_from_file(file_name):
    match = re.search(r'_(\d+)_attempt_', file_name)
    if match:
        return match.group(1)
    else:
        return None


def main():
    if len(sys.argv) != 4:
        print("Usage: organizer.py class_list.csv source_dir target_dir");
        return

    students_file = sys.argv[1]
    source_directory = sys.argv[2]
    target_directory = sys.argv[3]

    if os.path.isdir(target_directory):
        if len(os.listdir(target_directory)) > 0:
            print("Target directory is not empty.")
            return
    else:
        os.mkdir(target_directory)

    students_dict = dict()
    load_class_dictionary(students_file, students_dict)

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            id = get_id_from_file(file)
            if id == None:
                print("Could not find studentID in filename for: " + file)
                continue

            source = root + '/' + file
            target = target_directory + '/' + students_dict[id] + ' ' + id

            if not os.path.isdir(target):
                os.mkdir(target)

            if file.endswith('.zip'):
                print("Extracting: " + source)
                zip_ref = zipfile.ZipFile(source, 'r')
                zip_ref.extractall(target)
                zip_ref.close()
            else:
                print("Copying: " + source)
                copy2(source, target)

    print("Done!")


if __name__ == '__main__':
    main()
