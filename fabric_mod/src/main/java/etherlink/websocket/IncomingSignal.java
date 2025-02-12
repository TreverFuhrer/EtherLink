package etherlink.websocket;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.server.MinecraftServer;
import org.json.JSONObject;


public class IncomingSignal {

    private static MinecraftServer server;

    // Initialize with the Minecraft server instance
    public static void initialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server -> {
            IncomingSignal.server = server;
        });
    }

    /**
     * Routes incoming signals from the Discord bot to the appropriate handlers.
     * @param signal JSON message received from WebSocket
     */
    public static void routeSignal(String signal) {
        JSONObject json = new JSONObject(signal);
        String eventType = json.getString("type");
        String data = json.optString("message", "");
        String requestId = json.optString("request_id", "");

        switch (eventType) {
            case "CHAT_MESSAGE":
                // ChatHandler.handleChatMessage(json);
                break;
            case "SERVER_CHAT":
                consoleCommand("say " + data);
                break;
            case "WHITELIST":
                //WhitelistHandler.handleWhitelist(json);/////////////////////////////////////////////////////////
                break;
            default:
                System.out.println("[EtherLink] Unknown event type: " + eventType);
        }
    }

    /**
     * Runs a command in the Minecraft server console.
     * @param command The command to execute
     */
    private static void consoleCommand(String command) {
        if (server != null) {
            server.execute(() -> {
                server.getCommandManager().executeWithPrefix(server.getCommandSource(), command);
            });
        }
    }
}