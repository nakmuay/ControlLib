program lapack_test
use types, only : dp
use math
implicit none

real(dp), dimension(2, 2) :: A, Ainv, I

A(1, 1) = 11
A(2, 1) = 2
A(1, 2) = -3
A(2, 2) = 10

write (*,*) "A:"
call print_matrix(A)
write (*,*)

Ainv = inv(A)
write (*,*) "Ainv:"
call print_matrix(Ainv)
write (*,*)

I = matmul(A, Ainv)
write (*,*) "I:"
call print_matrix(I)

end program lapack_test
