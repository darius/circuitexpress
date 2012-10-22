class Constant:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return repr(self.value)

class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
    def __repr__(self):
        return self.name

class Mux:
    def __init__(self, select, *choices):
        self.select = select
        self.choices = choices
    def __repr__(self):
        return ('Mux(%r, %s)'
                % (self.select,
                   ', '.join(map(repr, self.choices))))

def realize(f, inputs):
    "Return a circuit which outputs the value of f on the given input variables."
    def extend(vs, env):
        if not vs:
            return Constant(f(env))
        else:
            v, vs = vs[0], vs[1:]
            return Mux(v, *[extend(vs, extended(env, v, value))
                            for value in v.domain])
    return extend(inputs, {})

def extended(env, variable, value):
    result = dict(env)
    result[variable] = value
    return result

x = Variable('x', (0, 1))
y = Variable('y', (0, 1))

## realize(lambda env: env[x], [x, y])
#. Mux(x, Mux(y, 0, 0), Mux(y, 1, 1))
