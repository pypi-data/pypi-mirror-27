class Fun(object):
    def __init__(self, function):
        self.id = None
        self.bus_id = None
        self.pin = None

        self.function = function

    def __str__(self):
        return self.function

    def __repr__(self):
        return 'fn %s' % self.function

class BusFun(Fun):
    def __init__(self, bus, function):
        super().__init__(function)

        self.bus = bus

    def __str__(self):
        return '%s %s' % (self.bus, self.function)

    def __repr__(self):
        return 'busfn %s %s' % (self.bus, self.function)

class Pin(object):
    def __init__(self, name, *funs, **kwargs):
        self.id = None
        self.device = None
        self.name = name
        self.funs = []

        if len(funs) == 0:
            self.add_fun(Fun(self.name))
        else:
            for fun in funs:
                self.add_fun(fun)

        self.optional = True
        if 'optional' in kwargs:
            self.optional = kwargs['optional']

        self.description = ''
        if 'description' in kwargs:
            self.description = kwargs['description']

    def has_function(self, function):
        for fun in self.funs:
            if fun.function == function:
                return True
        return False

    def add_fun(self, fun):
        assert not self.has_function(fun.function)
        self.funs.append(fun)

    def __str__(self):
        return self.name

    def __repr__(self):
        '''Return a string "Pin (Functions)".'''

        text = '%s(%s)' % (self.__class__.__name__, self.name)
        return '%-15s (%s)' % (text, ' | '.join([str(fun) for fun in self.funs]))


class Component(object):
    components = []

    def __init__(self, name, description, *pins):
        Component.components.append(self)

        self.name = name
        self.description = description

        self.pins = []
        self.funs = []
        self.busses = []
        self._functions = set()

        for pin in pins:
            self.add_pin(pin)

        # Check that there is no Fun named like a BusFun
        # and no BusFun named like a Fun
        for function in self._functions:
            iterator = self.funs_by_function(function)
            ty = type(next(iterator))
            for fun in iterator:
                assert type(fun) == ty

    def add_pin(self, pin):
        assert self.pin_by_name(pin.name) is None

        pin.id = len(self.pins)
        pin.component = self
        self.pins.append(pin)

        for fun in pin.funs:
            fun.id = len(self.funs)
            fun.pin = pin
            self.funs.append(fun)
            self._functions.add(fun.function)

            # Assign bus_id
            if isinstance(fun, BusFun):
                for i, bus in enumerate(self.busses):
                    if fun.bus == bus:
                        fun.bus_id = i
                        break
                else:
                    fun.bus_id = len(self.busses)
                    self.busses.append(fun.bus)
            else:
                # make sure bus_id is unique and smaller zero
                fun.bus_id = -fun.id - 1

    def has_function(self, function):
        return function in self._functions

    def is_busfun(self, function):
        return isinstance(next(self.funs_by_function(function)), BusFun)

    def funs_by_function(self, function):
        for fun in self.funs:
            if fun.function == function:
                yield fun

    def pin_by_name(self, name):
        for pin in self.pins:
            if pin.name == name:
                return pin

    def __str__(self):
        '''Return the name of the component.'''

        return self.name

    def __repr__(self):
        component = '%s\n' % self.name
        for pin in self.pins:
            component += '  ' + repr(pin) + '\n'
        return component

    @classmethod
    def component_by_name(cls, name):
        '''Returns the Component called `name` from registered components.'''

        for c in cls.components:
            if c.name == name:
                return c

        raise IndexError('No Component with name ' + name)

    @classmethod
    def register_component(cls, component):
        '''Register a Component.'''

        try:
            cls.component_by_name(component.name)
            raise Exception('Component with name %s exists' % component.name)
        except IndexError:
            cls.components.append(component)


class Io(Pin):
    '''Single function bidirectional signal pin.'''

    def __init__(self, name, *funs, **kwargs):
        super().__init__(name, *funs, **kwargs)

class Pwr(Io):
    '''Single function bidirectional power pin.'''

    def __init__(self, name, *funs, **kwargs):
        super().__init__(name, *funs, **kwargs)

class In(Pin):
    '''Single function input signal pin.'''

    def __init__(self, name, *funs, **kwargs):
        super().__init__(name, *funs, **kwargs)

class PwrIn(In):
    '''Single function input power pin.'''

    def __init__(self, name, *funs, **kwargs):
        super().__init__(name, *funs, **kwargs)

class Out(Pin):
    '''Single function output signal pin.'''

    def __init__(self, name, *funs, **kwargs):
        super().__init__(name, *funs, **kwargs)

class PwrOut(Out):
    '''Single function output power pin.'''

    def __init__(self, name, *funs, **kwargs):
        super().__init__(name, *funs, **kwargs)
