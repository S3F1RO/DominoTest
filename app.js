let socket = null;

function log(msg) {
    const logEl = document.getElementById("log")
    logEl.textContent += msg + "\n";
}

document.getElementById("connectBtn").addEventListener("click", () => {
    socket = new WebSocket("ws://10.122.7.180:8000");
    socket.onopen = () => {
        document.getElementById("status").textContent = "Connecté ";
        document.getElementById("status").style.color="green"

        log("Connecté au serveur WebSocket");
        socket.send(JSON.stringify({type: "hello", payload: "Bonjour serveur"
        }));
};
socket.onmessage = (event) => {
    data = JSON.parse(event.data);
    log("Joueur " + data.player);
    const hands = data.hands;
    const formattedHands = hands.map(d => `(${d[0]}) (${d[1]}) (${d[2]}) (${d[3]}) (${d[4]}) (${d[5]}) (${d[6]})`).join(" ");
    log("Tu as une main de " + formattedHands);
};

socket.onclose = () => {
    document.getElementById("status").textContent = "Déconnecté ";
    const status = document.getElementById("status");
    status.style.color="red";
    log("Connexion fermée");
};

socket.onerror = (error) => {
    log("Erreur WebSocket : " + error);
};

document.getElementById("joinBtn").addEventListener("click", () => {
    socket.send(JSON.stringify({type: "join"}));
});





document.getElementById("domino").addEventListener("keypress", () => {
    domino = domino.value;
});
document.getElementById("sideLBtn").addEventListener("click", () => {
    side = "left";

    const all = document.getElementById("button");
    all.style.color = "black";

    const focus = document.getElementById("sideBtn");
    focus.style.color = "blue";

    console.log(side)
});

document.getElementById("sideRBtn").addEventListener("click", () => {
    side = "right"

    const all = document.getElementById("button");
    all.style.color="black";

    const focus = document.getElementById("side2Btn");
    focus.style.color="blue";
});
document.getElementById("playBtn").addEventListener("click", () => {
    socket.send(JSON.stringify({type : "play", "domino" : domino, "side" : side}));
    // socket.s
});

document.getElementById("passBtn").addEventListener("click", () => {
    socket.send(JSON.stringify({type : "pass"}))
});

});