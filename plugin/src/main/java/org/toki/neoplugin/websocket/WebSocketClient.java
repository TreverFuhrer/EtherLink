package org.toki.neoplugin.websocket;

import java.net.URI;
import org.java_websocket.handshake.ServerHandshake;

public class WebSocketClient extends org.java_websocket.client.WebSocketClient {

    public WebSocketClient(URI socketUri) {
        super(socketUri);
    }

    @Override
    public void onOpen(ServerHandshake arg0) {
        System.out.println("Connected to WebSocket server.");
    }

    @Override // Incoming connection from Bot
    public void onMessage(String message) {
        IncomingConnection.routeConnect(message);
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("Disconnected from WebSocket server: " + reason);
    }

    @Override
    public void onError(Exception ex) {
        ex.printStackTrace();
    }

    /**
     * Connects to the server
     */
    public void connectToServer() {
        try {
            // connectBlocking waits until the connection is established
            this.connectBlocking();
            System.out.println("WebSocket connection established.");
        } catch (InterruptedException e) {
            e.printStackTrace();
            System.out.println("Failed to connect to WebSocket server.");
        }
    }

    /**
     * Disconnects from the server
     */
    public void disconnectFromServer() {
        this.close();
        System.out.println("WebSocket connection closed.");
    }

    // Send connection message to the Bot
    public void connect(org.json.JSONObject json) {
        this.send(json.toString());
    }

}
