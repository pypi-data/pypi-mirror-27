from subprocess import call
from typing import List
import os


class Compiler:
    def __init__(self, cc_exe: str, flags: List[str]):
        self.cc_exe = cc_exe
        self.flags = flags

    def compile(self, src: str, target: str, verbose: bool = False) -> bool:
        if verbose:
            print(self.cmd_str(src, target))

        return call([self.cc_exe, *self.flags, "-c", src, "-o", target]) == 0

    def cmd_str(self, src: str, target: str) -> str:
        return self.cc_exe + " " + ' '.join(self.flags) + " -c " + src + " -o " + target

class Linker:
    def __init__(self, ld_exe, flags: List[str]):
        self.ld_exe = ld_exe
        self.flags = flags

    def link(self, obj: List[str], target: str, verbose: bool = False) -> bool:
        if verbose:
            print(self.cmd_str(obj, target))

        return call([self.ld_exe, *self.flags, *obj, "-o", target]) == 0

    def cmd_str(self, obj: List[str], target: str) -> str:
        return self.ld_exe + " " + ' '.join(self.flags) + " " + ' '.join(obj) + " -o " + target


class Archiver:
    def __init__(self, ar_exe, flags: List[str]):
        self.ar_exe = ar_exe
        self.flags = flags

    def archive(self, obj: List[str], target: str, verbose: bool = False) -> bool:
        if verbose:
            print(self.cmd_str(obj, target))

        return call([self.ar_exe, *self.flags, target, *obj]) == 0

    def cmd_str(self, obj: List[str], target: str) -> str:
        return self.ar_exe + " " + ' '.join(self.flags) + " " + target + " " + ' '.join(obj)


class Toolchain:
    def __init__(self, cc: Compiler, ld: Linker, ar: Archiver, verbose: bool = False):
        self.cc = cc
        self.ld = ld
        self.ar = ar
        self.verbose = verbose

    def compile(self, src: str, target: str) -> bool:
        return self.cc.compile(src, target, self.verbose)

    def link(self, obj: List[str], target: str) -> bool:
        return self.ld.link(obj, target, self.verbose)

    def archive(self, obj: List[str], target: str) -> bool:
        return self.ar.archive(obj, target, self.verbose)


# Get the default toolchain
def default_toolchain() -> Toolchain:
    cc_exe: str = os.environ.get("CC")
    cflags: str = os.environ.get("CFLAGS")

    ld_exe: str = os.environ.get("LD")
    ldflags: str = os.environ.get("LDFLAGS")

    ar_exe: str = os.environ.get("AR")
    arflags: str = os.environ.get("ARFLAGS")

    if cc_exe is None:
        cc_exe = "cc" # Guess executable
    if ld_exe is None:
        ld_exe = cc_exe # Default to C compiler
    if ar_exe is None:
        ar_exe = "ar" # Guess executable

    cc = Compiler(cc_exe, [] if cflags is None else cflags.split(" "))
    ld = Linker(ld_exe, [] if ldflags is None else ldflags.split(" "))
    ar = Archiver(ar_exe, [] if arflags is None else arflags.split(" "))

    return Toolchain(cc, ld, ar, True)
