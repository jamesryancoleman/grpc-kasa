from kasa.iot import IotPlug
import asyncio

# TODO update function calls to use Module.Energy

# all async defs use this value. Must be set externally.
addr = "" 

async def On_Off(on_for=2.5):
    p = IotPlug(addr)
    await p.update()
    await p.turn_on()
    await asyncio.sleep(on_for)
    await p.turn_off()

async def On():
    p = IotPlug(addr)
    await p.update()
    await p.turn_on()

async def Off():
    p = IotPlug(addr)
    await p.turn_off()

async def State() -> bool:  
    p = IotPlug(addr)
    await p.update()
    return p.is_on

async def Power() -> float:
    p = IotPlug(addr)
    await p.update()
    return p.emeter_realtime.power

async def Voltage() -> float:
    p = IotPlug(addr)
    await p.update()
    return p.emeter_realtime.voltage

async def Current() -> float:
    p = IotPlug(addr)
    await p.update()
    return p.emeter_realtime.current

async def Usage() -> float:
    p = IotPlug(addr)
    await p.update()
    return p.emeter_realtime.total


if __name__ == "__main__":
    print("Restarting the switch at {}".format(addr))
    asyncio.run(On_Off(1.5))

    print("turning on again")
    asyncio.run(On())
    # add a delay so the power measurement is accurate
    asyncio.run(asyncio.sleep(2.5))
    power = asyncio.run(Power())
    print("Power draw is: {}".format(power))
    asyncio.run(Off())
    print("switch turned off")

   