@echo off
SETLOCAL EnableDelayedExpansion
TITLE PegaJogo - Sistema de Auto-Recuperacao

SET LOG_FILE=system_startup.log
echo [%DATE% %TIME%] --- Iniciando Processo de Automacao --- > %LOG_FILE%

echo [*] Verificando dependencias...

:: Verifica Node.js
where node >nul 2>1
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Node.js nao encontrado no PATH. Por favor, instale-o. >> %LOG_FILE%
    echo [ERRO] Node.js nao encontrado.
    pause
    exit /b
)

echo [*] Instalando/Atualizando dependencias Node...
call npm install >> %LOG_FILE% 2>&1

echo [*] Gerando catalogo de jogos (games.json)...
node generate_games.js >> %LOG_FILE% 2>&1
if %ERRORLEVEL% neq 0 (
    echo [AVISO] Falha ao gerar games.json. Verifique o log.
)

echo [*] Lancando Servidor com Auto-Recuperacao...
echo [!] O servidor sera reiniciado automaticamente se falhar.
echo [%DATE% %TIME%] --- Servidor Iniciado --- >> %LOG_FILE%

:server_loop
echo [%DATE% %TIME%] Rodando servidor...
node server.js
if %ERRORLEVEL% neq 0 (
    echo [%DATE% %TIME%] O servidor caiu com codigo %ERRORLEVEL%. Reiniciando em 5 segundos... >> %LOG_FILE%
    echo [!] O servidor caiu! Reiniciando...
    timeout /t 5
    goto server_loop
)

echo [%DATE% %TIME%] Servidor finalizado pelo usuario. >> %LOG_FILE%
pause
ENDLOCAL