"""
Simple example that sends a Read Property request and decodes the response.
python .\bacnet_test.py --address 192.168.10.132/24:47808 192.168.10.50 multi-state-value,0 present-value
"""

import asyncio
import re
import pytest

from bacpypes3.debugging import ModuleLogger
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application

from bacpypes3.pdu import Address
from bacpypes3.primitivedata import ObjectIdentifier, PropertyIdentifier
from bacpypes3.constructeddata import AnyAtomic
from bacpypes3.apdu import ErrorRejectAbortNack

# some debugging
_debug = 0
_log = ModuleLogger(globals())

# 'property[index]' matching
property_index_re = re.compile(r"^([0-9A-Za-z-]+)(?:\[([0-9]+)\])?$")

app = None


class MyTestCase:
    async def test_1(self):
        assert True

    async def test_2(self):
        await app.read_property(
            Address("192.168.1.5"),
            ObjectIdentifier("multi-state-value,0"),
            PropertyIdentifier("present-value"),
            -1,
        )


async def bacnet_app():

    try:
        global app
        parser = SimpleArgumentParser()
        parser.add_argument(
            "device_address",
            help="address of the server (B-device)",
        )
        parser.add_argument(
            "object_identifier",
            help="object identifier",
        )
        parser.add_argument(
            "property_identifier",
            help="property identifier with optional array index",
        )
        args = parser.parse_args()
        if _debug:
            _log.debug("args: %r", args)

        # interpret the address
        device_address = Address(args.device_address)
        if _debug:
            _log.debug("device_address: %r", device_address)

        # interpret the object identifier
        object_identifier = ObjectIdentifier(args.object_identifier)
        if _debug:
            _log.debug("object_identifier: %r", object_identifier)

        # split the property identifier and its index
        property_index_match = property_index_re.match(args.property_identifier)
        if not property_index_match:
            raise ValueError("property specification incorrect")
        property_identifier, property_array_index = property_index_match.groups()
        if property_identifier.isdigit():
            property_identifier = int(property_identifier)
        if property_array_index is not None:
            property_array_index = int(property_array_index)

        # build an application
        app = Application.from_args(args)
        if _debug:
            _log.debug("app: %r", app)

        try:
            response = await app.read_property(
                device_address,
                object_identifier,
                property_identifier,
                property_array_index,
            )
            if _debug:
                _log.debug("    - response: %r", response)
        except ErrorRejectAbortNack as err:
            if _debug:
                _log.debug("    - exception: %r", err)
            response = err

        if isinstance(response, AnyAtomic):
            if _debug:
                _log.debug("    - schedule objects")
            response = response.get_value()

        print(str(response))

        await asyncio.Future()

    finally:
        if app:
            app.close()


async def main():

    asyncio.create_task(bacnet_app())
    asyncio.create_task(pytest.main(["test_bacnet.py"]))


if __name__ == "__main__":
    asyncio.run(main())
