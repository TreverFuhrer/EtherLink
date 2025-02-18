package org.toki.neoplugin;

import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;

import org.bukkit.event.Listener;
import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;
import org.toki.neoplugin.events.ChatListener;
//import org.toki.neoplugin.events.PlayerCountListener;
import org.toki.neoplugin.websocket.InitWebSocket;
import java.util.logging.Logger;

import io.github.cdimascio.dotenv.Dotenv;

public final class NeoPlugin extends JavaPlugin {

    private static NeoPlugin instance;
    private static InitWebSocket webSocket;
    private static Logger logger;

    @Override
    public void onEnable() {
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
        instance = this;
        logger = getLogger();

        try {
            URI uri = new URI(dotenv.get("WEBSOCKET_URL"));
            String host = uri.getHost();
            int port = uri.getPort();

            // New webSocket with (address, logger) and starts it
            webSocket = new InitWebSocket(new InetSocketAddress(host, port));
            webSocket.start();
        } 
        catch (URISyntaxException e) {
            logger.info("[NeoPlugin] WebSocket failed to enable/start: " + e.getMessage());    
            e.printStackTrace();
        }

        // Register all event listeners
        registerListeners(
            List.of(
                new ChatListener()//,
                //new PlayerCountListener(webSocket)
                // Add other listeners here as needed
            )
        );

        // Startup log message
        logger.info("[NeoPlugin] Enabled and WebSocket client connected.");    
    }

    @Override // Shutdown websocket server when plugin disabled
    public void onDisable() {
        try {
            if (webSocket != null) {
                webSocket.stop();
                logger.info("[NeoPlugin] WebSocket server stopped.");
            }
        } catch (Exception e) {
            logger.info("[NeoPlugin] WebSocket failed to disable/stop: " + e.getMessage());    
            e.printStackTrace();
        }
    }    

    // Return instance of plugin
    public static NeoPlugin getInstance() {
        return instance;
    }

    // Return current websocket connect
    public static InitWebSocket getWebSocket() {
        return webSocket;
    }

    // Return the plugin logger
    public static Logger logger() {
        return logger;
    }

    /**
     * Registers all listeners into the plugin manager
     * @param listeners list of all listeners to be registered
     */
    private void registerListeners(List<Listener> listeners) {
        PluginManager pluginManager = getServer().getPluginManager();
        for (Listener listener : listeners) {
            pluginManager.registerEvents(listener, this);
        }
    }

}
