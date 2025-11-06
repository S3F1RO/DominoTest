let socket = null;

function log(msg) {
    const logEl = document.getElementById("log")
    logEl.textContent += msg + "\n";
}
document.getElementById("disconnectBtn").style.display = "none";

document.getElementById("connectBtn").addEventListener("click", () => {
    socket = new WebSocket("ws://10.122.7.180:8000");
    socket.onopen = () => {
        document.getElementById("status").textContent = "Connecté ";
        document.getElementById("status").style.color="rgb(12,204,12)";
        document.getElementById("connectBtn").style.display="none";
        log("Connecté au serveur WebSocket");
        socket.send(JSON.stringify({type: "hello", payload: "Bonjour serveur"
        }));
};

document.getElementById("chatInput").addEventListener('keydown', function(event) {
    const chatInput = document.getElementById("chatInput")
    if (event.key == 'Enter') {
        socket.send(JSON.stringify(chatInput.value));
    }
});

socket.onmessage = (event) => {
    data = JSON.parse(event.data);
    // Tu dois parse la data que je t'envoie en fonction du type
    // if data['type'] == "update"
    if (data['type'] == "infoS") log(data['dataS']);
    if (data['type'] == "init") {
        const formattedHands = data['hands'].map(d => `(${d[0]}) (${d[1]}) (${d[2]}) (${d[3]}) (${d[4]}) (${d[5]}) (${d[6]})`).join(" ");
        log("Vous êtes le joueur " + data['player']);
        log("Main : " + formattedHands) ;
        log("Table vide : " + data['board']);
        document.getElementById("idPlayer").value = data['player'];
    } 
    if (data['type'] == "update") {
        log("Table : " + data['board']);
        log("Tour du joueur :" + data['current_player'])
    }
    if (data['type'] == "error") log(data['message']);
    if (data['type'] == "win") {
        log("Le joueur : " + data['player'] + " a gagné la partie!")
    }
    if (data['type'] == "game_over") {
        log("Fin du jeu.");
    }

    // if (data['init']) log(data['init'])
    // log("Joueur " + data.player);
    // const hands = data.hands;
    // log("Tu as une main de " + formattedHands);
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
    document.getElementById("joinBtn").style.display = "none";
    document.getElementById("disconnectBtn").style.display ="block";
    
});

document.getElementById("disconnectBtn").addEventListener("click", () => {
    socket.send(JSON.stringify({type: "bye"}));
    document.getElementById("connectBtn").style.display = "block";
    document.getElementById("joinBtn").style.display = "block";
    document.getElementById("disconnectBtn").style.display = "none";
    });




// document.getElementById("domino").addEventListener("keypress", () => {
//     const dominoInput = document.getElementById("domino");
//     alert(dominoInput.value);
//     domino = dominoInput.value;
// });
document.getElementById("sideLBtn").addEventListener("click", () => {
    side = "left";

    const all = document.getElementsByTagName("button");
    for (let btn of all){
        btn.style.color="black"
    }

    const focus = document.getElementById("sideLBtn");
    focus.style.color = "blue";

    console.log(side)
});

document.getElementById("sideRBtn").addEventListener("click", () => {
    side = "right"

    const all = document.getElementsByTagName("button");
    for (let btn of all){
        btn.style.color="black"
    }

    const focus = document.getElementById("sideRBtn");
    focus.style.color = "blue";
    console.log(side)

});
document.getElementById("submitBtn").addEventListener("click", () => {
    const domino = document.getElementById("domino").value;
    const player = document.getElementById("idPlayer").value;
    socket.send(JSON.stringify({type : "play", "domino" : domino, "side" : side, "player" : player}));
});

document.getElementById("passBtn").addEventListener("click", () => {
    const player = document.getElementById("idPlayer").value;

    socket.send(JSON.stringify({type : "pass", player : player}));

});



});