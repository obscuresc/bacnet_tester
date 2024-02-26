import pytest
import asyncio

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_simple():
    await asyncio.sleep(1)


"""
class MyTestCase:

    @pytest.mark.asyncio
    async def test_1(self):
        await asyncio.sleep(1)
        assert True

    @pytest.mark.asyncio
    async def test_2(self):
        await app.read_property(
            Address("192.168.1.5"),
            ObjectIdentifier("multi-state-value,0"),
            PropertyIdentifier("present-value"),
            -1,
        )

        assert False

"""
