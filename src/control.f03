module control
use types
use math
implicit none

private
public  arx, &
        ss, &
        state_space, &
        print_ss, &
        sim_ss

type state_space
    real(dp), allocatable :: A(:,:)
    real(dp), allocatable :: B(:)
    real(dp), allocatable :: C(:)
    real(dp), allocatable :: D(:)
end type

contains

subroutine find_init_states(sys, u, y, x0)
type(state_space), intent(in) :: sys
real(dp), dimension(:), intent(in) :: u, y, x0


end subroutine find_init_states

subroutine sim_ss(sys, u, x0, response)
type(state_space), intent(in) :: sys
real(dp), dimension(:), intent(in) :: u, x0
real(dp), dimension(size(u)), intent(out) :: response

integer i, &
        y, &
        num_samp
real(dp)    x(size(sys%A, 1)), &
            A(size(sys%A, 1), size(sys%A, 2)), &
            B(size(sys%B)), &
            C(size(sys%C)), &
            D(size(sys%D))

num_samp = size(u)
x = 0.0_dp
response = 0.0_dp

A = sys%A
B = sys%B
C = sys%C
D = sys%D

! Simulate sys using input u
response(1) = dot_product(C, x0)
x = matmul(A, x0) + B*u(1)
do i = 2, num_samp

    ! Compute response
    response(i) = dot_product(C, x)

    ! Update states
    x = matmul(A, x) + B*u(i)

end do

end subroutine

subroutine ss(num, den, sys)
real(dp), intent(in) :: num(:), den(:)

integer i, num_coeffs, den_coeffs
type(state_space), intent(out) :: sys
allocate(sys%A(size(den)-1, size(den)-1), &
         sys%B(size(den)-1), &
         sys%C(size(den)-1), &
         sys%D(1))

! Initialize local variables
num_coeffs = size(num)
den_coeffs = size(den)-1

sys%A = 0.0_dp
sys%A(1, :) = -den(2:)
do i = 2, den_coeffs
    sys%A(i, i-1) = 1.0_dp
end do

! TODO:This is incorrect 
sys%B = 0.0_dp
sys%B(1) = 1.0_dp

! TODO:This is incorrect 
sys%C = 0.0_dp
sys%C = num

sys%D = 0.0_dp

end subroutine ss

subroutine print_ss(sys)
type(state_space), intent(in) :: sys

write(*,*) "A:"
call print_matrix(sys%A)
write(*,*)

write(*,*) "B:"
call print_array(sys%B)
write(*,*)

write(*,*) "C:"
call print_array(sys%C)
write(*,*)

write(*,*) "D:"
call print_array(sys%D)

end subroutine print_ss

subroutine arx(y, u, na, nb, sys, error, n_samp)

integer, intent(in) :: na, nb, n_samp 
real(dp), intent(in) :: y(n_samp), u(n_samp)
type(state_space), intent(inout) :: sys
integer, intent(inout) :: error
real(dp)    y_ident(n_samp-max(na, nb)), &
            y_residuals(n_samp-max(na, nb)), &
            PHI(n_samp-max(na, nb), na+nb), &
            coeff(na+nb), &
            num(nb), &
            den(na+1)
integer i, max_nanb, n_ident_samp

if (na < 0) then
    error = 1
    return
end if

if (nb < 1) then
    error = 2
    return
end if

max_nanb = max(na, nb)
n_ident_samp = n_samp-max_nanb

! Fill PHI array
do i = 1, na
    PHI(:, i) = -y(max_nanb+1-i:n_samp-i)
end do

do i = 1, nb
    PHI(:, na+i) = u(max_nanb+1-i:n_samp-i)
end do

write(*,*) "PHI:"
call print_matrix(PHI)

! Fill Y array
y_ident = y(max_nanb+1:n_samp)

! Solve for numerator and denominator
! coefficients using least squares
call least_squares(PHI, y_ident, coeff)

write(*,*) "coeff:"
call print_array(coeff)

!write(*,*) "y_ident:"
!call print_array(y_ident)

!write(*,*) "PHI * coeff:"
!call print_array(matmul(PHI, coeff))

!write(*,*) "Least squares residuals:"
y_residuals = y_ident - matmul(PHI, coeff)
!call print_array(y_residuals)

write(*,*) "Max error:"
write(*,*) maxval(abs(y_residuals))

! Extract numerator and denominator polynomials coefficients
den(1) = 1.0_dp
! The minus sign should be removed when ss subroutine if fixed
den(2:na+1) = coeff(1:na)
num(:) = coeff(na+1:)

call ss(num, den, sys)

end subroutine

function check_n(n) result(error)
integer n, error

error = 0
if (n < 0) then
    error = 1
end if
end function
end module control
