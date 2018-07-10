program arx_test
use types, only : dp
use math
use control
implicit none

integer :: n, na, nb, i, arx_error
parameter (n=10)
parameter (na=3)
parameter (nb=2)
real(dp), dimension(n) :: y, u
real(dp) sys(na + nb)

! Fill arrays
do i = 1, n
    u(i) = i
    y(i) = 10*i + 1
end do

write (*,*) "u: "
call print_array(u)
write (*,*) ""

write (*,*) "y: "
call print_array(y)
write (*,*) ""

arx_error = 0
call arx(y, u, na, nb, sys, arx_error, n)
write (*,*) "arx_error: ", arx_error

write (*,*) "sys"
call print_array(sys)
end program
