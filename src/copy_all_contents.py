import os
import shutil


def copy_all_contents(source_dir, destination_dir):

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    os.mkdir(destination_dir)

    for file in os.listdir(source_dir):
        source_full_path = os.path.join(source_dir, file)

        destination_full_path = os.path.join(destination_dir, file)

        if os.path.isfile(source_full_path):
            path = shutil.copy(source_full_path, destination_full_path)
            print(f"Copied Path: {path}")

        else:
            copy_all_contents(source_full_path, destination_full_path)




