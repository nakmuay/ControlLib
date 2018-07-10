module math
use types, only : dp

implicit none
private
public  print_array, &
        print_matrix, &
        inv, &
        least_squares

contains

subroutine print_array(x)
real(dp), intent(in) :: x(:)
integer i

do i = 1, size(x)
    print *, x(i)
end do
end subroutine

subroutine print_matrix(m)
real(dp), intent(in) :: m(:, :)
integer i

do i = 1, size(m, 1)
    write(*,*) m(i, :)
end do
end subroutine

function inv(A) result(Ainv)
  real(dp), dimension(:,:), intent(in) :: A
  real(dp), dimension(size(A,1),size(A,2)) :: Ainv

  real(dp), dimension(size(A,1)) :: work  ! work array for LAPACK
  integer, dimension(size(A,1)) :: ipiv   ! pivot indices
  integer :: n, info

  ! External procedures defined in LAPACK
  external DGETRF
  external DGETRI

  ! Store A in Ainv to prevent it from being overwritten by LAPACK
  Ainv = A
  n = size(A,1)

  ! DGETRF computes an LU factorization of a general M-by-N matrix A
  ! using partial pivoting with row interchanges.
  call DGETRF(n, n, Ainv, n, ipiv, info)

  if (info /= 0) then
     stop 'Matrix is numerically singular!'
  end if

  ! DGETRI computes the inverse of a matrix using the LU factorization
  ! computed by DGETRF.
  call DGETRI(n, Ainv, n, ipiv, work, n, info)

  if (info /= 0) then
     stop 'Matrix inversion failed!'
  end if
end function inv

subroutine least_squares(A, Y, x)
real(dp), intent(in) :: A(:, :), Y(size(A, 1))
real(dp), intent(inout) :: x(size(A, 1))
real(dp)    At(size(A, 2), size(A, 1)), &
            AtA(size(A, 2), size(A, 2)), &
            AtAinv(size(A, 2), size(A, 2)), &
            AtAinvAt(size(A, 2), size(A, 1))

At = transpose(A)
AtA = matmul(At, A)
AtAinv = inv(AtA)
x = matmul(matmul(AtAinv, At), Y)
end subroutine least_squares

end module math
