############### Definitions

java_sources := $(wildcard *.java)
java_classes := $(subst .java,.class,$(java_sources))

sources := $(java_sources)
executables := $(java_classes)

############### Top level targets

.PHONY: build
build:  $(executables)

.PHONY: clean
clean:
	@echo "Deleteing java class files"
	@rm -f *.class

.PHONY: distclean
distclean: clean	
	@echo "Deleteing all generated files"
	@rm -f tags

tags: $(sources)
	ctags --recurse=yes

############### Explicit rules

%.class: %.java
	javac $<
