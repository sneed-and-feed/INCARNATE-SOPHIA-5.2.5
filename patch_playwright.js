const fs = require('fs');
const path = 'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\playwright-core\\lib\\mcpBundleImpl\\index.js';
let content = fs.readFileSync(path, 'utf8');
content = content.replace(/https:\/\/api\.openai\.com\/v1\/responses/g, 'http://127.0.0.1:11434/v1/responses');
content = content.replace(/https:\/\/api\.openai\.com\/v1\/chat\/completions/g, 'http://127.0.0.1:11434/v1/chat/completions');
fs.writeFileSync(path, content, 'utf8');
console.log('Patch applied successfully.');
