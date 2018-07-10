module control
use types
use math
implicit none

private
public arx

contains

subroutine arx(y, u, na, nb, sys, error, n_samp)
integer, intent(in) :: na, nb, n_samp 
real(dp), intent(in) :: y(n_samp), u(n_samp)
real(dp), intent(inout) :: sys(na+nb)
integer, intent(inout) :: error
real(dp)    y_ident(n_samp-max(na, nb)), &
            PHI(n_samp-max(na, nb), na+nb), &
            PHItrans(na+nb, n_samp-max(na, nb)), &
            PHItransPHI(na+nb, na+nb)
integer i, max_nanb, n_ident_samp

if (na .lt. 0) then
    error = 1
    return
end if

if (nb .lt. 1) then
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
write (*,*) "PHI: "
call print_matrix(PHI)
write (*,*)

! Fill Y array
y_ident = y(max_nanb+1:n_samp)
write(*,*) "y_ident: "
call print_array(y_ident)
write (*,*)

! Solve for numerator and denominator
! coefficients using least squares
call least_squares(PHI, y_ident, sys)

end subroutine

function check_n(n) result(error)
integer n, error

error = 0
if (n < 0) then
    error = 1
end if
end function
end module control
