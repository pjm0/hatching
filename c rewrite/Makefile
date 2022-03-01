all: linted sphere process clean

linted: shader.c process.c sphere.c lib.c lib.h
	astyle --style=linux *.c *.h
	rm *.orig -f

sphere: shader.c sphere.c lib.c lib.h
	gcc -Wall -o sphere lib.c shader.c sphere.c -lm

process: shader.c process.c lib.c lib.h
	gcc -Wall -o process process.c lib.c shader.c -lm

clean:
	rm *.old *.orig -f