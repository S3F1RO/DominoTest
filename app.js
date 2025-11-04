let socket = null;

function log(msg) {
    const logEl = document.getElementById("log")
    logEl.textContent += msg + "\n";
}

document.getElementById("connectBtn").addEventListener("click", () => {
    socket = new WebSocket("ws://10.122.7.180:8000");
    socket.onopen = () => {
        document.getElementById("status").textContent = "Connecté ";
        log("Connecté au  serveur WebSocket");
        socket.send(JSON.stringify({type: "hello", payload: "Bonjour serveur"
        }));
};
socket.onmessage = (event) => {
    log("Reçu du serveur : " + event.data);
};

socket.onclose = () => {
    document.getElementById("status").textContent = "Déconnecté ";
    log("Connexion fermée");
};

socket.onerror = (error) => {
    log("Erreur WebSocket : " + error);
};
});