from hwt.hdl.operator import Operator
from hwt.hdl.portItem import PortItem
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.generic.constants import SIGNAL_TYPE


def _isEventDependentDriver(d):
    return not isinstance(d, (PortItem, Operator)) \
        and d.isEventDependent


def verilogTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    if signalItem._const or len(signalItem.drivers) > 1 or\
       arr_any(signalItem.drivers, _isEventDependentDriver) or\
       (signalItem._useNopVal
            and len(signalItem.drivers) > 0
            and signalItem.drivers[0].cond):

        return SIGNAL_TYPE.REG
    else:
        return SIGNAL_TYPE.WIRE
