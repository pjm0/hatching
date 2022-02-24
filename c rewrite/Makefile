all: sphere process

sphere: shader.c sphere.c lib.c lib.h
	gcc -o sphere lib.c shader.c sphere.c -lm

process: shader.c process.c lib.c lib.h
	gcc -o process process.c lib.c shader.c -lm