#! /usr/bin/env python3

import os


class Rule(object):
    def __init__(self):
        pass

    def match(self, name):
        pass


class NameRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.names = []
        self.help = "NameRule's parameter should be string, or list of strings."

        if type(args) == str:
            self.names.append(args)
        elif type(args) == list or type(args) == tuple:
            for name in args:
                if type(name) != str:
                    raise Exception(self.help + " But %s is %s!" %
                                    (name, type(name)))
                self.names.append(name)
        else:
            raise Exception(self.help + " But it's %s!" % type(args))

    def match(self, name):
        name = os.path.basename(name)
        return name in self.names


class SuffixRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.suffixes = []
        self.help = "SuffixRule's parameter should be string, or list of strings."

        if type(args) == str:
            self.suffixes.append(args)
        elif type(args) == list or type(args) == tuple:
            for suff in args:
                if type(suff) != str:
                    raise Exception(self.help + " But %s is %s!" %
                                    (suff, type(suff)))
                self.suffixes.append(suff)
        else:
            raise Exception(self.help + " But it's %s!" % type(args))

    def match(self, name):
        for suff in self.suffixes:
            if name.endswith("." + suff):
                return True

        return False


def parse_size(s):
    s = s.strip()

    # parse_unit
    UNITS = ["b", "k", "m", "g"]
    unit = ""
    for x in UNITS:
        if s.endswith(x) and len(x) > len(unit):
            unit = x
    assert(unit in UNITS)

    # convert to bytes
    size = float(s[:-len(unit)].strip())
    if unit == "b":
        unit = 1
    elif unit == "k":
        unit = 1024
    elif unit == "m":
        unit = 1024 * 1024
    elif unit == "g":
        unit = 1024 * 1024 * 1024
    size = size * unit
    size = int(size)
    
    return size

def parse_size_limit(s):
    s = s.strip()

    # parse operator
    OPS = [">", "<", ">=", "<="]
    op = ""
    for x in OPS:
        if s.startswith(x) and len(x) > len(op):
            op = x
    assert(op in OPS)

    # parse size
    size = parse_size(s[len(op):])

    return (op, size)


def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


class FileSizeRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.help = "FileSizeRule's parameter shoule be string with format \"[>|<|>=|<=] [FLOAT][k|m|g]\""
        self.op = ""
        self.size = ""

        if type(args) != str:
            raise Exception(self.help + " But it's %s" % type(args))
        args = args.strip()

        try:
            self.op, self.size = parse_size_limit(args)
        except Exception as e:
            raise Exception(self.help)

    def match(self, path):
        if not os.path.isfile(path):
            return False

        size = os.path.getsize(path)
        if self.op == "<":
            return size < self.size
        elif self.op == ">":
            return size > self.size
        elif self.op == "<=":
            return size <= self.size
        elif self.op == ">=":
            return size >= self.size


class DirSizeRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.help = "DirSizeRule's parameter shoule be string with format \"[>|<|>=|<=] [FLOAT][k|m|g]\""
        self.op = ""
        self.size = ""

        if type(args) != str:
            raise Exception(self.help + " But it's %s" % type(args))
        args = args.strip()

        try:
            self.op, self.size = parse_size_limit(args)
        except Exception as e:
            raise Exception(self.help)

    def match(self, path):
        if not os.path.isdir(path):
            return False

        size = get_directory_size(path)
        if self.op == "<":
            return size < self.size
        elif self.op == ">":
            return size > self.size
        elif self.op == "<=":
            return size <= self.size
        elif self.op == ">=":
            return size >= self.size


class AndRule(Rule):
    def __init__(self, args):
        super().__init__()
        self.rules = []
        self.help = "AndRule's parameter shoud be list of rules."

        if type(args) != list:
            raise Exception(self.help + " But it's %s" % type(args))

        for rule in args:
            if type(rule) == dict:
                self.rules.append(OrRule(rule))
            elif type(rule) == str:
                raise Exception(
                    "Currenctly, there are no filters with no parameters, so what do you mean for %s" % rule)
            else:
                raise Exception(self.help)

    def match(self, name):
        for rule in self.rules:
            if not rule.match(name):
                #print("Don't match %s" % type(rule))
                return False
        return True


class OrRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.rules = []
        self.help = "OrRule's parameter shoud be list of rules, or dict of rules."

        if type(args) != list and type(args) != dict:
            raise Exception(self.help + " But it's %s" % type(args))

        if type(args) == list:
            for rule in args:
                if type(rule) == dict:
                    self.rules.append(OrRule(rule))
                elif type(rule) == str:
                    raise Exception(
                        "Currenctly, there are no filters with no parameters, so what do you mean for %s" % rule)
                else:
                    raise Exception(self.help)
        elif type(args) == dict:
            for rule in args:
                if type(rule) == str and rule in _RULE_PROCESSER:
                    proc = _RULE_PROCESSER[rule]
                    self.rules.append(proc(args[rule]))
                else:
                    raise Exception("Can't recognize rule %s" % rule)

    def match(self, name):
        for rule in self.rules:
            if rule.match(name):
                return True
            # print("Don't match %s" % type(rule))
        return False


class AlwaysTrueRule(Rule):
    def __init__(self):
        pass

    def match(self, name):
        return True


class AlwaysFalseRule(Rule):
    def __init__(self):
        pass

    def match(self, name):
        return False

_RULE_PROCESSER = {
    "name": NameRule,
    "suffix": SuffixRule,
    "file_size": FileSizeRule,
    "dir_size": DirSizeRule,
    "and": AndRule,
    "or": OrRule
}
