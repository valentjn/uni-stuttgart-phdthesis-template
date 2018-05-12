import os
import shlex
import subprocess
import sys

# check SCons version
EnsureSConsVersion(3, 0)

# we need at least Python 3.5, for example for subprocess.run
if sys.version_info < (3, 5):
  raise RuntimeError("These SCons scripts require Python 3.5 or newer. "
                     "Try running `python3 /usr/bin/scons` or similar.")

# class with helper methods
class Helper(object):
  # check if a dependency is installed, fail if not (if desired)
  @staticmethod
  def checkProgramInstalled(env, program, fail=False):
    if (not env.GetOption("help")) and (not env.GetOption("clean")):
      conf = Configure(env, log_file=None)
      result = (conf.CheckProg(program) is not None)
      if fail and (not result): raise RuntimeError(
          "Program \"{}\" required, but not found in PATH.".format(program))
      conf.Finish()
      return result
    else:
      return True
  
  # print and run command line, check=True by default
  @staticmethod
  def runCommand(args, check=True, **kwargs):
    print(" ".join([shlex.quote(arg) for arg in args]))
    return subprocess.run(args, **kwargs)

# set up environment, export environment variables of the shell
# (for example needed for custom TeX installations which need PATH)
env = Environment(ENV=os.environ)

# use timestamp to decide if a file should be rebuilt
# (otherwise SCons won't rebuild even if it is necessary)
env.Decider("timestamp-newer")

sconscripts = {}
dirs = ["bib", "gfx", "lua", "tex"]
createDirs = (not env.GetOption("help")) and (not env.GetOption("clean"))

for dir_ in dirs:
  # tell SConscript which its build directory is
  env.Replace(BUILD_DIR=env.Dir(os.path.join("build", dir_)))
  
  # create build directory
  if (dir_ != "lua") and createDirs: env.Execute(Mkdir(env["BUILD_DIR"]))
  # execute SConscript
  sconscripts[dir_] = env.SConscript(os.path.join(dir_, "SConscript"), exports="env")
  # clean up (scons -c)
  if dir_ != "lua": env.Clean(sconscripts[dir_], env["BUILD_DIR"])

# dependencies
env.Depends(sconscripts["tex"], [sconscripts[dir] for dir in dirs if dir != "tex"])
# install PDF
pdf_dir = env.Dir("pdf")
env.Execute(Mkdir(pdf_dir))
pdf = env.Install(pdf_dir, sconscripts["tex"])

# don't clean final PDF in pdf directory
env.NoClean(sconscripts["tex"], pdf)
