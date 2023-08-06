import cocotb
import numpy as np
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.result import ReturnValue
from cocotb.triggers import RisingEdge, Timer


@cocotb.coroutine
def reset(dut, duration=10000):
    dut.log.debug("Resetting DUT")
    dut.rst_n = 0
    yield Timer(duration)
    yield RisingEdge(dut.clk)
    dut.rst_n = 1
    dut.log.debug("Out of reset")


@cocotb.coroutine
def run_dut(dut, in_data, out_count):
    # dut.enable = 1
    # dut.in0 = 0
    cocotb.fork(Clock(dut.clk, 5000).start())
    yield reset(dut)

    ret = []
    # print('Input data: {}'.format(in_data))
    for x in in_data:

        # put input
        # print('Processing slice: {}'.format(x))
        for i, xi in enumerate(x):
            # print('Set {} to {}'.format('in' + str(i), str(xi)))
            v = getattr(dut, 'in' + str(i))
            bval = BinaryValue(str(xi), len(xi))
            v.setimmediatevalue(bval)

        yield RisingEdge(dut.clk)

        # collect output
        tmp = []
        for i in range(out_count):
            var = 'out' + str(i)
            # val = getattr(dut, var).value.signed_integer
            val = str(getattr(dut, var).value)
            # print(val)
            tmp.append(val)
        ret.append(tmp)

    # print('Finish, ret: {}'.format(ret))
    raise ReturnValue(ret)


@cocotb.test()
def test_main(dut):
    import os
    in_data = np.load(os.getcwd() + '/../input.npy')

    output_vars = int(os.environ['OUTPUT_VARIABLES'])
    hdl_out = yield run_dut(dut, in_data, output_vars)

    np.save(os.getcwd() + '/../output.npy', hdl_out)
