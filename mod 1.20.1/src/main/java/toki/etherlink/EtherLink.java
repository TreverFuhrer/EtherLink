package toki.etherlink;

import net.fabricmc.api.ModInitializer;
import toki.etherlink.events.ChatListener;
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
    private static InitWebSocket webSocket;

    @Override
    public void onInitialize() {
        LOGGER.info("[EtherLink] Initializing mod...");

        // Load environment variables
        Dotenv dotenv = Dotenv.load();
        String websocketUrl = dotenv.get("WEBSOCKET_URL");

        // Initialize WebSocket
        try {
            URI uri = new URI(websocketUrl);
            String host = uri.getHost();
            int port = uri.getPort();

            // Start WebSocket server
            webSocket = new InitWebSocket(new InetSocketAddress(host, port));
            webSocket.start();
            LOGGER.info("[EtherLink] WebSocket server started successfully.");
        } catch (URISyntaxException e) {
            LOGGER.error("[EtherLink] ERROR: Invalid WebSocket URL!", e);
        }

		// Initialize server instances
        IncomingSignal.initialize();
        WhitelistHandler.initialize();

        // Register events initially
        registerEvents();

        LOGGER.info("[EtherLink] Mod initialized successfully!");
    }

    // Return current websocket connection
    public static InitWebSocket getWebSocket() {
        return webSocket;
    }

    private void registerEvents() {       
        LOGGER.info("[EtherLink] Registering Chat Listener...");
        new ChatListener().register();

		//LOGGER.info("[EtherLink] Registering Join/Leave Listener...");
		//PlayerCountListener playerCountListener = new PlayerCountListener(webSocket);
    	//playerCountListener.register();
    }
}
