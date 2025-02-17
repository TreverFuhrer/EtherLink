package org.toki.neoplugin.websocket;

import java.net.InetSocketAddress;
import java.util.logging.Logger;

import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import io.github.cdimascio.dotenv.Dotenv;

public class InitWebSocket extends WebSocketServer {

    private WebSocket botConnection = null;
    private final Logger logger;
    private final String AUTH_TOKEN;

    public InitWebSocket(InetSocketAddress address, Logger logger) {
        super(address);
        this.logger = logger;
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
        this.AUTH_TOKEN = dotenv.get("AUTH_TOKEN");
    }

    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {
        String clientAuthToken = handshake.getFieldValue("AUTH_TOKEN");
        if (AUTH_TOKEN.equals(clientAuthToken)) {
            if (botConnection == null || !botConnection.isOpen()) {
                botConnection = conn;
                logger.info("[EtherLink] Authorized connection: " + conn.getRemoteSocketAddress());
            }
        } 
        else {
            logger.warning("Unauthorized connection attempt: " + conn.getRemoteSocketAddress());
            conn.close(); // Close unauthorized connection
        }
    }

    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {
        logger.info("[EtherLink] Connection closed: Code=" + code + ", Reason=" + reason);
        logger.info("[EtherLink] Connection closed: " + conn.getRemoteSocketAddress());
        if (conn == botConnection) botConnection = null;
    }

    @Override // Handle incoming messages
    public void onMessage(WebSocket conn, String signal) {
        logger.info("Received message: " + signal);
        IncomingSignal.routeSignal(signal);
    }

    @Override
    public void onError(WebSocket conn, Exception ex) {
        logger.warning("Error: " + ex.getMessage());
    }

    @Override
    public void onStart() {
        logger.info("WebSocket server started successfully.");
    }

    // Send signal message to bot
    public void sendSignal(String signal) {
        if (botConnection != null && botConnection.isOpen()) {
            botConnection.send(signal);
        }
    }

}
