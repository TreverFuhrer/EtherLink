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
        //String request_id = json.getString("request_id");

        // Read - important for whitelist vvv

        // Whitelist handler could prob be improved a lot
        // This is because in it i have data as a string and i parse username and stuff out of it
        // But in the bot it sends **data which adds the data dictionary to it
        // So if the data dic has the username and stuff then i can just put the jsonObj into handleWhitelist
        // And with the jsonObj i can just do json.getString("username") or for request_id

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
