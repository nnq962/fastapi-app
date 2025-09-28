import asyncio
import httpx

URL = "http://127.0.0.1:8000/api/v1/users"
PAYLOADS = [
    {
        "name": "Nguyễn Ngọc Quyết",
        "phone": "1149999002",
        "position": "Dev IT",
    },
    {
        "name": "Nguyễn Ngọc Quyết",
        "phone": "1149999002",
        "position": "Dev IT",
    },
        {
        "name": "Nguyễn Ngọc Quyết",
        "phone": "1149999002",
        "position": "Dev IT",
    },
    {
        "name": "Nguyễn Ngọc Quyết",
        "phone": "1149999002",
        "position": "Dev IT",
    },
        {
        "name": "Nguyễn Ngọc Quyết",
        "phone": "1149999002",
        "position": "Dev IT",
    },
        {
        "name": "Nguyễn Ngọc Quyết",
        "phone": "1149999002",
        "position": "Dev IT",
    },
]


async def fire(label: str, payload: dict):
    async with httpx.AsyncClient(timeout=5) as client:
        resp = await client.post(URL, json=payload)
        print(f"{label}: status={resp.status_code} body={resp.text}")


async def main():
    await asyncio.gather(
        fire("req-1", PAYLOADS[0]),
        fire("req-2", PAYLOADS[1]),
        fire("req-3", PAYLOADS[2]),
        fire("req-4", PAYLOADS[3]),
        fire("req-5", PAYLOADS[4]),
        fire("req-6", PAYLOADS[5]),
    )


if __name__ == "__main__":
    asyncio.run(main())
