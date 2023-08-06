import math
from decimal import Decimal
from fractions import Fraction

def fexp(number):
    (sign, digits, exponent) = Decimal(number).as_tuple()
    return len(digits) + exponent - 1

def fman(number):
    return Decimal(number).scaleb(-fexp(number)).normalize()

def frac_approx(x,max_denom):
    frac = Fraction(x).limit_denominator(max_denom)
    return frac.numerator,frac.denominator

def format_output(result,mode):
    mant = fman(result)
    expo = fexp(result)
    if mode == "sci":
        return "%f*10^%i"%(mant,expo)
    if mode == "eng":
        ecor = expo%3
        return "%f*10^%i"%(10**ecor*mant,expo-ecor)
    if mode == "auto":
        return str(result)
    if mode == "dec":
        return "not supported"
    if mode == "frac":
        return "%i/%i"%frac_approx(result,10000)

