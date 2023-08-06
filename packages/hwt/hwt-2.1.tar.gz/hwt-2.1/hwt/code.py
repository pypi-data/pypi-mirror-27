import math
from operator import and_, or_, xor, add

from hwt.hdl.operatorDefs import concatFn
from hwt.hdl.typeShortcuts import hInt, vec
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.typeCast import toHVal
from hwt.pyUtils.arrayQuery import arr_any, flatten
from hwt.synthesizer.andReducedContainer import AndReducedContainer
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.walkers import \
    discoverEventDependency
from hwt.synthesizer.vectorUtils import fitTo


def _intfToSig(obj):
    if isinstance(obj, InterfaceBase):
        return obj._sig
    else:
        return obj


class StmCntx(list):
    "Base class of statement contexts"


class If(StmCntx):
    """
    If statement generator

    :ivar nowIsEventDependent: flag if current scope of if is event dependent
        (is used to mark statements as event dependent)
    """

    def __init__(self, cond, *statements):
        """
        :param cond: condition in if statement
        :param statements: list of statements which should be active
            if condition is met
        """
        self.cond = _intfToSig(cond)
        assert isinstance(self.cond, RtlSignalBase)

        self.nowIsEventDependent = arr_any(discoverEventDependency(cond),
                                           lambda x: True)
        self.elifConds = []

        c = AndReducedContainer()
        c.add(self.cond)
        self._appendStatements(c, statements)

    def Else(self, *statements):
        ncond = AndReducedContainer()

        for ec in reversed(self.elifConds):
            ncond.add(~ec)
        ncond.add(~self.cond)

        self._appendStatements(ncond, statements)

        # convert self to StmCntx to prevent any other else/elif
        stml = StmCntx()
        stml.extend(self)
        return stml

    def _appendStatements(self, condSet, statements):
        """
        Append statements to this container under conditions specified
        by condSet
        """
        for stm in flatten(statements):
            stm.isEventDependent = (stm.isEventDependent
                                    or self.nowIsEventDependent)
            for c in condSet:
                c.endpoints.append(stm)
            stm.cond.update(condSet)
            self.append(stm)

    def Elif(self, cond, *statements):
        cond = _intfToSig(cond)
        self.nowIsEventDependent = (self.nowIsEventDependent or
                                    arr_any(discoverEventDependency(cond),
                                            lambda x: True))
        thisCond = AndReducedContainer()
        thisCond.add(cond)
        for c in reversed(self.elifConds):
            thisCond.add(~c)

        thisCond.add(~self.cond)
        self._appendStatements(thisCond, statements)
        self.elifConds.append(cond)

        return self


class Switch(StmCntx):
    """
    Switch statement generator
    """

    def __init__(self, switchOn):
        self.switchOn = switchOn
        self.cond = None

    _appendStatements = If._appendStatements

    def Case(self, caseVal, *statements):
        "c-like case of switch statement"
        cond = self.switchOn._eq(caseVal)
        if self.cond is None:
            If.__init__(self, cond, *statements)
        else:
            If.Elif(self, cond, *statements)

        return self

    def addCases(self, tupesValStmnts):
        """
        Add multiple case statements from iterable of tuleles (caseVal, statements)
        """
        s = self
        for val, statements in tupesValStmnts:
            s = s.Case(val, *statements)
        return s

    def Default(self, *statements):
        """c-like default of switch statement
        """
        if self.cond is None:
            # no cases were used
            return statements

        return If.Else(self, *statements)


def SwitchLogic(cases, default=None):
    """
    generate if tree for cases like

    ..code-block:: python
        if cond0:
            statements0
        elif cond1:
            statements1
        else:
            default

    :param case: iterable of tuples (condition, statements)
    :param default: default statements
    """
    if default is not None:
        assigTop = default
    else:
        assigTop = []

    for cond, statements in reversed(cases):
        assigTop = If(cond,
                      statements
                      ).Else(
            assigTop
        )

    return assigTop


def In(sigOrVal, iterable):
    """
    Hdl convertible in operator, check if any of items
    in "iterable" equals "sigOrVal"
    """
    res = None
    for i in iterable:
        i = toHVal(i)
        if res is None:
            res = sigOrVal._eq(i)
        else:
            res = res | sigOrVal._eq(i)

    assert res is not None, "Parameter iterable is empty"
    return res


def StaticForEach(parentUnit, items, bodyFn, name=""):
    """
    Generate for loop for static items

    :param parentUnit: unit where this code should be instantiated
    :param items: items which this "for" itering on
    :param bodyFn: function which fn(item, index) or fn(item)
        returns (statementList, ack).
        It's content is performed in every iteration.
        When ack is high loop will fall to next iteration
    """

    items = list(items)
    itemsCnt = len(items)
    if itemsCnt == 0:
        # if there are no items there is nothing to generate
        return []
    elif itemsCnt == 1:
        # if there is only one item do not generate counter logic generate
        return bodyFn(items[0], 0)
    else:
        # if there is multiple items we have to generate counter logic
        index = parentUnit._reg(name + "for_index",
                                Bits(log2ceil(itemsCnt + 1), signed=False),
                                defVal=0)
        ackSig = parentUnit._sig(name + "for_ack")

        statementLists = []
        for i, (statementList, ack) in [(i, bodyFn(item, i))
                                        for i, item in enumerate(items)]:
            statementLists.append(statementList + [(ackSig(ack)), ])

        If(ackSig,
           If(index._eq(itemsCnt - 1),
              index(0)
              ).Else(
               index(index + 1)
           )
        )

        return Switch(index)\
            .addCases(
            enumerate(statementLists)
        ).Default(
            bodyFn(items[0], 0)[0]
        )


