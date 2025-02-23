package toki.etherlink.websocket;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.server.MinecraftServer;
import toki.etherlink.EtherLink;
import toki.etherlink.handlers.WhitelistHandler;

import org.json.JSONObject;
import org.slf4j.Logger;

public class IncomingSignal {

    private static MinecraftServer server;
    private static final Logger LOGGER = EtherLink.LOGGER;

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
        String data = json.optString("message");
        //String requestId = json.optString("request_id", "");

        switch (eventType) {
            case "SERVER_CHAT":
                consoleCommand("say " + data);
                break;
            case "WHITELIST":
                WhitelistHandler.handleWhitelist(data);
                break;
            default:
                LOGGER.info("[EtherLink] Unknown event type: " + eventType);
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