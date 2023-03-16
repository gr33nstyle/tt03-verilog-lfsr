import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


segments = [ 63, 6, 91, 79, 102, 109, 124, 7, 127, 103 ]

@cocotb.test()
async def test_lfsr(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0

    dut._log.info("check all segments")
# 01010101 reg -> 01
# 00110011 xor -> 10
# x
# 10101010 after shift
# 10011001 after xor

    # simple test case
    dut.mode.value = 1
    dut.data_in.value = 0x4
    await ClockCycles(dut.clk, 1)
    dut.data_in.value = 0x2
    await ClockCycles(dut.clk, 1)

    dut.mode.value = 2
    dut.data_in.value = 0x5
    await ClockCycles(dut.clk, 1)
    dut.data_in.value = 0x2
    await ClockCycles(dut.clk, 1)

    dut.mode.value = 3
    dut.data_in.value = 0x0
    await ClockCycles(dut.clk, 1)

    dut.mode.value = 0
    for i in range(256):
        dut._log.info("state: %s" % dut.data_out.value)
        await ClockCycles(dut.clk, 1)