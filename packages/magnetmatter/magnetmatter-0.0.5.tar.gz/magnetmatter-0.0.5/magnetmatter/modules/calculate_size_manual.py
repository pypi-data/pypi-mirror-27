import math

wavelength = 2.459151
""" Y cos """
Y =0.14354958E-01
sigma_Y =0.11723353E-03
""" lor size """
Sz = 0
sigma_Sz = 0

""" calculating the ab/c sizes. """
Y_degree = Y
Y_AA = Y_degree * math.pi**2 / 180 / 2 / wavelength * 1000
sigma_Y = sigma_Y * math.pi ** 2 / 180 / 2 / wavelength * 1000

absize = 100 / Y_AA
sigma_absize = 100 * (sigma_Y ** 2 / Y_AA ** 4) ** 0.5
csize = 100 / (Y_AA + Sz)
sigma_csize = 100 * ((sigma_Y ** 2 + sigma_Sz ** 2) / (Y_AA + Sz) ** 4) ** 0.5
""" prepare dictionary """
tmp_dict = {"ab-size": (absize, sigma_absize), "c-size": (csize, sigma_csize)}
print(tmp_dict)
"""


Extracted from Anna's Excel Sheet. Do not change!

Y[°]	from .out as "Y-cos_ph1_pat1"
σ_Y[°]	from .out error for above

S_z[Å^-1]	from .out as "L-Size_ph1_pat1"
σ_sz[Å^-1]	from .out error for above.

Y[Å^-1] = Y[°] * PI^2 / 180 / 2 / wavelength[Å] * 1000
σ_Y[Å^-1] = σ_Y[°] * PI^2 / 180 / 2 / wavelength * 1000

# ab size
a,b-size[nm] = 100 / Y[Å^-1]
σ_a,b-size[nm] = 100 * (σ_Y[Å^-1]^2 / Y[Å^-1]^4)^0.5

# c size
c-size[nm] = 100 / (Y[Å^-1] + S_Z[Å^-1])
σ_c-size[nm] = =100 * ((σ_Y[Å^-1]^2 + σ_sz[Å^-1]^2) / (Y[Å^-1] + S_z[Å^-1])^4)^0.5
"""
