program control_test
use types, only : dp
use math
use control, only : state_space, ss, print_ss, sim_ss, arx, find_init_states

integer error 
type(state_space) sys

integer i, num_samp, na, nb
parameter(num_samp=100, na=4, nb=4, n_states = max(na, nb))
real(dp), dimension(num_samp) :: t, u, y, y_sim
real(dp) x0(n_states)

! Fill input and output arrays
do i = 1, num_samp
    t(i) = 0.1_dp*i
    u(i) = sin(0.2*t(i) + 0.2) + cos(0.1*t(i)) + sin(0.5*t(i))
    y(i) = u(i) + 0.5*rand()
end do

write(*,*) "t:"
!call print_array(t)

!write(*,*) "u:"
!call print_array(u)

!write(*,*) "y:"
!call print_array(y)

call arx(y, u, na, nb, sys, error, num_samp)
call print_ss(sys)

call find_init_states(sys, u, y, x0, num_samp)

x0 = 0.0_dp
write(*,*) "x0"
call print_array(x0)

call sim_ss(sys, u, x0, y_sim)

open(unit = 2, file = "sim.txt")

write(2,*) "t   u   y   y_sim"
do i = 1, num_samp
    write(2,*) t(i), u(i), y(i), y_sim(i)
end do

close(2)

end program control_test
