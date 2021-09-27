import os
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='details',
                                     usage='use "%(prog)s --help" for more information')
    parser.add_argument(
        '--argument', default=None,
        help='Usage python ROOTDIR *** Checks for preAuth annotation on public implementations. Writes output to preauth_missing_impl_list.txt  ')
    parser.add_argument('rootdir', nargs='*', default=[1], help='full path of files to check for preauth')
    args = parser.parse_args()

    print("PreAuth checking in dir: " + sys.argv[1])
    rootdir = sys.argv[1]

    preauth_missing_impl_list = set()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.__contains__('Impl.java'):
                with open(os.path.join(subdir, file)) as service_file:
                    lines = service_file.readlines()
                    service_file.close()
                    for service_line_count in range(lines.__len__()):
                        if lines[service_line_count].__contains__('public') and lines[service_line_count].__contains__(
                                'class'):
                            for pre_auth_seek in range(service_line_count, 0, -1):
                                if lines[pre_auth_seek].__contains__('preAuthorize') or lines[pre_auth_seek] == '':
                                    break
                            else:
                                preauth_missing_impl_list.add(subdir + ' : ' + file + '\n')
                                break
f = open("preauth_missing_impl_list.txt", "w")

if preauth_missing_impl_list.__len__() == 0:
    f.writelines('Nothing found ^_^"')
else:
    f.writelines(sorted(preauth_missing_impl_list))
f.close()
