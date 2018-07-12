program control_test
use types, only : dp
use math
use control, only : state_space, ss, print_ss, sim_ss, arx

integer error 
parameter (num_coeffs=2, den_coeffs=4)
type(state_space) sys

integer i, num_samp
parameter(num_samp=20)
real(dp), dimension(num_samp) :: t, u, y, y_hat

! Fill input and output arrays
do i = 1, num_samp
    t(i) = i
end do
u = sin(0.2 * t)
y = u * u

write(*,*) "t:"
call print_array(t)

write(*,*) "u:"
call print_array(u)

write(*,*) "y:"
call print_array(y)

call arx(y, u, 2, 1, sys, error, num_samp)

call sim_ss(sys, u, y_hat)

call print_ss(sys)

write(*,*) "u       y       y_hat"
do i = 1, num_samp
    write(*,*) u(i), y(i), y_hat(i)
end do

end program control_test
