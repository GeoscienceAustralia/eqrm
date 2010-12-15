#!/usr/bin/env python

"""A simplistic implementation of Campbell03.

Should be as different from code in ground_motion_interface.py
as possible.
"""

import math


# # Cambbell 2003 table 6
# # c1      c2      c3       c4      c5       c6        c7     c8     c9      c10    c11     c12     c13
# [ 0.0305, 0.633, -0.0427, -1.591, -0.00428, 0.000483, 0.683, 0.416, 1.140, -0.873, 1.030, -0.0860, 0.414] # PGA
# [ 0.0305, 0.633, -0.0427, -1.591, -0.00428, 0.000483, 0.683, 0.416, 1.140, -0.873, 1.030, -0.0860, 0.414] # 0.01
# [ 1.3535, 0.630, -0.0404, -1.787, -0.00388, 0.000497, 1.020, 0.363, 0.851, -0.715, 1.030, -0.0860, 0.414] # 0.02
# [ 1.1860, 0.622, -0.0362, -1.691, -0.00367, 0.000501, 0.922, 0.376, 0.759, -0.922, 1.030, -0.0860, 0.414] # 0.03
# [ 0.3736, 0.616, -0.0353, -1.469, -0.00378, 0.000500, 0.630, 0.423, 0.771, -1.239, 1.042, -0.0838, 0.443] # 0.05
# [-0.0395, 0.615, -0.0353, -1.383, -0.00421, 0.000486, 0.491, 0.463, 0.955, -1.349, 1.052, -0.0838, 0.453] # 0.075
# [-0.1475, 0.613, -0.0353, -1.369, -0.00454, 0.000460, 0.484, 0.467, 1.096, -1.284, 1.059, -0.0838, 0.460] # 0.10
# [-0.1901, 0.616, -0.0478, -1.368, -0.00473, 0.000393, 0.461, 0.478, 1.239, -1.079, 1.068, -0.0838, 0.469] # 0.15
# [-0.4328, 0.617, -0.0586, -1.320, -0.00460, 0.000337, 0.399, 0.493, 1.250, -0.928, 1.077, -0.0838, 0.478] # 0.20
# [-0.6906, 0.609, -0.0786, -1.280, -0.00414, 0.000263, 0.349, 0.502, 1.241, -0.753, 1.081, -0.0838, 0.482] # 0.30
# [-0.5907, 0.534, -0.1379, -1.216, -0.00341, 0.000194, 0.318, 0.503, 1.166, -0.606, 1.098, -0.0824, 0.508] # 0.50
# [-0.5429, 0.480, -0.1806, -1.184, -0.00288, 0.000160, 0.304, 0.504, 1.110, -0.526, 1.105, -0.0806, 0.528] # 0.75
# [-0.6104, 0.451, -0.2090, -1.158, -0.00255, 0.000141, 0.299, 0.503, 1.067, -0.482, 1.110, -0.0793, 0.543] # 1.0
# [-0.9666, 0.441, -0.2405, -1.135, -0.00213, 0.000119, 0.304, 0.500, 1.029, -0.438, 1.099, -0.0771, 0.547] # 1.5
# [-1.4306, 0.459, -0.2552, -1.124, -0.00187, 0.000103, 0.310, 0.499, 1.015, -0.417, 1.093, -0.0758, 0.551] # 2.0
# [-2.2331, 0.492, -0.2646, -1.121, -0.00154, 0.000084, 0.310, 0.499, 1.014, -0.393, 1.090, -0.0737, 0.562] # 3.0
# [-2.7975, 0.507, -0.2738, -1.119, -0.00135, 0.000074, 0.294, 0.506, 1.018, -0.386, 1.092, -0.0722, 0.575] # 4.0

######
# Globals
######

R1 = 70.0
R2 = 130.0

M1 = 7.16

Tolerance = 0.10

######
# The Campbell equation(s)
######

def eqn_31(Mw, table6_coeffs):
    # unpack table6 coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13) = table6_coeffs

    return C2*Mw + C3*(8.5-Mw)*(8.5-Mw)

def eqn_32(Mw, R, Rrup, table6_coeffs):
    # unpack table6 coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13) = table6_coeffs

    return C4*math.log(R) + (C5 + C6*Mw)*Rrup

def eqn_33(Mw, Rrup, table6_coeffs):
    # unpack table6 coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13) = table6_coeffs

    tmp = C7*math.exp(C8*Mw)

    return math.sqrt(Rrup*Rrup + tmp*tmp)

