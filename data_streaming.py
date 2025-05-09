import asyncio
import websockets
import json
import time

# WebSocket server URL (could be your internal server or third-party service)
SERVER_URL = "wss://yourwebsocketserver.com/data"

async def send_data(websocket, path):
    """Simulate streaming data to the client in real-time"""
    while True:
        # Simulate data fetching (in real use, fetch actual data)
        data = {
            "timestamp": time.time(),
            "value": 100 + (time.time() % 50),  # Example value that changes over time
            "status": "OK"
        }

        # Send the data to the connected client
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)  # Stream data every second

async def start_server():
    """Start the WebSocket server for real-time data streaming"""
    async with websockets.serve(send_data, "localhost", 8765):
        print("Server started, awaiting connections...")
        await asyncio.Future()  # Keep the server running indefinitely

# Example of the client-side connection
async def stream_data():
    """Connect to the WebSocket server and receive real-time data"""
    async with websockets.connect(SERVER_URL) as websocket:
        while True:
            # Wait for the incoming message
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received data: {data}")

if __name__ == "__main__":
    # Start WebSocket server to stream data (run on a server)
    asyncio.run(start_server())
    
    # Simulate a client-side connection for testing
    # asyncio.run(stream_data())  # Uncomment to run the client
