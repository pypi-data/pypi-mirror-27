class BasicDbAdapter:
    """
    Interface for db adapters to make it compatible with basic driver
    """
    def __init__(self):
        pass

    async def check(self, thing, version=None, vendor=None):
        raise NotImplementedError("'check' method is not implemented for this db adapter. Please implement this interface")
