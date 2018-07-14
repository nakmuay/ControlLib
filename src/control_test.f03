program control_test
use types, only : dp
use math
use control, only : state_space, ss, print_ss, sim_ss, arx

integer error 
type(state_space) sys

integer i, num_samp
parameter(num_samp=300)
real(dp), dimension(num_samp) :: t, u, y, y_sim

! Fill input and output arrays
do i = 1, num_samp
    t(i) = 0.1_dp*i
end do
u = sin(0.2 * t)
y = u * u

write(*,*) "t:"
call print_array(t)

!write(*,*) "u:"
!call print_array(u)

!write(*,*) "y:"
!call print_array(y)

call arx(y, u, 2, 1, sys, error, num_samp)

call sim_ss(sys, u, y_sim)

call print_ss(sys)

open(unit = 2, file = "sim.txt")

write(2,*) "t   u   y   y_sim"
do i = 1, num_samp
    write(2,*) t(i), u(i), y(i), y_sim(i)
end do

close(2)

end program control_test
