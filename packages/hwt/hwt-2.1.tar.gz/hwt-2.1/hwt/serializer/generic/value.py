from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bool import HBool
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.integer import Integer
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.string import String
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class GenericSerializer_Value():
    @classmethod
    def Value(cls, val, ctx):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or Value
        """
        t = val._dtype

        if isinstance(val, RtlSignalBase):
            return cls.SignalItem(val, ctx)

        # try to extract value as constant
        try:
            consGetter = ctx.constCache.getConstName
        except AttributeError:
            consGetter = None

        if consGetter and not isinstance(t, HEnum):
            return "self." + consGetter(val)

        if isinstance(t, Slice):
            return cls.Slice_valAsHdl(t, val, ctx)
        elif isinstance(t, HArray):
            return cls.HArrayValAsHdl(t, val, ctx)
        elif isinstance(t, Bits):
            return cls.Bits_valAsHdl(t, val, ctx)
        elif isinstance(t, HBool):
            return cls.Bool_valAsHdl(t, val, ctx)
        elif isinstance(t, HEnum):
            return cls.HEnumValAsHdl(t, val, ctx)
        elif isinstance(t, Integer):
            return cls.Integer_valAsHdl(t, val, ctx)
        elif isinstance(t, String):
            return cls.String_valAsHdl(t, val, ctx)
        else:
            raise Exception("can not resolve value serialization for %r"
                            % (val))

    @classmethod
    def Integer_valAsHdl(cls, dtype, val, ctx):
        return str(int(val.val))

    @classmethod
    def Bits_valAsHdl(cls, dtype, val, ctx):
        w = dtype.bit_length()
        if dtype.signed is None:
            if dtype.forceVector or w > 1:
                return cls.BitString(val.val, w, val.vldMask)
            else:
                return cls.BitLiteral(val.val, val.vldMask)
        elif dtype.signed:
            return cls.SignedBitString(val.val, w, dtype.forceVector,
                                       val.vldMask)
        else:
            return cls.UnsignedBitString(val.val, w, dtype.forceVector,
                                         val.vldMask)
