package toki.etherlink.handlers;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.command.ServerCommandSource;
import net.minecraft.util.WorldSavePath;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class WhitelistHandler {
    private static final Logger LOGGER = LoggerFactory.getLogger("EtherLink");
    private static MinecraftServer server;

    // Register event to get MinecraftServer instance on startup
    public static void initialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server -> {
            WhitelistHandler.server = server;
        });
    }

    /**
     * Whitelists a Java or Bedrock user
     * @param delimitedString string with data divided with | char
     */
    public static void handleWhitelist(String delimitedString) {
        if (server == null) {
            LOGGER.error("Server instance is null. Cannot execute whitelist command.");
            return;
        }

        String[] parts = delimitedString.split("\\|");

        String invoker = parts[0];
        String version = parts[1];
        String username;
        String floodgateuid;

        if (version.equals("java")) {
            username = parts[2];
            consoleCommand("whitelist add " + username);
            LOGGER.info(invoker + " attempted command: whitelist add " + username);
        } else if (version.equals("bedrock")) {
            username = parts[2];
            floodgateuid = parts[3];

            if (editWhitelistFile(username, floodgateuid)) {
                consoleCommand("whitelist reload");
            }

            LOGGER.info(invoker + " attempted command: bedrock whitelist " + username);
        }
    }

    /**
     * Runs a command in the Minecraft server console.
     */
    private static void consoleCommand(String command) {
        if (server != null) {
            server.execute(() -> {
                ServerCommandSource commandSource = server.getCommandSource();
                server.getCommandManager().executeWithPrefix(commandSource, command);
            });
        } else {
            LOGGER.error("Server instance is null. Cannot execute command: " + command);
        }
    }

    /**
     * Edits the whitelist.json file to add a new Bedrock user entry.
     */
    private static boolean editWhitelistFile(String username, String floodgateuid) {
        if (server == null) {
            LOGGER.error("Server instance is null. Cannot edit whitelist.json.");
            return false;
        }

        // Get whitelist.json file path
        File whitelistFile = server.getSavePath(WorldSavePath.ROOT).resolve("whitelist.json").toFile();

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
                writer.write(whitelist.toString(4));
            }

            LOGGER.info("Added Bedrock user to whitelist.json: " + username);
            return true;
        } catch (IOException e) {
            LOGGER.error("Error editing whitelist.json: " + e.getMessage());
            return false;
        } catch (Exception e) {
            LOGGER.error("Error parsing whitelist.json: " + e.getMessage());
            return false;
        }
    }
}
