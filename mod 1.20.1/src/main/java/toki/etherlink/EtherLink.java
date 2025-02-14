package toki.etherlink;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import toki.etherlink.events.ChatListener;
import toki.etherlink.events.PlayerCountListener;
import toki.etherlink.handlers.WhitelistHandler;
import toki.etherlink.websocket.IncomingSignal;
import toki.etherlink.websocket.InitWebSocket;

import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URISyntaxException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.github.cdimascio.dotenv.Dotenv;

public class EtherLink implements ModInitializer {
    public static final String MOD_ID = "etherlink";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);
    private InitWebSocket webSocket;
    private String websocketUrl;
    private ChatListener chatListener;

    @Override
    public void onInitialize() {
        LOGGER.info("[EtherLink] Initializing mod...");

        // Load environment variables
        Dotenv dotenv = Dotenv.load();
        websocketUrl = dotenv.get("WEBSOCKET_URL");

        // Initialize WebSocket
        startWebSocketServer();

		// Initialize server instances
        IncomingSignal.initialize();
        WhitelistHandler.initialize();

        // Register events initially
        registerEvents();

        // Ensure WebSocket and events restart on server restart
        ServerLifecycleEvents.SERVER_STARTING.register(server -> {
            LOGGER.info("[EtherLink] Server restarting... Restarting WebSocket and events.");
            startWebSocketServer();
            registerEvents();
        });

        LOGGER.info("[EtherLink] Mod initialized successfully!");
    }

    private void startWebSocketServer() {
        if (webSocket != null) {
            LOGGER.info("[EtherLink] Stopping old WebSocket instance...");
            try {
                webSocket.stop();
            } 
			catch (InterruptedException e) {
                LOGGER.error("[EtherLink] ERROR: Couldn't stop WebSocket.", e);
            }
        }

        try {
            URI uri = new URI(websocketUrl);
            String host = uri.getHost();
            int port = uri.getPort();

            // Start WebSocket server
            webSocket = new InitWebSocket(new InetSocketAddress(host, port));
            webSocket.start();
            LOGGER.info("[EtherLink] WebSocket server started successfully.");
        } 
		catch (URISyntaxException e) {
            LOGGER.error("[EtherLink] ERROR: Invalid WebSocket URL!", e);
        }
    }

    private void registerEvents() {       
        LOGGER.info("[EtherLink] Registering Chat Listener...");
        chatListener = new ChatListener(webSocket);
        chatListener.register();

		LOGGER.info("[EtherLink] Registering Join/Leave Listener...");
		PlayerCountListener playerCountListener = new PlayerCountListener(webSocket);
    	playerCountListener.register();
    }
}
