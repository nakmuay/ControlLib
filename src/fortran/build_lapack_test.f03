gfortran types.f03 math.f03 lapack_test.f03 -Llib -llapack -lblas -o lapack_test

# Clean up mod files
rm *.mod
