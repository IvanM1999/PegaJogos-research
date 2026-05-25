// Script de Inicialização do Google Analytics
// Substitua o 'G-XXXXXXXXXX' pelo seu ID de Medição no index.html

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

// O ID de medição deve ser passado dinamicamente ou fixado no HTML
gtag('config', 'G-XXXXXXXXXX');