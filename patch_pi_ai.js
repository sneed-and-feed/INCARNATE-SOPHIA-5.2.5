const fs = require('fs');
const path = require('path');

const targets = [
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\models.generated.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\providers\\openai-responses.js',
    'C:\\Users\\x\\AppData\\Roaming\\npm\\node_modules\\openclaw\\node_modules\\@mariozechner\\pi-ai\\dist\\providers\\openai-codex-responses.js'
];

targets.forEach(filePath => {
    if (fs.existsSync(filePath)) {
        console.log(`Patching ${filePath}...`);
        let content = fs.readFileSync(filePath, 'utf8');
        const originalCount = (content.match(/https:\/\/api\.openai\.com\/v1/g) || []).length;
        content = content.replace(/https:\/\/api\.openai\.com\/v1/g, 'http://127.0.0.1:11434/v1');
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Applied ${originalCount} replacements.`);
    } else {
        console.log(`File not found: ${filePath}`);
    }
});
