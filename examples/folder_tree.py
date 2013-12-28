#!/usr/bin/env python
# A file folder scanner contributed by @holger 
#
# You can spicify the scanned folder and file pattern by changing rootPath
# and pattern variables
#

__author__ = 'holger'

from treelib import tree

import fnmatch
import os
import zlib
import argparse

DEBUG = 0
FILECOUNT = 0
DIRCOUNT = 0
DIR_ERRORLIST = []
FILE_ERRORLIST = []


# Time Profiling
PROFILING = 0
# 0 - nothing
# 1 - time
# 2 - cProfile

if PROFILING == 1:
    import timeit
if PROFILING == 2:
    import cProfile


parser = argparse.ArgumentParser(description='Scan the given folder and print its structure in a tree.')
parser.add_argument('abspath', type=str, help= 'An absolute path to be scanned.')
parser.add_argument('pattern', type=str, help= 'File name pattern to filtered, e.g. *.pdf')

args = parser.parse_args()
rootPath = args.abspath
pattern = args.pattern

folder_blacklist = []

dir_tree = tree.Tree()
dir_tree.create_node('Root', rootPath)  # root node


def crc32(data):
    data = bytes(data, 'UTF-8')

    if DEBUG:
        print('++++++ CRC32 ++++++')
        print('input: ' + str(data))
        print('crc32: ' + hex(zlib.crc32(data) & 0xffffffff))
        print('+++++++++++++++++++')
    return hex(zlib.crc32(data) & 0xffffffff)  # crc32 returns a signed value, &-ing it will match py3k

parent = rootPath
i = 1

# calculating start depth
start_depth = rootPath.count('/')


def get_noteid(depth, root, dir):
    """ get_noteid returns
        - depth contains the current depth of the folder hierarchy
        - dir contains the current directory

        Function returns a string containing the current depth, the folder name and unique ID build by hashing the
        absolute path of the directory. All spaces are replaced by '_'

        <depth>_<dirname>+++<crc32>
        e.g. 2_Folder_XYZ_1+++<crc32>
    """
    return str(str(depth) + '_' + dir).replace(" ", "_") + '+++' + crc32(os.path.join(root, dir))

# TODO: Verzeichnistiefe pruefen: Was ist mit sowas /mp3/


def get_parentid(current_depth, root, dir):
    # special case for the 'root' of the tree
    # because we don't want a cryptic root-name
    if current_depth == 0:
        return root

    # looking for parent directory
    # e.g. /home/user1/mp3/folder1/parent_folder/current_folder
    # get 'parent_folder'

    search_string = os.path.join(root, dir)
    pos2 = search_string.rfind('/')
    pos1 = search_string.rfind('/', 0, pos2)
    parent_dir = search_string[pos1 + 1:pos2]
    parentid = str(current_depth - 1) + '_' + parent_dir.replace(" ", "_") + '+++' + crc32(root)
    return parentid
    # TODO: catch error



def print_node(dir, node_id, parent_id):
    print('#############################')
    print('node created')
    print('      dir:     ' + dir)
    print('      note_id: ' + node_id)
    print('      parent:  ' + parent_id)


def crawler():
    global DIRCOUNT
    global FILECOUNT

    for root, dirs, files in os.walk(rootPath):

        # +++ DIRECTORIES +++
        for dir in dirs:

            # calculating current depth
            current_depth = os.path.join(root, dir).count('/') - start_depth

            if DEBUG:
                print('current: ' + os.path.join(root, dir))

            node_id = get_noteid(current_depth, root, dir)
            parent_id = str(get_parentid(current_depth, root, dir))

            if parent_id == str(None):
                DIR_ERRORLIST.append(os.path.join(root, dir))

            if DEBUG:
                print_node(dir, node_id, parent_id)

            # create node
            dir_tree.create_node(dir, node_id, parent_id)
            DIRCOUNT += 1

        # +++ FILES +++
        for filename in fnmatch.filter(files, pattern):

            if dir in folder_blacklist:
                continue

            # calculating current depth
            current_depth = os.path.join(root, filename).count('/') - start_depth

            if DEBUG:
                print('current: ' + os.path.join(root, filename))

            node_id   = get_noteid(current_depth, root, filename)
            parent_id = str(get_parentid(current_depth, root, filename))

            if parent_id == str(None):
                FILE_ERRORLIST.append(os.path.join(root, dir))

            if DEBUG:
                print_node(filename, node_id, parent_id)

            # create node
            dir_tree.create_node(filename, node_id, parent_id)
            FILECOUNT += 1


if PROFILING == 0:
    crawler()
if PROFILING == 1:
    t1 = timeit.Timer("crawler()", "from __main__ import crawler")
    print('time:      ' + str(t1.timeit(number=1)))
if PROFILING == 2:
    cProfile.run("crawler()")


print('filecount: ' + str(FILECOUNT))
print('dircount:  ' + str(DIRCOUNT))

if DIR_ERRORLIST:
    for item in DIR_ERRORLIST:
        print(item)
else:
    print('no directory errors')

print('\n\n\n')

if FILE_ERRORLIST:
    for item in FILE_ERRORLIST:
        print(item)
else:
    print('no file errors')

print('nodes: ' + str(len(dir_tree.nodes)))

dir_tree.show()




