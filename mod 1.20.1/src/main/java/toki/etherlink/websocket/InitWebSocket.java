package toki.etherlink.websocket;

import java.net.InetSocketAddress;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;
import io.github.cdimascio.dotenv.Dotenv;
import toki.etherlink.EtherLink;

import org.slf4j.Logger;

public class InitWebSocket extends WebSocketServer {

    private WebSocket botConnection = null;
    private static final Logger LOGGER = EtherLink.LOGGER;
    private final String AUTH_TOKEN;

    public InitWebSocket(InetSocketAddress address) {
        super(address);
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
        this.AUTH_TOKEN = dotenv.get("AUTH_TOKEN");
    }

    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {
        String clientAuthToken = handshake.getFieldValue("AUTH_TOKEN");
        if (AUTH_TOKEN.equals(clientAuthToken)) {
            botConnection = conn;
            LOGGER.info("[EtherLink] Authorized connection: " + conn.getRemoteSocketAddress());
            LOGGER.info("[EtherLink] Stored botConnection: " + botConnection);
        } 
        else {
            LOGGER.warn("[EtherLink] Unauthorized connection attempt: " + conn.getRemoteSocketAddress());
            conn.close(); // Close unauthorized connection
        }
    }

    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {
        if (conn == botConnection) botConnection = null;
        LOGGER.info("[EtherLink] Connection closed: " + conn.getRemoteSocketAddress());
    }

    @Override
    public void onMessage(WebSocket conn, String signal) {
        LOGGER.info("[EtherLink] Received message: " + signal);
        IncomingSignal.routeSignal(signal);
    }

    @Override
    public void onError(WebSocket conn, Exception ex) {
        LOGGER.warn("[EtherLink] Error: " + ex.getMessage());
    }

    @Override
    public void onStart() {
        LOGGER.info("[EtherLink] WebSocket server started successfully.");
    }

    // Send signal message to bot
    public void sendSignal(String signal) {
    synchronized (this) {
        if (botConnection != null && botConnection.isOpen()) {
            try {
                botConnection.send(signal);
                LOGGER.info("[EtherLink] Signal sent successfully.");
            } catch (Exception e) {
                LOGGER.error("[EtherLink] Error sending signal: " + e.getMessage(), e);
            }
        } else {
            LOGGER.warn("[EtherLink] Tried to send signal, but no active connection.");
        }
    }
}
}
