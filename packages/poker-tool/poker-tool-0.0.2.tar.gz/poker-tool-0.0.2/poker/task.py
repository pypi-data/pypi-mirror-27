#! /usr/bin/env pythons

import os
import shutil

import poker.ruler as ruler


class Task(object):
    def __init__(self, task_name, args):
        self.task_name = task_name
        self.src_root = args["directory"]

        if "match" in args:
            self.match = ruler.OrRule(args["match"])
        else:
            self.match = ruler.AlwaysTrueRule()

        if "ignore" in args:
            self.ignore = ruler.OrRule(args["ignore"])
        else:
            self.ignore = ruler.AlwaysFalseRule()

    def _dfs_search(self, current_dir, related_path):
        names = os.listdir(current_dir)
        ret = []
        for n in names:
            new_path = os.path.join(current_dir, n)
            new_related_path = os.path.join(related_path, n)
            
            if os.path.islink(new_path):
                # TODO: How to processing link need to be discussed
                continue

            match = self.match.match(new_path)
            ignore = self.ignore.match(new_path)
            if match and not ignore:
                ret.append(new_related_path)
            elif ignore:
                #print("ignore ", new_path)
                continue
            elif os.path.isdir(new_path):
                try:
                    ret += self._dfs_search(new_path, new_related_path)
                except Exception as e:
                    print("failed in searching", new_path)

        return ret

    def _search_matched_files(self):
        return self._dfs_search(self.src_root, "")

    def _copy_file(self, src_path, dst_path):
        dirname = os.path.dirname(dst_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        shutil.copyfile(src_path, dst_path)
        shutil.copystat(src_path, dst_path)

    def _copy_dir(self, src_path, dst_path):
        os.makedirs(dst_path, exist_ok=True)
        shutil.copystat(src_path, dst_path)

        for name in os.listdir(src_path):
            new_src_path = os.path.join(src_path, name)
            new_dst_path = os.path.join(dst_path, name)    
            self._copy(new_src_path, new_dst_path)

    def _copy(self, src_path, dst_path):
        # print(src_path)
        if os.path.isfile(src_path):
            self._copy_file(src_path, dst_path)
        elif os.path.isdir(src_path):
            self._copy_dir(src_path, dst_path)
        elif os.path.islink(src_path):
            # TODO: how to copy link?
            pass
        else:
            raise Exception("What's the type of file?")

    def collect(self, to):
        dst_root = os.path.join(to, self.task_name)
        os.mkdir(dst_root)

        files = self._search_matched_files()
        #print(files)
        failed = []
        for f in files:
            try:
                src_path = os.path.join(self.src_root, f)
                dst_path = os.path.join(dst_root, f)
                self._copy(src_path, dst_path)
            except Exception as e:
                failed.append(f)
        return failed
