# Copyright (c) Hello Robot, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in the root directory
# of this source tree.
#
# Some code may be adapted from other open-source works with their respective licenses. Original
# license information maybe found below, if so.

"""
This is a tool to add license headers to all files in the repo.
"""


import os


def read_license_header(file_path):
    with open(file_path, "r") as file:
        return file.read()


def check_and_add_license_header(file_path, license_header):
    with open(file_path, "r") as file:
        content = file.read()

    if not content.startswith(license_header):
        with open(file_path, "w") as file:
            file.write(license_header + "\n" + content)
        print(f"Added license header to {file_path}")
    else:
        print(f"License header already present in {file_path}")


def main(directory, license_file):
    license_header = read_license_header(license_file)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                check_and_add_license_header(file_path, license_header)


if __name__ == "__main__":
    directory = "."  # Change to the directory you want to check
    license_file = "docs/license_header.txt"  # Path to your license header file
    main(directory, license_file)
