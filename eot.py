import numpy as np
from math import pi, radians, pow, sin, asin, cos

# Sources of formulas:
# [1]   Position of the Sun
#           https://en.wikipedia.org/wiki/Position_of_the_Sun
#           Declination of the Sun as seen from Earth
#           Calculations, 3rd "more accurate" formula
#
# [2]   EQUATION OF TIME — PROBLEM IN ASTRONOMY
#           M. Müller
#           Gymnasium Münchenstein Grellingerstrasse 5,
#           4142 Münchenstein, Switzerland


# equation of time, based on source [2]
# inputs:
#   e               earth orbit eccentricity (0.01671)
#   p_degs          projection of the axis of the earth onto the plane of the orbit in degrees (12.25)
#   axis_norm_degs  angle between the earth's axis and the norm of the orbit in degrees (23.4367)
#   peri_day        calendar day in January of perihelion in decimal/fractional format (~3-5)
#   orb_per         earth orbital period (365.25696)
#   day_start       day of year to start calculation
#   day_end         day of year to end calculation
# outputs:
#   days           integer list of days based on start and end dates input
#   mins           equation of time list in minutes
def eot_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, day_start, day_end):
    mins = []
    days = np.arange(day_start, (day_end+1))

    p = radians(p_degs)
    axis_norm_rads = radians(axis_norm_degs)
    t1 = (axis_norm_rads/2)*(1-4*pow(e, 2))
    tan2_1_4e2 = (1-cos(2*t1)) / (1+cos(2*t1))
    tan2 = (1-cos(axis_norm_rads)) / (1+cos(axis_norm_rads))
    e2 = 2*e
    tan2_2e = 2*e*tan2
    tan4_1_2 = (1/2)*pow(tan2, 2)
    e2_5_4 = (5/4)*(pow(e, 2))
    tan4_2e = 2*e*pow(tan2, 2)
    tan2_2e_13_4 = (13/4)*(pow(e, 2))*tan2
    tan6_1_3 = (1/3)*pow(tan2, 2)*tan2

    time_mins = (24 * 60) / (2 * pi)

    for d in days:

        d_offset = d + 0.5 - peri_day

        m = 2*pi*(d_offset/orb_per)

        mins.append(-(tan2_1_4e2*sin(2*(m+p))+e2*sin(m) -
                    tan2_2e*sin(m+2*p)+tan2_2e*sin(3*m+2*p) +
                    tan4_1_2*sin(4*(m+p))+e2_5_4*sin(2*m)-tan4_2e*sin((3*m)+(4*p)) +
                    tan4_2e*sin((5*m)+(4*p))+tan2_2e_13_4*sin(4*m+2*p) +
                    tan6_1_3*sin(6*(m+p)))*time_mins)
    return days, mins


# Eccentricity part of Equation of Time, based on source [2]
# this is a convenience function where axis_norm_rads is set to 0
def ecc_gen(e, p, peri_day, orb_per, day_start, day_end):
    return eot_gen(e, p, 0, peri_day, orb_per, day_start, day_end)


# Obliquity part of Equation of Time, based on source [2]
# this is a convenience function where e is set to 0
def obl_gen(p, axis_norm_rads, peri_day, orb_per, day_start, day_end):
    return eot_gen(0, p, axis_norm_rads, peri_day, orb_per, day_start, day_end)


# Sun's declination, based on source [1]
# inputs:
#   e               earth orbit eccentricity (0.01671)
#   axis_norm_degs  angle between the earth's axis and the norm of the orbit in degrees (23.4367)
#   orb_per         earth orbital period (365.25696)
#   day_start       day of year to start calculation
#   day_end         day of year to end calculation
# outputs:
#   days           integer list of days based on start and end dates input
#   decs           declination list in degrees
def dec_gen(e, axis_norm_degs, orb_per, day_start, day_end):
    decs = []
    days = np.arange(day_start, (day_end+1))

    for d in days:
        d_offset = d - 0.5
        sin_axis_norm = sin(radians(axis_norm_degs))
        ratio360 = 360/orb_per
        ratio_pi_e = (360/pi)*e

        decs.append(-(asin(sin_axis_norm *
                           cos(radians(ratio360*(d_offset+10) +
                               ratio_pi_e*sin(radians(ratio360*(d_offset-2))))))*360/(2*pi)))

    return days, decs


# Analemma Data
# inputs:
#   e               earth orbit eccentricity (0.01671)
#   p_degs          projection of the axis of the earth onto the plane of the orbit in degrees (12.25)
#   axis_norm_degs  angle between the earth's axis and the norm of the orbit in degrees (23.4367)
#   peri_day        calendar day in January of perihelion in decimal/fractional format (~3-5)
#   orb_per         earth orbital period (365.25696)
# outputs:
#   days           integer list of days
#   decs           declination list in degrees
#   mins           equation of time list in minutes
def analemma_gen(e, p_degs, axis_norm_degs, peri_day, orb_per):
    days, decs = dec_gen(e, axis_norm_degs, orb_per, 1, 366)
    _, mins = eot_gen(e, p_degs, axis_norm_degs, peri_day, orb_per, 1, 366)
    return days, decs, mins

