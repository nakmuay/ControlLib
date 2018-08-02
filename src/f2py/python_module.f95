module python_module
use types, only : dp

contains

subroutine array_multiply(arr, factor, res, n)
real(dp), intent(in) :: arr(n), factor
real(dp), intent(out) :: res(n)

res = arr * factor

end subroutine array_multiply

end module python_module
