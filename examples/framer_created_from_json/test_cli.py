import os
import asyncio
import unittest
from main import export_config, import_config, Frame


class TestFramerConfig(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_framer_config.json"
        self.frame = Frame()

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    async def test_export_import(self):
        await export_config(self.frame, self.test_filename)
        framer = await import_config(self.test_filename)
        self.assertIsNotNone(framer)
        self.assertTrue(hasattr(framer, "__dict__"))


if __name__ == "__main__":
    asyncio.run(unittest.main())
