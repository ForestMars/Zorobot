.PHONY: clean build build-source build-arch build-local

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    build"
	@echo "        Alias for build-arch"
	@echo "    build-source"
	@echo "        Compile Cython code to c extension."
	@echo "    build-arch"
	@echo "        Compile c source code into executable binaries."
	@echo "    build-local"
	@echo "        Compile Cython code into executable binaries."


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

build:
	build/build_arch.sh

build-source:
	build/build_source.sh

build-arch:
	build/build_arch.sh

build-local:
	build/src/build_local.sh
