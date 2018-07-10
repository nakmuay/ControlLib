program math_test
use types, only : dp
use math
implicit none

integer m, n
parameter (m=3, n=2)
real(dp) :: A(m, n), Y(m), X(n)

! Fill A
A(1, 1) = 0
A(2, 1) = 1
A(3, 1) = 4
A(1, 2) = 0
A(2, 2) = 1
A(3, 2) = 2

! Fill Y
Y(1) = 0
Y(2) = -0.2
Y(3) = 1.6

call least_squares(A, Y, X)
write (*,*) "X"
call print_array(X)

end program math_test
