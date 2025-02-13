package toki.etherlink;

import net.fabricmc.api.ModInitializer;
import toki.etherlink.events.ChatListener;
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

	// This logger is used to write text to the console and the log file.
	// It is considered best practice to use your mod id as the logger's name.
	// That way, it's clear which mod wrote info, warnings, and errors.
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	private InitWebSocket webSocket;

	@Override
	public void onInitialize() {
		// This code runs as soon as Minecraft is in a mod-load-ready state.
		// However, some things (like resources) may still be uninitialized.
		// Proceed with mild caution.

		Dotenv dotenv = Dotenv.load();

		LOGGER.info("[EtherLink] Initializing mod...");

        // Initialize WebSocket connection
        try {
            URI uri = new URI(dotenv.get("WEBSOCKET_URL"));
            String host = uri.getHost();
            int port = uri.getPort();

            // Initialize WebSocket and start connection
            webSocket = new InitWebSocket(new InetSocketAddress(host, port));
            webSocket.start();
            LOGGER.info("[EtherLink] WebSocket server started.");
        } catch (URISyntaxException e) {
            LOGGER.error("[EtherLink] Invalid WebSocket URL!", e);
        }

		// Initialize listening for incoming signals
		IncomingSignal.initialize();

		// Register Events
		ChatListener chatListener = new ChatListener(webSocket);
        chatListener.register();

        LOGGER.info("[EtherLink] Mod initialized successfully!");
	}
}