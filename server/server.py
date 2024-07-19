import asyncio
import websockets

async def handler(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            print(f"Received message from client: {message}")
            response = input("Enter your message to send to client: ")
            await websocket.send(response)
        except websockets.ConnectionClosed:
            print("Connection closed")
            break

async def main():
    async with websockets.serve(handler, "172.20.10.2", 8765):
        print("Server started, waiting for connection...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())