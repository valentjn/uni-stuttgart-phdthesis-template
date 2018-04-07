# Only use this Makefile if you insist on using latexmk.
# The recommended way to build is `scons`.
# This Makefile copies almost all needed files to build/tex/, as
# latexmk supports neither TEXINPUTS (environment variable) nor
# `\graphicspath` (LaTeX command).
# Important: If you want to run latexmk in the `-pvc` mode
# (watch for file changes), then you need to work on the copied files
# in build/tex/.

# external Makefile that will be created in build/tex/Makefile
define BUILD_MAKEFILE
# =====================================================================
# The current directory is now build/tex/!

thesis.gls:
# build glossary
	python3 ../../tools/buildGlossary.py -q -o thesis.gls thesis

.DEFAULT:
# unknown target should be a graphics file
# run SCons to generate the graphics file if necessary
	scons -C ../.. build/gfx/$$@
# copy graphics from build/gfx/ to build/tex/,
# because latexmk doesn't support \graphicspath...
	cp ../gfx/$$@ ./
# =====================================================================
endef
export BUILD_MAKEFILE

# additional arguments for latexmk
#LATEXMK_ARGS := -pvc

# phony targets
.PHONY: all pdf/thesis.pdf gfx clean cleanall

# make all target
all: pdf/thesis.pdf

# compile the thesis
pdf/thesis.pdf:
# create directories
	mkdir -p build/bib/ build/tex/
# copy *.bib file
# (-u option for the case if -pvc is enabled and the user changed
# some files in build/tex/)
	cp -u bib/*.bib build/bib/
# copy *.lua and *.tex files
	cp -u lua/*.lua tex/* build/tex/
# create the build Makefile (see above)
	echo "$$BUILD_MAKEFILE" > build/tex/Makefile
# hack build/tex/settings.tex: remove \graphicspath
# because latexmk doesn't support it
	sed -i -e 's/\\graphicspath{{\.\.\/gfx\/}}//g' \
		build/tex/settings.tex
# run latexmk
	latexmk -lualatex -shell-escape -interaction=nonstopmode \
		-cd -use-make ${LATEXMK_ARGS} build/tex/thesis.tex
# copy result to pdf/
	cp build/tex/thesis.pdf pdf/thesis.pdf

# manually generate all graphics:
# latexmk will not regenerate a graphics *.pdf if you've changed
# the corresponding Python code. `make gfx` regenerates all graphics,
# `scons build/gfx/GRAPHICS_NAME.pdf` only a single graphics file.
gfx:
	scons build/gfx/

# cleans all files except build/tex/*.tex (security measure)
clean:
	rm -rf build/bib/
	find build/tex/ -maxdepth 1 -type f -not -name '*.tex' -delete

# cleans all files
# (don't use this if you have latexmk's `-pvc` option enabled!)
cleanall:
	rm -rf build/
