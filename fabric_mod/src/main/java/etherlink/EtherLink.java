package etherlink;

import net.fabricmc.api.ModInitializer;

import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URISyntaxException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import etherlink.websocket.InitWebSocket;
import io.github.cdimascio.dotenv.Dotenv;

public class EtherLink implements ModInitializer {
	// This logger is used to write text to the console and the log file.
	// It is considered best practice to use your mod id as the logger's name.
	// That way, it's clear which mod wrote info, warnings, and errors.
	public static final String MOD_ID = "etherlink";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);
	private InitWebSocket webSocket;

    @Override
    public void onInitialize() {
        LOGGER.info("[EtherLink] Initializing mod...");

        // Initialize WebSocket connection
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
        try {
            URI uri = new URI(dotenv.get("WEBSOCKET_URL"));
            String host = uri.getHost();
            int port = uri.getPort();

            // Initialize WebSocket and start connection
            webSocket = new InitWebSocket(new InetSocketAddress(host, port));
            webSocket.start();
            LOGGER.info("[EtherLink] WebSocket client started.");
        } catch (URISyntaxException e) {
            LOGGER.error("[EtherLink] Invalid WebSocket URL!", e);
        }

        // Initialize event listeners
        //IncomingSignal.initialize(this);
        registerListeners();

        LOGGER.info("[EtherLink] Mod initialized successfully!");
    }

    private void registerListeners() {
        
        // Add more event listeners here as needed
    }
}