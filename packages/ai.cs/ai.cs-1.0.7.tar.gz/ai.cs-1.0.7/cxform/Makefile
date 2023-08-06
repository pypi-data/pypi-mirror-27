# CXFORM multi-purpose makefile
#
# 2000/06/14: Ed Santiago - Original version
# 2003/09/12: Ryan Boller - Modified for multiple platforms/languages
# 2004/03/18: Ryan Boller - Modified for OS auto-detect, Mac compatibility
# 2009/11/25: Ryan Boller - Added compiler flags for 64-bit Mac platform
# 2017/11/30: Alexey Isavnin - Modified for the Python package ai.cs

# NOTE: If using MS Windows, this Makefile is only useful for gcc/cygwin builds.

all:
ifdef SYSTEMROOT
	@echo "OS type detected: Windows"
	make dll-c
else
	make so-c
endif

# Detect which OS is running and select appropriate flags
so-c:
	@echo "OS type detected: "`uname`
	@case `uname` in \
		"SunOS")  make sun-cxform-c.so \
				"CFLAGS=-fPIC -shared" ;;\
		"Darwin") make mac-cxform-c.so \
				"CFLAGS=-fPIC -arch x86_64 -arch i386 -arch ppc -arch ppc64" ;;\
		"Linux")  make linux-cxform-c.so \
				"CFLAGS=-fPIC -shared" ;;\
		*) echo "This operating system is not supported -- use make dll-c if under MS Windows" ;;\
	esac

dll-c:		
	make cxform-c.dll "CFLAGS=-Wall -shared -g"

# MAC-SPECIFIC
mac-cxform-c.so: cxform-auto.o  cxform-manual.o
	gcc -arch x86_64 -arch i386 -arch ppc -arch ppc64 -flat_namespace -undefined suppress -bundle -o cxform-c.so $^

# LINUX-SPECIFIC
linux-cxform-c.so: cxform-auto.o  cxform-manual.o
	ld -G -lm -o cxform-c.so $^

# SUN-SPECIFIC
sun-cxform-c.so: cxform-auto.o  cxform-manual.o
	ld -G -lm -o cxform-c.so $^

# WINDOWS-SPECIFIC
cxform-c.dll: cxform-auto.o  cxform-manual.o
	gcc -shared $^ -o $@

#######################
clean:
	rm -f *.so *.sl *.o *.obj cxform.dll cxform-c.dll