class FsmBuilder(StmCntx):
    """
    :ivar stateReg: register with state
    """

    def __init__(self, parent, stateT, stateRegName="st"):
        """
        :param parent: parent unit where fsm should be builded
        :param stateT: enum type of state
        :param stateRegName: name of register where sate is stored
        """
        if isinstance(stateT, HEnum):
            beginVal = stateT.fromPy(stateT._allValues[0])
        else:
            beginVal = 0

        self.stateReg = parent._reg(stateRegName, stateT, beginVal)
        Switch.__init__(self, self.stateReg)

    _appendStatements = Switch._appendStatements

    def Trans(self, stateFrom, *condAndNextState):
        """
        :param stateFrom: apply when FSM is in this state
        :param condAndNextState: tupes (condition, newState),
            last does not to have condition

        :attention: transitions has priority, first has the biggest
        :attention: if stateFrom is None it is evaluated as default
        """
        top = None
        last = True

        for cAndS in reversed(condAndNextState):
            if last is True:
                last = False
                # if this is last trans. it does not have to condition
                try:
                    condition, newvalue = cAndS
                except TypeError:
                    top = c(cAndS, self.stateReg)
                    continue
                top = []

            else:
                condition, newvalue = cAndS

            # building decision tree
            top = If(condition,
                     self.stateReg(newvalue)
                     ).Else(
                top
            )

        s = Switch.Case(self, stateFrom, *top)
        return s

    def Default(self, *condAndNextState):
        d = self.Trans(None, *condAndNextState)
        d.stateReg = self.stateReg
        return d


def _connect(src, dst, exclude, fit):
    if isinstance(src, InterfaceBase):
        if isinstance(dst, InterfaceBase):
            return dst._connectTo(src, exclude=exclude, fit=fit)
        src = src._sig

    assert not exclude, "this intf. is just a signal"
    if src is None:
        src = dst._dtype.fromPy(None)
    else:
        src = toHVal(src)

    if fit:
        src = fitTo(src, dst)

    src = src._auto_cast(dst._dtype)

    return dst(src)


def connect(src, *destinations, exclude=set(), fit=False):
    """
    Connect src (signals/interfaces/values) to all destinations

    :param exclude: interfaces on any level on src or destinations
        which should be excluded from connection process
    :param fit: auto fit source width to destination width
    """
    assignemnts = []
    for dst in destinations:
        assignemnts.extend(_connect(src, dst, exclude, fit))

    return assignemnts


def _mkOp(fn):
    """
    Function to create variadic operator function

    :param fn: function to perform binary operation
    """
    def op(*operands, key=None) -> RtlSignalBase:
        """
        :param operands: variadic parameter of input uperands
        :param key: optional function applied on every operand
            before processing
        """
        assert operands, operands
        top = None
        if key is not None:
            operands = map(key, operands)

        for s in operands:
            if top is None:
                top = s
            else:
                top = fn(top, s)
        return top

    return op


# variadic operator functions
And = _mkOp(and_)
Add = _mkOp(add)
Or = _mkOp(or_)
Xor = _mkOp(xor)
Concat = _mkOp(concatFn)


def power(base, exp) -> RtlSignalBase:
    return toHVal(base)._pow(exp)


def ror(sig, howMany) -> RtlSignalBase:
    "Rotate right"
    return sig[howMany:]._concat(sig[:howMany])


def rol(sig, howMany) -> RtlSignalBase:
    "Rotate left"
    width = sig._dtype.bit_length()
    return sig[(width - howMany):]._concat(sig[:(width - howMany)])


def sll(sig, howMany) -> RtlSignalBase:
    "Logical shift left"
    width = sig._dtype.bit_length()
    return sig[(width - howMany):]._concat(vec(0, howMany))


def srl(sig, howMany) -> RtlSignalBase:
    "Logical shift right"
    return vec(0, howMany)._concat(sig[:howMany])


def log2ceil(x):
    """
    Returns no of bits required to store x-1
    for example x=8 returns 3
    """

    if not isinstance(x, (int, float)):
        x = int(x)

    if x == 0 or x == 1:
        res = 1
    else:
        res = math.ceil(math.log2(x))

    return hInt(res)


def isPow2(num) -> bool:
    if not isinstance(num, int):
        num = int(num)
    return num != 0 and ((num & (num - 1)) == 0)


def binToGray(sigOrVal) -> RtlSignalBase:
    width = sigOrVal._dtype.bit_length()
    return Concat(sigOrVal[width - 1],
                  sigOrVal[width - 1:0] ^ sigOrVal[width:1])


def sizeof(_type) -> int:
    "get size of type in bytes"
    s = _type.bit_length()
    return math.ceil(s / 8)


# shortcuts
c = connect
