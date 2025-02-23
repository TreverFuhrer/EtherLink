import asyncio
import json
import websockets
import os
from dotenv import load_dotenv
from handlers import joinLeave_handler
from handlers import chat_handler
from database import get_all_servers, get_discord_id
from handlers.joinLeave_handler import update_player_count_channel

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")

# Event dictionary: Maps events to handler functions
EVENTS = {
    "CHAT_MESSAGE": chat_handler.process_chat_message,
    "PLAYER_COUNT_UPDATE" : joinLeave_handler.update_player_count_channel
}

# Global Variable
active_websockets = {}

# Connect bot to plugin websocket server
async def connect_to_websockets(discord_id, websocket_url):
    """Connects to a Minecraft server WebSocket and listens for messages."""
    sleep_duration = 10
    attempts = 0
    set_offline = False
    
    while True:
        if (attempts > 12):
            sleep_duration = 60
        try:
            async with websockets.connect(websocket_url, extra_headers={"AUTH_TOKEN": AUTH_TOKEN}
            ) as websocket:
                print("Connected to the WebSocket server.")
                active_websockets[discord_id] = websocket

                # Reset temp variables
                attempts = 0
                sleep_duration = 10
                if set_offline:
                    await update_player_count_channel({"player_count": 0}, discord_id)
                    set_offline = False

                # Start listening for messages
                while True:
                    await handle_signals(websocket)

        except Exception as e:
            print(f"WebSocket connection lost for {websocket_url}. Retrying in {sleep_duration} seconds...")
            attempts += 1
            active_websockets.pop(discord_id, None)
            if not set_offline:
                await update_player_count_channel({"player_count": " "}, discord_id)
                set_offline = True
            await asyncio.sleep(sleep_duration) # Wait before retrying


async def initialize_connections():
    """Loads all linked servers and connects to their WebSockets on startup."""
    print(get_all_servers())
    servers = get_all_servers()
    for discord_id, server in servers.items():
        if "websocket_url" in server and server["websocket_url"]:
            asyncio.create_task(connect_to_websockets(discord_id, server["websocket_url"]))


# Handle incoming messages
async def handle_signals(websocket):
    """ Handles incoming WebSocket messages. """
    signal = await websocket.recv()                
    data = json.loads(signal)
    event_type = data.get("type")
    request_id = data.get("request_id")
    discord_id = get_discord_id(data.get("mc_ip"))

    # Check if this is a response to a pending request
    if request_id and request_id in pending_requests:
        pending_requests[request_id].set_result(data)
    else:
        # Route the signal to the correct event handler
        handler = EVENTS.get(event_type)
        if handler:
            await handler(data, discord_id)
        else:
            print(f"Unrecognized event type: {event_type}")


# Send signal message to plugin
async def send_signal(discord_id, message_type, data, ctx=None):
    """Send a JSON message to the WebSocket server."""
    ws = active_websockets.get(discord_id)
    if ws:
        signal = {"request_id": None, "type": message_type, **data}
        await ws.send(json.dumps(signal))
    else:
        error_msg = "Error, WebSocket connection not established."
        if ctx:
            await ctx.reply(error_msg, ephemeral=True)
        else:
            print(error_msg)


# Send requests for data
pending_requests = {}

async def send_request(discord_id, message_type, data, timeout=5):
    """ Sends a request to the WebSocket server and waits for a response. """

    if discord_id not in active_websockets:
        return {"error": "WebSocket connection not established"}

    # Create a unique request ID
    request_id = f"{message_type}-{data.get('username', 'unknown')}-{os.urandom(4).hex()}"

    # Create an asyncio.Future to wait for a response
    future = asyncio.Future()
    pending_requests[request_id] = future

    try:
        # Send the request
        ws = active_websockets.get(discord_id)
        signal = {"request_id": request_id, "type": message_type, **data}
        await ws.send(json.dumps(signal))

        # Wait for response or timeout
        response = await asyncio.wait_for(future, timeout)
        return response
    except asyncio.TimeoutError:
        return {"error": "Request timed out"}
    finally:
        pending_requests.pop(request_id, None)  # Cleanup