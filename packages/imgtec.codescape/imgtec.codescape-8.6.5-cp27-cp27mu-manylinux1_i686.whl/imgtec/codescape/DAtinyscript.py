# This file exists only for backwards compatibility with CSUtils.
def CreateDAtiny(*args, **kwargs):
    from imgtec.codescape import DAscript
    return DAscript.CreateDAtiny(*args, **kwargs)