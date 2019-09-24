from __future__ import print_function

try:
    from scipy import optimize
except ImportError:
    import sys
    print("Missing scipy, using secant method", file=sys.stderr)
    optimize = None



def secant_method(f, x0, tol=0.0001):
    """
    Solve for x where f(x)=0, given starting x0 and tolerance.

    Arguments
    ----------
    f  : a function of a single variable
    x0 : a starting value of x to begin the solver
    tol: tolerance as percentage of final result. If two subsequent x values
         are within tol percent, the function will return.

    Return
    -------
    * a single value which is x

    Notes
    ------
    The secant method for finding the zero value of a function uses the
    following formula to find subsequent values of x.

    x(n+1) = x(n) - f(x(n))*(x(n)-x(n-1))/(f(x(n))-f(x(n-1)))

    Warning
    --------
    This implementation is simple and does not handle cases where there is no
    solution. Those requiring a more robust version should use optimize.newton
    from the scipy module.
    """

    x1 = x0 * 1.1
    while (abs(x1 - x0) / abs(x1) > tol):
        x0, x1 = x1, x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
    return x1


def xnpv(rate, cashflows):
    """
    Calculate the Net Present Value of a series of cashflows, possibly at
    irregular intervals.

    Arguments
    ---------
    * rate     : the discount rate to be applied to the cash flows
    * cashflows: a list in which each element is a tuple of the form (date,
      amount), where date is a python datetime.date object and amount is an
      integer or floating point number. Cash outflows (investments) are
      represented with negative amounts, and cash inflows (returns) as
      positive amounts.

    Return
    ------
    * a single value which is the NPV of the given cash flows.

    Notes
    ---------------
    * Equivalent to the Microsoft Excel function of the same name.
    * Net Present Value is the sum of each of the cash flows discounted back to
      the date of the first cash flow. The discounted value of a given cash
      flow is A/(1+r)**(t-t0), where A is the amount, r is the discount rate,
      and (t-t0) is the time in years from the date of the first cash flow in
      the series (t0) to the date of the cash flow being added to the sum (t).
    """

    chron_order = sorted(cashflows, key=lambda x: x[0])
    t0 = chron_order[0][0]  # t0 is the date of the first cash flow

    return sum(cf / (1 + rate) ** ((t - t0).days / 365.0) for (t, cf) in chron_order)


def xirr(cashflows, guess=0.1):
    """
    Calculate the Internal Rate of Return of a series of cashflows, possibly at
    irregular intervals.

    Arguments
    ---------
    * cashflows: a list in which each element is a tuple of the form (date,
      amount), where date is a python datetime.date object and amount is an
      integer or floating point number. Cash outflows (investments) are
      represented with negative amounts, and cash inflows (returns) as
      positive amounts.
    * guess (optional, default = 0.1): a guess at the solution to be used as
      a starting point for the numerical solution.

    Return
    ------
    * a single value which is the IRR

    Notes
    ----------------
    * Equivalent to the Microsoft Excel function of the same name.
    * Internal Rate of Return (IRR) is the discount rate at which the Net
      Present Value (NPV) of a series of cash flows is equal to zero. The NPV
      of the series of cash flows is determined using the xnpv function in this
      module. The discount rate at which NPV equals zero is found using the
      secant method of numerical solution.
    * For users that do not have the scipy module installed, there is an
      alternate version that uses the secant_method function defined in this
      module rather than the scipy.optimize module's numerical solver (newton).
      Both use the same method of calculation so there should be no difference
      in result. scipy.optimize.newton is preferred as the secant_method does
      not fail gracefully in cases where there is no solution.
    """

    return method(lambda r: xnpv(r, cashflows), guess)


method = optimize.newton if optimize else secant_method
