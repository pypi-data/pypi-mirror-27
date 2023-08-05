# MAKEFILE for scs
include scs.mk

SCS_OBJECTS = src/scs.o src/util.o src/cones.o src/accel.o src/cs.o src/linalg.o src/ctrlc.o src/scs_version.o src/normalize.o

SRC_FILES = $(wildcard src/*.c)
INC_FILES = $(wildcard include/*.h)

CFLAGS += $(OPT_FLAGS)
CUDAFLAGS += $(OPT_FLAGS)

AMD_SOURCE = $(wildcard $(DIRSRCEXT)/amd_*.c)
DIRECT_SCS_OBJECTS = $(DIRSRCEXT)/ldl.o $(AMD_SOURCE:.c=.o)
TARGETS = $(OUT)/demo_socp_indirect $(OUT)/demo_socp_direct

.PHONY: default

default: $(TARGETS) $(OUT)/libscsdir.a $(OUT)/libscsindir.a $(OUT)/libscsdir.$(SHARED) $(OUT)/libscsindir.$(SHARED)
	@echo "****************************************************************************************"
	@echo "Successfully compiled scs, copyright Brendan O'Donoghue 2012."
	@echo "To test, type '$(OUT)/demo_socp_indirect' to solve a random SOCP."
	@echo "**********************************************************************************"
ifneq ($(USE_LAPACK), 0)
	@echo "Compiled with blas and lapack, can solve LPs, SOCPs, SDPs, ECPs, and PCPs"
else
	@echo "NOT compiled with blas/lapack, cannot solve SDPs (can solve LPs, SOCPs, ECPs, and PCPs)."
	@echo "To solve SDPs, install blas and lapack, then edit scs.mk to set USE_LAPACK=1"
	@echo "and point to the library install locations, and recompile with 'make purge', 'make'."
endif
	@echo "****************************************************************************************"

%.o : src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

src/scs.o	: $(SRC_FILES) $(INC_FILES)
src/util.o	: src/util.c include/util.h include/constants.h
src/cones.o	: src/cones.c include/cones.h include/scs_blas.h
src/accel.o	: src/accel.c include/accel.h include/scs_blas.h
src/cs.o	: src/cs.c include/cs.h
src/linalg.o: src/linalg.c include/linalg.h
src/ctrl.o  : src/ctrl.c include/ctrl.h
src/scs_version.o: src/scs_version.c include/constants.h

$(DIRSRC)/private.o: $(DIRSRC)/private.c  $(DIRSRC)/private.h
$(INDIRSRC)/indirect/private.o: $(INDIRSRC)/private.c $(INDIRSRC)/private.h
$(LINSYS)/common.o: $(LINSYS)/common.c $(LINSYS)/common.h

$(OUT)/libscsdir.a: $(SCS_OBJECTS) $(DIRSRC)/private.o $(DIRECT_SCS_OBJECTS) $(LINSYS)/common.o
	mkdir -p $(OUT)
	$(ARCHIVE) $@ $^
	- $(RANLIB) $@

$(OUT)/libscsindir.a: $(SCS_OBJECTS) $(INDIRSRC)/private.o $(LINSYS)/common.o
	mkdir -p $(OUT)
	$(ARCHIVE) $@ $^
	- $(RANLIB) $@

$(OUT)/libscsdir.$(SHARED): $(SCS_OBJECTS) $(DIRSRC)/private.o $(DIRECT_SCS_OBJECTS) $(LINSYS)/common.o
	mkdir -p $(OUT)
	$(CC) $(CFLAGS) -shared -Wl,$(SONAME),$(@:$(OUT)/%=%) -o $@ $^ $(LDFLAGS)

$(OUT)/libscsindir.$(SHARED): $(SCS_OBJECTS) $(INDIRSRC)/private.o $(LINSYS)/common.o
	mkdir -p $(OUT)
	$(CC) $(CFLAGS) -shared -Wl,$(SONAME),$(@:$(OUT)/%=%) -o $@ $^ $(LDFLAGS)

$(OUT)/demo_socp_direct: test/random_socp_prob.c $(OUT)/libscsdir.a
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(OUT)/demo_socp_indirect: test/random_socp_prob.c $(OUT)/libscsindir.a
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# basic testing
.PHONY: test
test: $(OUT)/run_tests
$(OUT)/run_tests: test/run_tests.c $(OUT)/libscsindir.a
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) -Itest

# REQUIRES GPU AND CUDA INSTALLED
gpu: $(OUT)/demo_socp_gpu $(OUT)/libscsgpu.$(SHARED) $(OUT)/libscsgpu.a

$(GPU)/private.o: $(GPU)/private.c
	$(CUCC) -c -o $(GPU)/private.o $^ $(CUDAFLAGS)

$(OUT)/libscsgpu.$(SHARED): $(SCS_OBJECTS) $(GPU)/private.o $(LINSYS)/common.o
	mkdir -p $(OUT)
	$(CC) $(CFLAGS) -shared -Wl,$(SONAME),$(@:$(OUT)/%=%) -o $@ $^ $(LDFLAGS) $(CULDFLAGS)

$(OUT)/libscsgpu.a: $(SCS_OBJECTS) $(GPU)/private.o $(LINSYS)/common.o
	mkdir -p $(OUT)
	$(ARCHIVE) $@ $^
	- $(RANLIB) $@

$(OUT)/demo_socp_gpu: test/random_socp_prob.c $(OUT)/libscsgpu.a
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) $(CULDFLAGS)

.PHONY: clean purge
clean:
	@rm -rf $(TARGETS) $(SCS_OBJECTS) $(DIRECT_SCS_OBJECTS) $(LINSYS)/*.o $(DIRSRC)/*.o $(INDIRSRC)/*.o $(GPU)/*.o
	@rm -rf $(OUT)/*.dSYM
	@rm -rf matlab/*.mex*
	@rm -rf .idea
	@rm -rf python/*.pyc
	@rm -rf python/build
purge: clean
	@rm -rf $(OUT)

