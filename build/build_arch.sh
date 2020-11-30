# build.sh - Build script for compiling Zorobot source code.

# Compile NLU for intent extraction.
# cc -c -o nlu.o nlu.c
# cc nlu.o -shared -o lib/models/nlu.so

# Compile Dialogue model.
# cc -c -o dialog.o dialog.c
#gc dialog.o -shared -o lib/models/dialog.so

# Compile Time Domain.
gcc -c -fPIC -I/usr/include/python3.8 -o kronos.o kronos.c
gcc -shared -fPIC -I/usr/include/python3.8 -o kronos.so kronos.o

gcc -c -fPIC -I/usr/include/python3.8 -o scheduler.o lib/c/scheduler.c
gcc -shared -fPIC -I/usr/include/python3.8 -o lib/ext/scheduler.so scheduler.o
