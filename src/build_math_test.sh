gfortran types.f03 math.f03 math_test.f03 -Llib -llapack -lblas -o math_test

# Clean up mod files
rm *.mod
