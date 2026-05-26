const fs = require('fs');
const path = require('path');

const gamesDir = path.join(__dirname, '../Reference-Flash');
const outputFile = path.join(__dirname, 'assets/data/games.json');

// Garante que o diretório de destino exista
const outputDir = path.dirname(outputFile);
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

/**
 * Escaneia a pasta de jogos recursivamente e retorna uma lista de objetos
 */
function scanGames(dir, gameList = []) {
    if (!fs.existsSync(dir)) return gameList;

    const items = fs.readdirSync(dir);
    items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            scanGames(fullPath, gameList);
        } else if (path.extname(item).toLowerCase() === '.swf') {
            // Caminho relativo a partir da raiz do projeto para o server.js servir corretamente
            const relativePath = '/' + path.relative(path.join(__dirname, '..'), fullPath).replace(/\\/g, '/');
            gameList.push({
                title: path.parse(item).name,
                file: relativePath,
                category: path.basename(dir)
            });
        }
    });
    return gameList;
}

console.log(`🔍 [Catalog] Escaneando jogos em: ${gamesDir}`);
const games = scanGames(gamesDir);
fs.writeFileSync(outputFile, JSON.stringify(games, null, 4));
console.log(`✅ [Catalog] Sucesso! ${games.length} jogos catalogados em: ${outputFile}`);