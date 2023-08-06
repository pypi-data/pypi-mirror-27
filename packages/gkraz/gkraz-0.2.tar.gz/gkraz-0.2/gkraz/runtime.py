import numpy as np
from pint import UnitRegistry

from .bytecode import *
from .functions import FUNCS,CONSTS

class BcEnvironment:
    def __init__(self):
        self.globs = {}
        self.num = 1
        self.ureg = UnitRegistry()

    def get_num(self):
        return self.num

    def inc_num(self):
        self.num += 1

    def add_func(self,name,params,bc):
        def newfunc(*args):
            if len(args) != len(params):
                raise TypeError("%s() takes %i positional argument but %s were given"%
                        (name,len(params),len(args)))
            locals = { param: arg for param,arg in zip(params,args) }
            return self.run_bc(bc,locals)
        self.globs[name] = newfunc

    def add_var(self,name,bc):
        self.globs[name] = self.run_bc(bc)

    def run_expr(self,bc):
        return self.run_bc(bc)

    def run_bc(self,bc,locals={}):
        stack = []
        storage = {}

        def get_var(name,var):
            if name in locals:
                return locals[name]
            if name in self.globs:
                return self.globs[name]
            if name in FUNCS:
                return FUNCS[name]
            if name in CONSTS:
                return CONSTS[name]
            raise NameError("%s %s not defined"%("Variable" if var else "Function",name))

        def o_add(opargs):
            stack.append(stack.pop()+stack.pop())
        def o_sub(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2-s1)
        def o_mul(opargs):
            stack.append(stack.pop()*stack.pop())
        def o_div(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2/s1)
        def o_mod(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2%s1)
        def o_and(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s1 and s2)
        def o_or(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s1 or s2)
        def o_not(opargs):
            stack.append(not stack.pop())
        def o_neg(opargs):
            stack.append(-stack.pop())
        def o_eq(opargs):
            stack.append(stack.pop()==stack.pop())
        def o_neq(opargs):
            stack.append(stack.pop()!=stack.pop())
        def o_gt(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2>s1)
        def o_gte(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2>=s1)
        def o_lt(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2<s1)
        def o_lte(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2<=s1)
        def o_pow(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2**s1)
        def o_fun(opargs):
            args = stack[-opargs[1] or None:]
            del stack[-opargs[1] or None:]
            stack.append(get_var(opargs[0],False)(*args))
        def o_var(opargs):
            stack.append(get_var(opargs[0],True))
        def o_lit(opargs):
            stack.append(opargs[0])
        def o_vec(opargs):
            vec = np.array(stack[-opargs[0] or None:])
            del stack[-opargs[0] or None:]
            stack.append(vec)
        def o_sto(opargs):
            storage[opargs[0]] = stack.pop()
        def o_ld(opargs):
            stack.append(storage[opargs[0]])
        def o_dot(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2 @ s1)
        def o_uni(opargs):
            stack.append(self.ureg.parse_expression(opargs[0]))
        def o_to(opargs):
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s2.to(s1))

        odict = {
            OpCo.ADD: o_add,
            OpCo.SUB: o_sub,
            OpCo.MUL: o_mul,
            OpCo.DIV: o_div,
            OpCo.MOD: o_mod,
            OpCo.AND: o_and,
            OpCo.OR : o_or ,
            OpCo.NOT: o_not,
            OpCo.NEG: o_neg,
            OpCo.EQ : o_eq ,
            OpCo.NEQ: o_neq,
            OpCo.GT : o_gt ,
            OpCo.GTE: o_gte,
            OpCo.LT : o_lt ,
            OpCo.LTE: o_lte,
            OpCo.POW: o_pow,
            OpCo.FUN: o_fun,
            OpCo.VAR: o_var,
            OpCo.LIT: o_lit,
            OpCo.VEC: o_vec,
            OpCo.STO: o_sto,
            OpCo.LD : o_ld ,
            OpCo.DOT: o_dot,
            OpCo.UNI: o_uni,
            OpCo.TO : o_to
        }
        for op in bc:
            odict[op.opcode](op.args)
        self.globs["_%i"%self.num] = stack[0]
        if "__" in self.globs: self.globs["___"] = self.globs["__"]
        if "_" in self.globs: self.globs["__"] = self.globs["_"]
        self.globs["_"] = stack[0]
        return stack[0]
