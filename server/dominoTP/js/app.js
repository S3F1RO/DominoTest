let socket = null;

function log(msg) {
    const logEl = document.getElementById("log")
    logEl.textContent += msg + "\n";
}
// setTimeout(function() {
//         document.getElementById("log").textContent="";
//     }, 15000);
document.getElementById("disconnectBtn").style.display = "none";

document.getElementById("connectBtn").addEventListener("click", () => {
    socket = new WebSocket("ws://10.122.7.16:8000");
    socket.onopen = () => {
        document.getElementById("status").textContent = "Connecté ";
        document.getElementById("status").style.color="rgb(12,204,12)";
        document.getElementById("connectBtn").style.display="none";
        // document.getElementById("dominoInput").style.display="block";
        // document.getElementById("inputTitle").style.display="block";
        log("Connecté au serveur WebSocket");
        socket.send(JSON.stringify({type: "hello", payload: "Bonjour serveur"
        }));
};


const playerName = document.getElementById("playerName");
document.getElementById("playerName").addEventListener('keydown', function(event) {
    if (event.key == 'Enter') {
        log('Nom enregistré ' + playerName.value);
        socket.send(JSON.stringify({type: "userName", payload: playerName.value}));
        playerName.style.display = 'none';
    }
}); 

const emotes = {
  ":smile:": "https://twemoji.maxcdn.com/v/latest/72x72/1f604.png",
  ":heart:": "https://twemoji.maxcdn.com/v/latest/72x72/2764.png",
  ":thumbsup:": "https://twemoji.maxcdn.com/v/latest/72x72/1f44d.png"
};
document.getElementById("chatInput").addEventListener('keydown', function(event) {
    const chatInput = document.getElementById("chatInput")
    const message = chatInput.value.trim();
    if (event.key == 'Enter') {
        socket.send(JSON.stringify({type: "chat", payload: chatInput.value}));
        document.getElementById("chatInput").value = "";
        // const div = document.createElement('div');
        // const listChats = document.createElement('ul');
        // listChats.id = 'chatList';
        // const li = document.createElement('li');
        // li.innerHTML = '<strong>' + playerName.value + ' : </strong> ' + message;
        // document.getElementById("chatDisplay").append(li);
        // document.getElementById("chatDisplay").scrollTop = document.getElementById("chatDisplay").scrollHeight;
        // document.getElementById("chatInput").value = "";
    }
});


socket.onmessage = (event) => {
    data = JSON.parse(event.data);
    // Tu dois parse la data que je t'envoie en fonction du type
    // if data['type'] == "update"
    if (data['type'] == "infoS") log(data['payload']);
    if (data['type'] == "init") {
        const formattedHands = data['hands'].map(d => `(${d[0]},${d[1]})`).join(" ");
        log("Main : " + formattedHands) ;
        log("Table vide : " + data['board']);
        if (data['your_turn']){
            message = "C'est à vous de jouer";
        }else{
            message = "C'est le tour de l'autre joueur";
        }
        log(message);
        document.getElementById("idPlayer").value = data['player'];
    } 
    if (data['type'] == "update") {
        log("Table : " + data['board'].map(d => `(${d[0]},${d[1]})`).join(" "));
        if (data['your_turn']){
            message = "C'est à vous de jouer";
        }else{
            message = "C'est le tour de l'autre joueur";
        }
        log(message);
        log("Nouvelle Main : " + data['hands'].map(d => `(${d[0]},${d[1]})`).join(" "));
      
    }
    if (data['type'] == "error") log(data['message']);
    if (data['type'] == "game_over") {
        log("Fin du jeu.");
        log( data['winner'] + " a gagné la partie!") // Suly doit process l'info nomDuJoueur
    }
    if (data['type'] == "chat") {
        //Define var 
        const message = (data['message'])
        const div = document.createElement('div');
        const listChats = document.createElement('ul');
        listChats.id = 'chatList';
        const li = document.createElement('li')
        ;
        li.innerHTML = '<strong>' + data['sender'] + ' : </strong> ' + message;
        document.getElementById("chatDisplay").append(li);
        document.getElementById("chatDisplay").scrollTop = document.getElementById("chatDisplay").scrollHeight;
    }
    if (data['type'] == "clear") {
        document.getElementById("log").textContent = "";
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
    document.getElementById("log").textContent = '';
    playerName.style.display = 'block';
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
    focus.style.color = "cyan";

    console.log(side)
});

document.getElementById("sideRBtn").addEventListener("click", () => {
    side = "right"

    const all = document.getElementsByTagName("button");
    for (let btn of all){
        btn.style.color="black"
    }

    const focus = document.getElementById("sideRBtn");
    focus.style.color = "cyan";
    console.log(side)

});
document.getElementById("submitBtn").addEventListener("click", () => {
    const domino = document.getElementById("domino").value;
    const player = document.getElementById("idPlayer").value;
    socket.send(JSON.stringify({type : "play", "domino" : domino, "side" : side, "player" : player}));
    document.getElementById("domino").value = "";
});

document.getElementById("passBtn").addEventListener("click", () => {
    const player = document.getElementById("idPlayer").value;

    socket.send(JSON.stringify({type : "pass", player : player}));

});



});