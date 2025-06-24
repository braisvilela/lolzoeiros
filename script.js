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

    function getRandomRank() {
        const tier = ranks[Math.floor(Math.random() * ranks.length)];
        const division = divisions[Math.floor(Math.random() * divisions.length)];
        return `${tier} ${division}`;
    }

    function getRandomLevel() {
        return Math.floor(Math.random() * 701) + 100; // Level entre 100 e 800
    }

    function getRandomWinrate() {
        return (Math.random() * (85 - 30) + 30).toFixed(1) + "%"; // 30% a 85%
    }

    names.forEach((name, index) => {
        const soloqRank = getRandomRank();
        const flexRank = Math.random() > 0.3 ? getRandomRank() : "Sem rank"; // 70% chance de ter rank Flex
        const level = getRandomLevel();
        const winrate = getRandomWinrate();

        const card = document.createElement("div");
        card.classList.add("card", "fade-in");

        card.innerHTML = `
            <div class="card-content">
                <h2>${name}</h2>
                <div class="rank soloq">SoloQ: ${soloqRank}</div>
                <div class="rank flex">Flex: ${flexRank}</div>
                <div class="level">Level: ${level}</div>
                <div class="winrate">Winrate: ${winrate}</div>
            </div>
        `;

        container.appendChild(card);

        // Fade-in com delay
        setTimeout(() => {
            card.classList.add("show");
        }, index * 100);
    });
});
