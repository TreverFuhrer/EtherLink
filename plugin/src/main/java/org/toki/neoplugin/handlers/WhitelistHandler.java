package org.toki.neoplugin.handlers;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;
import org.json.JSONArray;
import org.json.JSONObject;

public class WhitelistHandler {

    /**
     * Whitelists a Java or Bedrock user
     * @param delimitedString string with data divided with | char
     * @param p plugin object to execute commands on
     */
    public static void handleWhitelist(String delimitedString, JavaPlugin p) {
        String[] parts = delimitedString.split("\\|");

        String version = parts[0];
        String username;
        String floodgateuid;
        if (version.equals("java")) {
            username = parts[1];
            consoleCommand(p, "whitelist add " + username);
        } 
        else if (version.equals("bedrock")) {
            username = parts[1];
            floodgateuid = parts[2];

            if (editWhitelistFile(username, floodgateuid, p)) {
                consoleCommand(p, "whitelist reload");
            }
        } 
        else // "unknown"
            return;
    }

    // Helper method to run commands in server console
    private static void consoleCommand(JavaPlugin plugin, String command) {
        Bukkit.getScheduler().runTask(plugin, () -> {
            Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "reload whitelist");
        });
    }

    /**
     * Edits the whitelist.json file to add a new Bedrock user entry
     */
    private static boolean editWhitelistFile(String username, String floodgateuid, JavaPlugin plugin) {
        File whitelistFile = new File(plugin.getDataFolder().getParentFile(), "whitelist.json");

        try {
            // Read the existing whitelist.json file
            StringBuilder content = new StringBuilder();
            try (FileReader reader = new FileReader(whitelistFile)) {
                int c;
                while ((c = reader.read()) != -1) {
                    content.append((char) c);
                }
            }

            // Parse the JSON content
            JSONArray whitelist = new JSONArray(content.toString());

            // Add a new user
            JSONObject newUser = new JSONObject();
            newUser.put("uuid", floodgateuid);
            newUser.put("name", username);
            whitelist.put(newUser);

            // Write back the updated JSON array to the file
            try (FileWriter writer = new FileWriter(whitelistFile)) {
                writer.write(whitelist.toString(4)); // Pretty print with indentation
            }

            //plugin.getLogger().info("Added Bedrock user to whitelist.json: " + username);
            return true;
        } 
        catch (IOException e) {
            plugin.getLogger().severe("Error editing whitelist.json: " + e.getMessage());
            return false;
        } 
        catch (Exception e) {
            plugin.getLogger().severe("Error parsing whitelist.json: " + e.getMessage());
            return false;
        }
    }
}
