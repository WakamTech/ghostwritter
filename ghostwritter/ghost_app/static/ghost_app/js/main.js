document.addEventListener('DOMContentLoaded', function() {
    const startOperationButton = document.getElementById('start-operation-button');
    const operationLog = document.getElementById('operation-log');

    startOperationButton.addEventListener('click', function() {
        operationLog.innerHTML += "<p>Démarrage des opérations...</p>";
        // Simulation d'opérations (à remplacer par la logique réelle)
        simulateOperation(operationLog);
    });

    function simulateOperation(logArea) {
        const operations = [
            "Récupération des configurations...",
            "Lecture du fichier sites_keywords.csv...",
            "Génération de contenu pour https://example.com/article-de-test-1...",
            "Publication de l'article sur WordPress...",
            "Génération de contenu pour https://example.com/page-importante...",
            "Publication de la page sur WordPress...",
            "Opérations terminées.",
        ];

        let delay = 1000; // Délai en millisecondes entre chaque log

        operations.forEach(operation => {
            setTimeout(() => {
                logArea.innerHTML += `<p>${operation}</p>`;
                logArea.scrollTop = logArea.scrollHeight; // Scroll vers le bas automatiquement
            }, delay);
            delay += 1500; // Augmenter le délai pour la prochaine opération
        });
    }
});