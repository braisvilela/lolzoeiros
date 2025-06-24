document.addEventListener("DOMContentLoaded", () => {
    const players = [
        { name: "The Last Dance#GYN", soloq: "GOLD I", flex: "Sem rank" },
        { name: "DISC LOLZEIROS#DISC", soloq: "GOLD I", flex: "Sem rank" },
        { name: "Hand of Noxus#Br01", soloq: "DIAMOND IV", flex: "PLATINUM II" },
        { name: "Fodão#GYN1", soloq: "DIAMOND I", flex: "MASTER I" },
        { name: "Fodão#GYN3", soloq: "EMERALD IV", flex: "Sem rank" },
        { name: "Shadow Uchiha#Carry", soloq: "DIAMOND IV", flex: "GOLD III" },
        { name: "Fodão#GYN4", soloq: "EMERALD IV", flex: "Sem rank" },
        { name: "Fodão#GYN5", soloq: "DIAMOND I", flex: "EMERALD I" }
    ];

    const container = document.getElementById("cardContainer");

    players.forEach((player, index) => {
        const card = document.createElement("div");
        card.classList.add("card", "fade-in");

        card.innerHTML = `
            <div class="card-content">
                <h2>${player.name}</h2>
                <div class="rank soloq">SoloQ: ${player.soloq}</div>
                <div class="rank flex">Flex: ${player.flex}</div>
            </div>
        `;

        container.appendChild(card);

        // Adiciona efeito de entrada com delay
        setTimeout(() => {
            card.classList.add("show");
        }, index * 150);
    });
});
