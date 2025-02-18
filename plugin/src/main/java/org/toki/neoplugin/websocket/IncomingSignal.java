package org.toki.neoplugin.websocket;

import org.bukkit.Bukkit;
import org.json.JSONObject;
import org.toki.neoplugin.NeoPlugin;
import org.toki.neoplugin.handlers.WhitelistHandler;

/**
 * Handles incoming signal from Discord Bot
 */
public class IncomingSignal {

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
            case "SERVER_CHAT":
                consoleCommand("say " + data);
                break;
            case "WHITELIST":
                WhitelistHandler.handleWhitelist(data, NeoPlugin.getInstance());
                break;
            default:
                NeoPlugin.logger().info("[NeoPlugin] Unknown event type: " + eventType);
        }
    }

    // Helper method to run commands in server console
    private static void consoleCommand(String command) {
        Bukkit.getScheduler().runTask(NeoPlugin.getInstance(), () -> {
            Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), command);
        });
    }
}
