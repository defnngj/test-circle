import unittest
import httpx


class AsyncTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.cli = httpx.AsyncClient()
        print("asyncSetUp")

    async def test_response(self):
        print("test_response")
        response = await self.cli.get("http://127.0.0.1:5000/")
        self.assertEqual(response.status_code, 200)

    async def test_response2(self):
        print("test_response")
        response = await self.cli.get("http://127.0.0.1:5000/")
        self.assertEqual(response.status_code, 200)

    async def asyncTearDown(self):
        await self.cli.aclose()
        print("asyncTearDown")


if __name__ == "__main__":
    unittest.main()

