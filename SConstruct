import os

# increase line length of LuaLaTeX error log lines by setting environment variables
os.environ["max_print_line"] = "1000"
os.environ["error_line"] = "254"
os.environ["half_error_line"] = "238"

# set up environment, export environment variables of the shell
# (for example needed for custom TeX installations which need PATH)
env = Environment(ENV=os.environ)

# use LuaLaTeX as compiler (successor of PDFLaTeX)
env.Replace(PDFLATEX="texfot lualatex")
# don't call BibTeX on *.aux files of chapters
env.Replace(BIBTEXCOM="")
# quiet Biber output
env.Append(BIBERFLAGS="-q")
# use makeglossaries instead of directly calling makeindex
env.Replace(MAKEGLOSSARY="makeglossaries")
# quiet makeglossaries output
env.Replace(MAKEGLOSSARYFLAGS="-q")
# reorder arguments for makeglossaries
# (filename without extension has to be at the end)
env.Replace(MAKEGLOSSARYCOM=env["MAKEGLOSSARYCOM"].replace(
    "${SOURCE.filebase}.glo $MAKEGLOSSARYFLAGS -o ${SOURCE.filebase}.gls",
    "$MAKEGLOSSARYFLAGS -o ${SOURCE.filebase}.gls ${SOURCE.filebase}"))

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
