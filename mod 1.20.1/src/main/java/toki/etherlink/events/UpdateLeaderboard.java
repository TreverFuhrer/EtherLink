// Updated Cobblemon Pokédex Completion Tracker Example (Fabric Mod)

package toki.etherlink.events;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.server.MinecraftServer;
import org.json.JSONObject;
import toki.etherlink.websocket.InitWebSocket;

//import com.cobblemon.mod.common.Cobblemon;
// Use proper Cobblemon imports based on the mod's documentation
//import com.cobblemon.mod.common.api.storage.player.PlayerInstancedDataStoreManager;
//import com.cobblemon.mod.common;


import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class UpdateLeaderboard {
    private final InitWebSocket webSocket;
    private final Map<UUID, Integer> playerPokedexCounts = new ConcurrentHashMap<>();

    public UpdateLeaderboard(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    public void register() {
        ServerLifecycleEvents.SERVER_STARTED.register(this::sendPokedexLeaderboard);
    }

    private void sendPokedexLeaderboard(MinecraftServer server) {
        playerPokedexCounts.clear();
        server.getPlayerManager().getPlayerList().forEach(player -> {
            //Cobblemon.getPokedex;
            //Cobblemon.playerDataManager.getPokedexData(player);
            //UUID playerId = player.getUuid();
            //PlayerPokedex pokedex = PlayerApi.INSTANCE.getPokedex(player);
            //int count = (pokedex != null) ? pokedex.getEntries().size() : 0;
            //layerPokedexCounts.put(playerId, count);
        });

        JSONObject json = new JSONObject();
        json.put("type", "POKEDEX_LEADERBOARD");
        json.put("leaderboard", playerPokedexCounts);
        webSocket.sendSignal(json.toString());
    }
}
