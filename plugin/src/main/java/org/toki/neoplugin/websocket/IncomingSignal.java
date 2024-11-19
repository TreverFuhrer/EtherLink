package org.toki.neoplugin.websocket;

import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;
import org.json.JSONObject;
import org.toki.neoplugin.handlers.WhitelistHandler;

/**
 * Handles incoming signal from Discord Bot
 */
public class IncomingSignal {
    
    private static JavaPlugin plugin;

    public static void initialize(JavaPlugin pluginInstance) {
        plugin = pluginInstance;
    }
    
    /** 
     * Route incomming signal message to handlers
     * @param signal message from bot
     */
    public static void routeSignal(String signal) {
        JSONObject json = new JSONObject(signal);
        String eventType = json.getString("type");
        String data = json.getString("message");

        switch (eventType) {
            case "CHAT_MESSAGE":
                //ChatHandler.handleChatMessage(json);
                break;
            case "SERVER_CHAT":
                consoleCommand("say " + data);
                break;
            case "WHITELIST":
                WhitelistHandler.handleWhitelist(data, plugin);
                break;
            default:
                System.out.println("Unknown event type: " + eventType);
        }
    }

    // Helper method to run commands in server console
    private static void consoleCommand(String command) {
        Bukkit.getScheduler().runTask(plugin, () -> {
            Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), command);
        });
    }
}
