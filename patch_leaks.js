const fs = require('fs');
const path = require('path');

const targets = [
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\models.generated.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\providers\\openai-responses.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\providers\\openai-codex-responses.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\providers\\openai-completions.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\utils\\oauth\\openai-codex.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\openai\\client.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\openai\\client.mjs'
];

targets.forEach(filePath => {
    if (fs.existsSync(filePath)) {
        console.log(`Patching ${filePath}...`);
        let content = fs.readFileSync(filePath, 'utf8');

        // Comprehensive replacement: Replace all variations of api.openai.com
        // Capture https://api.openai.com/v1, api.openai.com, etc.
        const originalCount = (content.match(/api\.openai\.com/g) || []).length;

        // Replace full URL with local bridge
        content = content.replace(/https:\/\/api\.openai\.com\/v1/g, 'http://127.0.0.1:11434/v1');
        content = content.replace(/https:\/\/api\.openai\.com/g, 'http://127.0.0.1:11434/v1');
        content = content.replace(/api\.openai\.com/g, '127.0.0.1:11434');

        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Applied ${originalCount} replacements.`);
    } else {
        console.log(`File not found: ${filePath}`);
    }
});
