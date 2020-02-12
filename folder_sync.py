#!/usr/bin/env python3
"""
Program that produces a list of files that are present in one folder but not
another.
"""
import os
import argparse


def get_files(folder, extension):
    """
    Returns all files in a folder that match a given extension
    """
    all_files = [f for f in os.listdir(folder)
                 if os.path.isfile(os.path.join(folder, f))]
    filtered_files = [f for f in all_files if f.split('.')[1] == extension]
    return filtered_files


def get_differences(local_file_list, remote_file_list, ignore_extensions=True):
    """
    Returns a list of all files in the remote branch that do not exist in the
    local branch.
    """
    file_differences = []
    for remote_file in remote_file_list:
        for local_file in local_file_list:
            if ignore_extensions and remote_file.split('.')[0] in local_file:
                break
            if not ignore_extensions and remote_file in local_file_list:
                break
        else:
            file_differences.append(remote_file)
    return file_differences


def delete_files(path, files):
    """
    Delete all files found in the path
    """
    for filename in files:
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            print(f'Cannot file file: {file_path}')


def main():
    """
    Produces a list of all files that are present in one folder but not another
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--local',
                        default=os.getcwd(),
                        help='local filesystem to compare')
    parser.add_argument('-r', '--remote',
                        default=os.getcwd(),
                        help='remote filesystem to compare')
    parser.add_argument('-f', '--filetype',
                        required=True,
                        help='filetype to compare')
    parser.add_argument('-c', '--remote_filetype',
                        required=False,
                        help='files to compare in the destination')
    parser.add_argument('-v', '--verbose',
                        required=False,
                        help='display a list of files matched',
                        action='store_true')
    parser.add_argument('-d', '--delete',
                        required=False,
                        help='delete matched files',
                        action='store_true')
    args = parser.parse_args()
    files_local = get_files(args.local, args.filetype)
    if args.remote_filetype:
        files_remote = get_files(args.remote, args.remote_filetype)
    else:
        files_remote = get_files(args.remote, args.filetype)
    file_differences = get_differences(files_local, files_remote)
    if args.verbose:
        for filename in sorted(file_differences):
            print(os.path.join(args.remote, filename))
    if args.delete:
        delete_files(args.remote, file_differences)


if __name__ == '__main__':
    main()
