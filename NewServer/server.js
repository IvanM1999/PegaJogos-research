const express = require('express');
const path = require('path');
const mime = require('mime-types');
const fs = require('fs');

const app = express();
const LOG_PATH = path.join(__dirname, 'server_error.log');
const PORT = process.env.PORT || 3000;

const log = (msg) => {
    const entry = `[${new Date().toISOString()}] ${msg}\n`;
    console.log(msg);
    fs.appendFileSync(LOG_PATH, entry);
};
// Define explicitamente o tipo MIME para arquivos .wasm
// Isso é crítico para que o Ruffle (emulador Flash) funcione corretamente.
express.static.mime.define({
    'application/wasm': ['wasm']
});

process.on('uncaughtException', (err) => log(`FATAL ERROR: ${err.message}\n${err.stack}`));

// Configuração explícita de MIME types críticos
mime.types['swf'] = 'application/x-shockwave-flash';
mime.types['wasm'] = 'application/wasm';

// Servir arquivos estáticos com suporte a MIME types corretos
app.use(express.static(__dirname, {
    setHeaders: (res, filePath) => {
        const type = mime.lookup(filePath);
        if (type) res.setHeader('Content-Type', type);
    }
}));

// Servir a pasta de jogos que está fora do diretório do servidor
app.use('/Reference-Flash', express.static(path.join(__dirname, '../Reference-Flash'), {
    setHeaders: (res, filePath) => {
        const type = mime.lookup(filePath);
        if (type) res.setHeader('Content-Type', type);
    }
}));

// Mock de API Legada: intercepta chamadas PHP do app antigo
app.get('/*.php', (req, res) => {
    try {
        res.sendFile(path.join(__dirname, 'assets/data/games.json'));
    } catch (e) {
        log(`Erro ao servir .php: ${e.message}`);
        res.status(500).send('Erro interno');
    }
});

// Rota padrão para servir o index.html (SPA)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Suporte a SPA: Qualquer rota não reconhecida entrega o index.html
app.get('*', (req, res) => {
    try {
        res.sendFile(path.join(__dirname, 'index.html'));
    } catch (e) {
        log(`Erro SPA: ${e.message}`);
        res.status(500).send('Erro interno');
    }
});

app.listen(PORT, () => {
    log(`🚀 Servidor PegaJogo rodando em http://localhost:${PORT}`);
    log(`📡 Suporte a modo legado (.php) e SPA ativado.`);
}).on('error', (e) => log(`Erro ao iniciar servidor: ${e.message}`));