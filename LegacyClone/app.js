const { QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QBoxLayout, FlexDirection, QApplication } = require('@nodegui/nodegui');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = new QApplication(process.argv);
const win = new QMainWindow();
win.setWindowTitle('LegacyClone');
win.resize(800, 640);

const centralWidget = new QWidget();
const layout = new QBoxLayout(FlexDirection.TopToBottom);
centralWidget.setLayout(layout);

const title = new QLabel();
title.setText('<h1>LegacyClone</h1>');
layout.addWidget(title);

const statusLabel = new QLabel();
statusLabel.setText('Status: aguardando ação');
layout.addWidget(statusLabel);

const output = new QTextEdit();
output.setReadOnly(true);
output.setPlaceholderText('Logs e mensagens aparecerão aqui...');
layout.addWidget(output);

const buttonsLayout = new QBoxLayout(FlexDirection.LeftToRight);
const runTriageButton = new QPushButton();
runTriageButton.setText('Run String Triage');
const startServerButton = new QPushButton();
startServerButton.setText('Start Server');
const stopServerButton = new QPushButton();
stopServerButton.setText('Stop Server');
const refreshReportButton = new QPushButton();
refreshReportButton.setText('Refresh Report');
buttonsLayout.addWidget(runTriageButton);
buttonsLayout.addWidget(startServerButton);
buttonsLayout.addWidget(stopServerButton);
buttonsLayout.addWidget(refreshReportButton);
layout.addLayout(buttonsLayout);

const serverPortInput = new QLineEdit();
serverPortInput.setPlaceholderText('80');
serverPortInput.setText('80');
layout.addWidget(new QLabel('Server port:'));
layout.addWidget(serverPortInput);

const hostHint = new QLabel();
hostHint.setText('Hosts: pegajogo.com, www.pegajogo.com, desktop.meusjogosonline.com, www.meusjogosonline.com');
layout.addWidget(hostHint);

win.setCentralWidget(centralWidget);

const projectRoot = path.resolve(__dirname);
const legacyRoot = path.resolve(projectRoot, '..', 'LegacyLabs');
const pythonScriptRoot = path.join(legacyRoot, 'scripts');
const binPath = path.join(legacyRoot, 'bin', 'PegaJogo.exe');
const reportPath = path.join(legacyRoot, 'reports', 'legacy_strings_report.json');
const legacyServerScript = path.join(pythonScriptRoot, 'legacy_local_server.py');
const stringTriageScript = path.join(pythonScriptRoot, 'string_triage.py');

let serverProcess = null;

function log(message) {
  const now = new Date().toISOString();
  output.setText(output.toPlainText() + `[${now}] ${message}\n`);
  output.ensureCursorVisible();
}

function runPythonScript(scriptPath, args = []) {
  const python = process.platform === 'win32' ? 'python' : 'python3';
  const proc = spawn(python, [scriptPath, ...args], { cwd: pythonScriptRoot });

  proc.stdout.on('data', data => log(data.toString().trim()));
  proc.stderr.on('data', data => log(data.toString().trim()));
  proc.on('close', code => log(`Processo finalizado com código ${code}`));
  proc.on('error', err => log(`Falha ao iniciar processo: ${err.message}`));

  return proc;
}

runTriageButton.addEventListener('clicked', () => {
  statusLabel.setText('Status: executando string triage');
  if (!fs.existsSync(stringTriageScript)) {
    log('Não foi possível encontrar string_triage.py');
    return;
  }
  if (!fs.existsSync(binPath)) {
    log('Não foi possível encontrar bin/PegaJogo.exe');
    return;
  }
  runPythonScript(stringTriageScript, [binPath, '--json', reportPath]);
});

startServerButton.addEventListener('clicked', () => {
  statusLabel.setText('Status: iniciando servidor');
  if (!fs.existsSync(legacyServerScript)) {
    log('Não foi possível encontrar legacy_local_server.py');
    return;
  }
  if (serverProcess) {
    log('Servidor já está em execução. Pare-o antes de iniciar outro.');
    return;
  }
  const port = serverPortInput.text().trim() || '80';
  serverProcess = spawn(process.platform === 'win32' ? 'python' : 'python3', [legacyServerScript, '--port', port], {
    cwd: pythonScriptRoot,
    env: process.env
  });

  serverProcess.stdout.on('data', data => log(data.toString().trim()));
  serverProcess.stderr.on('data', data => log(data.toString().trim()));
  serverProcess.on('close', code => {
    log(`Servidor finalizado com código ${code}`);
    serverProcess = null;
    statusLabel.setText('Status: servidor parado');
  });
  serverProcess.on('error', err => log(`Falha ao iniciar servidor: ${err.message}`));
  statusLabel.setText(`Status: servidor iniciado na porta ${port}`);
});

stopServerButton.addEventListener('clicked', () => {
  if (!serverProcess) {
    log('Servidor não está em execução.');
    return;
  }
  serverProcess.kill();
  serverProcess = null;
  statusLabel.setText('Status: servidor parado');
  log('Servidor solicitado a parar.');
});

refreshReportButton.addEventListener('clicked', () => {
  if (!fs.existsSync(reportPath)) {
    log('Relatório não encontrado. Execute primeiro string triage.');
    return;
  }
  try {
    const raw = fs.readFileSync(reportPath, 'utf-8');
    const report = JSON.parse(raw);
    const summary = [];
    summary.push(`URLs: ${report.URLs?.join(', ') || 'nenhum'}`);
    summary.push(`Hosts: ${report.Hosts?.join(', ') || 'nenhum'}`);
    summary.push(`Scripts: ${report.Scripts?.join(', ') || 'nenhum'}`);
    summary.push(`SWF files: ${report.SwfFiles?.join(', ') || 'nenhum'}`);
    output.setText(summary.join('\n'));
    statusLabel.setText('Status: relatório carregado');
  } catch (ex) {
    log(`Erro ao ler relatório: ${ex.message}`);
  }
});

win.show();
app.exec();
