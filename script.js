document.addEventListener("DOMContentLoaded", () => {
    const names = [
        "Ana#PEEL", "Carlos#Mage", "Lucas#ADC", "Mariana#Jungle", "Pedro#Top", "Giovanna#Support", 
        "Fernando#Tank", "Julia#Carry", "Rafael#Sniper", "Bianca#Heal", "Igor#Assassin", "Camila#Burst",
        "Felipe#Shield", "Larissa#CC", "Vinicius#DPS", "Sofia#Control", "Diego#Bruiser", "Isabela#Fighter",
        "Gustavo#Lethal", "Tatiane#Scout", "Leandro#Bot", "Paula#Kite", "Bruno#Roam", "Yasmin#Charm",
        "Thiago#Gank", "Renata#Split", "Danilo#Engage", "Aline#Zone", "Eduardo#Slow", "Leticia#TrueDmg",
        "Caio#Outplay", "Fernanda#Wave", "Marcelo#Trap", "Priscila#Roamer", "João#CCChain", "Nathalia#Roar",
        "André#Wombo", "Marcia#Peel", "Vitor#Duo", "Helena#AutoFill", "Samuel#Baron", "Bruna#EloHell",
        "Luiz#Backdoor", "Debora#Crit", "Henrique#Meta", "Tatiana#Wintrade", "Rodrigo#Drake", "Sara#SupportGod",
        "Mauricio#Clutch"
    ];

    const ranks = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"];
    const divisions = ["IV", "III", "II", "I"];
    const container = document.getElementById("cardContainer");
    let currentModal = null;

    function getRandomRank() {
        const tier = ranks[Math.floor(Math.random() * ranks.length)];
        const division = divisions[Math.floor(Math.random() * divisions.length)];
        return `${tier} ${division}`;
    }

    function getRandomLevel() {
        return Math.floor(Math.random() * 701) + 100;
    }

    function getRandomWinrate() {
        return (Math.random() * (85 - 30) + 30).toFixed(1) + "%";
    }

    function createCard(name, index) {
        const soloqRank = getRandomRank();
        const flexRank = Math.random() > 0.3 ? getRandomRank() : "Sem rank";
        const level = getRandomLevel();
        const winrate = getRandomWinrate();

        const card = document.createElement("div");
        card.classList.add("card", "fade-in");

        card.innerHTML = `
            <div class="card-content">
                <h2 class="clickable-name">${name}</h2>
                <div class="rank soloq">SoloQ: ${soloqRank}</div>
                <div class="rank flex">Flex: ${flexRank}</div>
                <div class="level">Level: ${level}</div>
                <div class="winrate">Winrate: ${winrate}</div>
            </div>
        `;

        card.addEventListener("click", (e) => {
            if (!e.target.classList.contains("close-btn")) {
                openModal(card);
            }
        });

        setTimeout(() => {
            card.classList.add("show");
        }, index * 100);

        container.appendChild(card);
    }

    function openModal(card) {
        if (currentModal) return;

        const overlay = document.createElement("div");
        overlay.classList.add("card-overlay");

        // Clona o card para o modal
        const modalCard = card.cloneNode(true);
        modalCard.classList.add("modal-card");
        // Garante que o modal card não responda ao hover com escala
        modalCard.classList.remove("fade-in");
        
        // Cria botão fechar
        const closeButton = document.createElement("button");
        closeButton.classList.add("close-btn");
        closeButton.innerText = "X";

        closeButton.addEventListener("click", (e) => {
            e.stopPropagation();
            closeModal();
        });

        // Adiciona botão antes do conteúdo para garantir visibilidade
        modalCard.insertBefore(closeButton, modalCard.firstChild);

        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                closeModal();
            }
        });

        overlay.appendChild(modalCard);
        document.body.appendChild(overlay);
        document.body.classList.add("modal-open");

        currentModal = { overlay };
    }

    function closeModal() {
        if (!currentModal) return;

        currentModal.overlay.remove();
        document.body.classList.remove("modal-open");
        currentModal = null;
    }

    names.forEach((name, index) => createCard(name, index));
});
