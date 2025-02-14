package org.toki.neoplugin;

import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;

import org.bukkit.event.Listener;
import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;
import org.toki.neoplugin.events.ChatListener;
import org.toki.neoplugin.events.PlayerCountListener;
import org.toki.neoplugin.websocket.IncomingSignal;
import org.toki.neoplugin.websocket.InitWebSocket;

import io.github.cdimascio.dotenv.Dotenv;

public final class NeoPlugin extends JavaPlugin {

    private static NeoPlugin instance;
    private InitWebSocket webSocket;

    @Override
    public void onEnable() {
        IncomingSignal.initialize(this);
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
        instance = this;

        try {
            URI uri = new URI(dotenv.get("WEBSOCKET_URL"));
            String host = uri.getHost();
            int port = uri.getPort();

            // New webSocket with (address, logger) and starts it
            webSocket = new InitWebSocket(new InetSocketAddress(host, port), getLogger());
            webSocket.start();
        } 
        catch (URISyntaxException e) {
            e.printStackTrace();
        }

        // Register all event listeners
        registerListeners(
            List.of(
                new ChatListener(webSocket),
                new PlayerCountListener(webSocket)
                // Add other listeners here as needed
            )
        );

        // Startup log message
        getLogger().info("NeoPlugin enabled and WebSocket client connected.");    
    }

    @Override // Shutdown websocket server when plugin disabled
    public void onDisable() {
        try {
            if (webSocket != null) {
                webSocket.stop();
                getLogger().info("WebSocket server stopped.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }    

    // Return instance of plugin
    public static NeoPlugin getInstance() {
        return instance;
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