def eqn_34(Rrup, table6_coeffs):
    # unpack table6 coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13) = table6_coeffs

    if Rrup <= R1:
        return 0.0

    if R1 < Rrup <= R2:
        return C9*(math.log(Rrup) - math.log(R1))

    return C9*(math.log(Rrup) - math.log(R1)) + C10*(math.log(Rrup) - math.log(R2))

def eqn_35(Mw, table6_coeffs):
    # unpack table6 coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13) = table6_coeffs

    if Mw < M1:
        return C11 + C12*Mw

    return C13

def eqn_30(Mw, Rrup, table6_coeffs):
    # unpack table6 coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13) = table6_coeffs

    R = eqn_33(Mw, Rrup, table6_coeffs)
    lnY = (C1 + eqn_31(Mw, table6_coeffs) + eqn_32(Mw, R, Rrup, table6_coeffs) + 
           eqn_34(Rrup, table6_coeffs))

    return lnY

######
# handle doing one estimate
######

def estimate(period, Mw, Rrup, table6_coeffs, expected):
    lnY = eqn_30(Mw, Rrup, table6_coeffs)
    g = math.exp(lnY)
    tol = abs(g-expected)/max(g, expected)
    flag = ' ' if tol <= Tolerance else '*'
    sigma = eqn_35(Mw, table6_coeffs)
    print('period=%.2f, Rrup=%6.1f, M=%.1f, lnY=%7.4f, sigma=%7.4f\tg=%8.5f, expected=%7.4f, tol=%.2f%s'
          % (period, Rrup, Mw, lnY, sigma, g, expected, tol, flag))

######
# Handle various cases
######

print('Campbell03 model')
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)

# period = 0.01, M=5.0
period = 0.01
M = 5.0
table6_coeffs = [ 0.0305, 0.633, -0.0427, -1.591, -0.00428, 0.000483, 0.683, 0.416, 1.140, -0.873, 1.030, -0.0860, 0.414] # PGA

Rrup = 1.0
expected = 8.7e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 3.3e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 1.2e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 1.2e-4
estimate(period, M, Rrup, table6_coeffs, expected)

print('-' * 102)

M = 7.0

Rrup = 1.0
expected = 1.5e+0
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 8.5e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 7.0e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 2.0e-3
estimate(period, M, Rrup, table6_coeffs, expected)


print('=' * 102)

# period = 0.2, M=5.0
period = 0.2
M = 5.0
table6_coeffs = [-0.4328, 0.617, -0.0586, -1.320, -0.00460, 0.000337, 0.399, 0.493, 1.250, -0.928, 1.077, -0.0838, 0.478] # 0.20

Rrup = 1.0
expected = 8.0e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 3.0e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 1.8e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 1.7e-4
estimate(period, M, Rrup, table6_coeffs, expected)

print('-' * 102)

M = 7.0

Rrup = 1.0
expected = 1.7e+0
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 1.0e+0
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 1.1e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 2.0e-3
estimate(period, M, Rrup, table6_coeffs, expected)


print('=' * 102)

# period = 1.0, M=5.0
period = 1.0
M = 5.0
table6_coeffs = [-0.6104, 0.451, -0.2090, -1.158, -0.00255, 0.000141, 0.299, 0.503, 1.067, -0.482, 1.110, -0.0793, 0.543] # 1.0

Rrup = 1.0
expected = 8.0e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 2.2e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 2.0e-3
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 1.3e-4
estimate(period, M, Rrup, table6_coeffs, expected)

print('-' * 102)

M = 7.0

Rrup = 1.0
expected = 6.0e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 3.1e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 4.5e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 3.3e-3
estimate(period, M, Rrup, table6_coeffs, expected)


print('=' * 102)

# period = 3.0, M=5.0
period = 3.0
M = 5.0
table6_coeffs = [-2.2331, 0.492, -0.2646, -1.121, -0.00154, 0.000084, 0.310, 0.499, 1.014, -0.393, 1.090, -0.0737, 0.562] # 3.0

Rrup = 1.0
expected = 1.0e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 4.0e-3
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 3.3e-4
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 4.3e-5
estimate(period, M, Rrup, table6_coeffs, expected)

print('-' * 102)

M = 7.0

Rrup = 1.0
expected = 1.3e-1
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 10.0
expected = 9.0e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 100.0
expected = 1.3e-2
estimate(period, M, Rrup, table6_coeffs, expected)

Rrup = 1000.0
expected = 2.0e-3
estimate(period, M, Rrup, table6_coeffs, expected)


