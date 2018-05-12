import os
import sys

# check SCons version
EnsureSConsVersion(3, 0)

# we need at least Python 3.5, for example for subprocess.run
if sys.version_info < (3, 5):
  raise RuntimeError("These SCons scripts require Python 3.5 or newer. "
                     "Try running `python3 /usr/bin/scons` or similar.")

# set up environment, export environment variables of the shell
# (for example needed for custom TeX installations which need PATH)
env = Environment(ENV=os.environ)

# use timestamp to decide if a file should be rebuilt
# (otherwise SCons won't rebuild even if it is necessary)
env.Decider("timestamp-newer")

sconscripts = {}
dirs = ["bib", "gfx", "tex"]

for dir in dirs:
  # tell SConscript which its build directory is
  env.Replace(BUILD_DIR=env.Dir("build/{}".format(dir)))
  # create build directory
  env.Execute(Mkdir(env["BUILD_DIR"]))
  # execute SConscript
  sconscripts[dir] = env.SConscript("{}/SConscript".format(dir), exports="env")
  # clean up (scons -c)
  env.Clean(sconscripts[dir], env["BUILD_DIR"])

# dependencies
env.Depends(sconscripts["tex"], [sconscripts[dir] for dir in dirs if dir != "tex"])
# install PDF
pdf_dir = env.Dir("pdf")
env.Execute(Mkdir(pdf_dir))
pdf = env.Install(pdf_dir, sconscripts["tex"])

# don't clean final PDF in pdf directory
env.NoClean(sconscripts["tex"], pdf)
