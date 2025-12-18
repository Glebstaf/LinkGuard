<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkGuard v2.0 - Web Edition</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Consolas:wght@400;700&family=Inter:wght@300;400;600&display=swap');

        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a;
            color: #e2e8f0;
            overflow-x: hidden;
        }

        /* Terminal Styles */
        .terminal-font {
            font-family: 'Consolas', 'Courier New', monospace;
        }
        
        .cursor-blink {
            animation: blink 1s step-end infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        /* Toast Notification Styles - Windows 10 Style */
        .toast-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 50;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toast {
            background-color: #1f2937;
            border-left: 4px solid #3b82f6; /* Default Blue */
            width: 360px;
            padding: 16px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            animation: slideIn 0.3s ease-out forwards;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            opacity: 0;
            transform: translateX(100%);
        }

        .toast.safe { border-left-color: #22c55e; }
        .toast.danger { border-left-color: #ef4444; }
        .toast.warning { border-left-color: #f59e0b; }

        @keyframes slideIn {
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes slideOut {
            to { opacity: 0; transform: translateX(100%); }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1e293b;
        }
        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
    </style>
</head>
<body class="h-screen flex flex-col">

    <!-- Navbar -->
    <nav class="bg-slate-900 border-b border-slate-700 p-4 flex justify-between items-center shadow-lg">
        <div class="flex items-center gap-3">
            <i class="fa-solid fa-shield-halved text-blue-500 text-2xl"></i>
            <h1 class="text-xl font-bold tracking-wide">LinkGuard <span class="text-xs bg-blue-600 px-2 py-0.5 rounded text-white font-normal">v2.0 Web</span></h1>
        </div>
        <div class="flex gap-4">
            <button onclick="switchView('dashboard')" id="btn-dashboard" class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-500 transition">
                <i class="fa-solid fa-chart-line mr-2"></i>Монитор
            </button>
            <button onclick="switchView('terminal')" id="btn-terminal" class="px-4 py-2 rounded bg-slate-700 text-slate-300 hover:bg-slate-600 transition">
                <i class="fa-solid fa-terminal mr-2"></i>Менеджер (CLI)
            </button>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-1 relative overflow-hidden">
        
        <!-- DASHBOARD VIEW -->
        <div id="view-dashboard" class="absolute inset-0 p-6 flex flex-col gap-6 transition-all duration-300">
            
            <!-- Status Panel -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Main Status -->
                <div class="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg flex items-center justify-between">
                    <div>
                        <h2 class="text-slate-400 text-sm font-semibold uppercase">Статус защиты</h2>
                        <div id="status-text" class="text-2xl font-bold text-green-400 mt-1">АКТИВНО</div>
                        <p class="text-xs text-slate-500 mt-2">Следит за вводом ссылок...</p>
                    </div>
                    <div id="status-icon" class="h-12 w-12 rounded-full bg-green-900/50 flex items-center justify-center text-green-400 text-2xl animate-pulse">
                        <i class="fa-solid fa-radar"></i>
                    </div>
                </div>

                <!-- Stats -->
                <div class="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
                    <h2 class="text-slate-400 text-sm font-semibold uppercase">Проверено ссылок</h2>
                    <div id="scan-count" class="text-3xl font-bold text-white mt-1">0</div>
                    <div class="flex gap-4 mt-2 text-xs">
                        <span class="text-green-400"><i class="fa-solid fa-check"></i> <span id="safe-count">0</span> Безопасных</span>
                        <span class="text-red-400"><i class="fa-solid fa-triangle-exclamation"></i> <span id="danger-count">0</span> Опасных</span>
                    </div>
                </div>

                <!-- Database Info -->
                <div class="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
                    <h2 class="text-slate-400 text-sm font-semibold uppercase">База доверенных</h2>
                    <div id="whitelist-count" class="text-3xl font-bold text-blue-400 mt-1">0</div>
                    <p class="text-xs text-slate-500 mt-2">Сайтов в белом списке</p>
                </div>
            </div>

            <!-- Scanner Input -->
            <div class="bg-slate-800 p-8 rounded-lg border border-slate-700 shadow-lg text-center">
                <i class="fa-solid fa-magnifying-glass text-4xl text-slate-600 mb-4"></i>
                <h2 class="text-xl font-bold mb-2">Проверка ссылки</h2>
                <p class="text-slate-400 mb-6">Вставьте ссылку ниже или используйте кнопку для сканирования буфера обмена (требуется разрешение)</p>
                
                <div class="max-w-2xl mx-auto flex gap-2">
                    <input type="text" id="link-input" placeholder="https://example.com" class="flex-1 bg-slate-900 border border-slate-600 rounded px-4 py-3 text-white focus:outline-none focus:border-blue-500 font-mono">
                    <button onclick="analyzeInput()" class="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded font-semibold transition">
                        Проверить
                    </button>
                    <button onclick="pasteAndAnalyze()" class="bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded font-semibold transition" title="Вставить из буфера">
                        <i class="fa-regular fa-clipboard"></i>
                    </button>
                </div>
            </div>

            <!-- Recent Logs -->
            <div class="flex-1 bg-slate-900 rounded-lg border border-slate-700 shadow-inner overflow-hidden flex flex-col">
                <div class="bg-slate-800 px-4 py-2 border-b border-slate-700 flex justify-between items-center">
                    <span class="text-xs font-mono text-slate-400">ЖУРНАЛ СОБЫТИЙ</span>
                    <button onclick="clearLogs()" class="text-xs text-slate-400 hover:text-white"><i class="fa-solid fa-trash"></i> Очистить</button>
                </div>
                <div id="log-container" class="flex-1 p-4 overflow-y-auto font-mono text-sm space-y-2">
                    <!-- Logs will appear here -->
                    <div class="text-slate-500 italic">Ожидание действий...</div>
                </div>
            </div>
        </div>

        <!-- TERMINAL (MANAGER) VIEW -->
        <div id="view-terminal" class="absolute inset-0 bg-black p-6 hidden flex flex-col terminal-font">
            <div class="text-green-500 mb-4">
                <pre style="font-size: 10px; line-height: 10px;" class="mb-4 text-green-600">
 _      _       _     _____                     _ 
| |    (_)     | |   / ____|                   | |
| |     _ _ __ | | _| |  __ _   _  __ _ _ __ __| |
| |    | | '_ \| |/ / | |_ | | | |/ _` | '__/ _` |
| |____| | | | |   <| |__| | |_| | (_| | | | (_| |
|______|_|_| |_|_|\_\\_____|\__,_|\__,_|_|  \__,_|
                                v2.0 Web Interface
                </pre>
                <p>Welcome to LinkGuard Manager v2.0</p>
                <p>Type the number of the command and press ENTER.</p>
            </div>

            <div id="terminal-output" class="flex-1 overflow-y-auto mb-4 text-slate-300 whitespace-pre-wrap">
=============================================
  🛡️ LinkGuard Manager v2.0
=============================================
1. Добавить домен в белый список
2. Перезапустить LinkGuard
3. Выключить LinkGuard / Включить LinkGuard
4. Проверить статус работы
5. Показать белый список
6. Очистить терминал
=============================================
            </div>

            <div class="flex items-center text-green-500 border-t border-slate-800 pt-4">
                <span class="mr-2">admin@linkguard:~$</span>
                <input type="text" id="terminal-input" class="bg-transparent border-none outline-none text-green-500 flex-1 terminal-font" autocomplete="off" autofocus>
            </div>
        </div>

    </main>

    <!-- Toast Container -->
    <div id="toast-container" class="toast-container"></div>

    <script>
        // --- CONFIG & STATE ---
        const CONFIG = {
            version: "2.0",
            whitelistKey: "linkguard_whitelist_v2",
            isActive: true
        };

        // Expanded Whitelist Data
        const DEFAULT_WHITELIST = [
            // Банки и финансы
            'sber.ru', 'tinkoff.ru', 'vtb.ru', 'alfabank.ru', 'raiffeisen.ru',
            'rosbank.ru', 'rshb.ru', 'gazprombank.ru', 'mosoblbank.ru', 'psbank.ru',
            'tinkoffinvest.ru', 'qiwi.com', 'yoomoney.ru', 'paypal.com', 'webmoney.ru',
            
            // Госуслуги
            'gosuslugi.ru', 'nalog.ru', 'pfrf.ru', 'fms.gov.ru', 'fgis.gost.ru',
            'mos.ru', 'spb.ru', 'ekaterinburg.ru', 'gorod.mos.ru', 'kremlin.ru',
            
            // Соцсети
            'vk.com', 'ok.ru', 'instagram.com', 'tiktok.com', 'youtube.com',
            'telegram.org', 'whatsapp.com', 'viber.com', 'signal.org', 'x.com', 'twitter.com',
            'facebook.com', 'odnoklassniki.ru', 'pinterest.com', 'reddit.com', 'linkedin.com',
            'discord.com', 'twitch.tv', 'snapchat.com',
            
            // Магазины
            'wildberries.ru', 'ozon.ru', 'yandex.market', 'aliexpress.ru', 'avito.ru',
            'yula.ru', 'cian.ru', 'lamoda.ru', 'sbermegamarket.ru', 'citilink.ru',
            'dns-shop.ru', 'mvideo.ru', 'eldorado.ru', 'leroymerlin.ru', 'amazon.com',
            'ebay.com', 'asos.com', 'shein.com', 'sportmaster.ru', 'detmir.ru',
            
            // Почта/Облако
            'mail.ru', 'yandex.ru', 'gmail.com', 'outlook.com', 'icloud.com',
            'disk.yandex.ru', 'drive.google.com', 'dropbox.com', 'onedrive.com', 'protonmail.com',
            'mega.nz',
            
            // Поиск и IT
            'google.com', 'yandex.com', 'bing.com', 'github.com', 'gitlab.com',
            'stackoverflow.com', 'habr.com', 'vc.ru', 'zen.yandex.ru', 'dzen.ru',
            'yahoo.com', 'duckduckgo.com', 'wikipedia.org', 'w3schools.com', 'mdn.io',
            'mozilla.org', 'microsoft.com', 'apple.com', 'adobe.com', 'jetbrains.com',
            
            // Медиа
            'rutube.ru', 'kinopoisk.ru', 'ivi.ru', 'okko.ru', 'netflix.com',
            'spotify.com', 'music.yandex.ru', 'vk.music', 'deezer.com', 'shazam.com',
            'soundcloud.com', 'steamcommunity.com', 'steampowered.com', 'epicgames.com'
        ];

        let state = {
            whitelist: [],
            scanned: 0,
            safe: 0,
            danger: 0,
            logs: [],
            terminalStep: 'menu' // menu, adding_domain
        };

        // --- INITIALIZATION ---
        function init() {
            // Load whitelist from localStorage or use default
            const stored = localStorage.getItem(CONFIG.whitelistKey);
            if (stored) {
                state.whitelist = JSON.parse(stored);
            } else {
                state.whitelist = [...DEFAULT_WHITELIST];
                saveWhitelist();
            }

            updateStats();
            logToDashboard("Система инициализирована. Версия " + CONFIG.version, "info");
            
            // Terminal input listener
            document.getElementById('terminal-input').addEventListener('keydown', handleTerminalInput);
            
            // Link input listener (Analyze on Enter)
            document.getElementById('link-input').addEventListener('keydown', (e) => {
                if(e.key === 'Enter') analyzeInput();
            });
        }

        function saveWhitelist() {
            localStorage.setItem(CONFIG.whitelistKey, JSON.stringify(state.whitelist));
            updateStats();
        }

        // --- UTILS ---
        function updateStats() {
            document.getElementById('whitelist-count').textContent = state.whitelist.length;
            document.getElementById('scan-count').textContent = state.scanned;
            document.getElementById('safe-count').textContent = state.safe;
            document.getElementById('danger-count').textContent = state.danger;
        }

        function switchView(viewName) {
            const dashboard = document.getElementById('view-dashboard');
            const terminal = document.getElementById('view-terminal');
            const btnDash = document.getElementById('btn-dashboard');
            const btnTerm = document.getElementById('btn-terminal');

            if (viewName === 'dashboard') {
                dashboard.classList.remove('hidden');
                terminal.classList.add('hidden');
                btnDash.classList.remove('bg-slate-700', 'text-slate-300');
                btnDash.classList.add('bg-blue-600', 'text-white');
                btnTerm.classList.remove('bg-blue-600', 'text-white');
                btnTerm.classList.add('bg-slate-700', 'text-slate-300');
            } else {
                dashboard.classList.add('hidden');
                terminal.classList.remove('hidden');
                btnTerm.classList.remove('bg-slate-700', 'text-slate-300');
                btnTerm.classList.add('bg-blue-600', 'text-white');
                btnDash.classList.remove('bg-blue-600', 'text-white');
                btnDash.classList.add('bg-slate-700', 'text-slate-300');
                document.getElementById('terminal-input').focus();
            }
        }

        // --- TOAST NOTIFICATIONS ---
        function showToast(title, message, type = 'info') {
            const container = document.getElementById('toast-container');
            
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            
            let icon = 'fa-circle-info';
            let colorClass = 'text-blue-400';
            
            if (type === 'safe') {
                icon = 'fa-circle-check';
                colorClass = 'text-green-400';
            } else if (type === 'danger') {
                icon = 'fa-triangle-exclamation';
                colorClass = 'text-red-400';
            } else if (type === 'warning') {
                icon = 'fa-circle-exclamation';
                colorClass = 'text-yellow-400';
            }

            toast.innerHTML = `
                <div class="mt-1 ${colorClass} text-xl"><i class="fa-solid ${icon}"></i></div>
                <div>
                    <h4 class="font-bold text-sm text-slate-100">${title}</h4>
                    <p class="text-xs text-slate-400 mt-1">${message}</p>
                </div>
            `;

            container.appendChild(toast);

            // Remove after 5 seconds
            setTimeout(() => {
                toast.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => toast.remove(), 300);
            }, 5000);
        }

        // --- LOGIC: LEVENSHTEIN ---
        function levenshtein(a, b) {
            if (a.length === 0) return b.length;
            if (b.length === 0) return a.length;

            const matrix = [];

            // increment along the first column of each row
            for (let i = 0; i <= b.length; i++) {
                matrix[i] = [i];
            }

            // increment each column in the first row
            for (let j = 0; j <= a.length; j++) {
                matrix[0][j] = j;
            }

            // Fill in the rest of the matrix
            for (let i = 1; i <= b.length; i++) {
                for (let j = 1; j <= a.length; j++) {
                    if (b.charAt(i - 1) == a.charAt(j - 1)) {
                        matrix[i][j] = matrix[i - 1][j - 1];
                    } else {
                        matrix[i][j] = Math.min(
                            matrix[i - 1][j - 1] + 1, // substitution
                            Math.min(
                                matrix[i][j - 1] + 1, // insertion
                                matrix[i - 1][j] + 1  // deletion
                            )
                        );
                    }
                }
            }

            return matrix[b.length][a.length];
        }

        function similarity(s1, s2) {
            let longer = s1;
            let shorter = s2;
            if (s1.length < s2.length) {
                longer = s2;
                shorter = s1;
            }
            const longerLength = longer.length;
            if (longerLength === 0) {
                return 1.0;
            }
            return (longerLength - levenshtein(longer, shorter)) / parseFloat(longerLength);
        }

        // --- LOGIC: LINK ANALYSIS ---
        function extractDomain(url) {
            try {
                url = url.trim().toLowerCase();
                if (!url.startsWith('http')) {
                    url = 'http://' + url;
                }
                const hostname = new URL(url).hostname;
                return hostname.startsWith('www.') ? hostname.slice(4) : hostname;
            } catch (e) {
                return null;
            }
        }

        function analyzeLink(url) {
            if (!CONFIG.isActive) {
                showToast("Система отключена", "Включите LinkGuard в менеджере для проверки.", "warning");
                return;
            }

            const domain = extractDomain(url);
            if (!domain || !domain.includes('.')) {
                logToDashboard(`Некорректная ссылка: ${url}`, "warning");
                showToast("Ошибка", "Текст не похож на ссылку.", "warning");
                return;
            }

            state.scanned++;
            
            // Check Exact Match
            if (state.whitelist.includes(domain)) {
                state.safe++;
                updateStats();
                logToDashboard(`Проверка: ${domain} - БЕЗОПАСНО`, "success");
                showToast("✅ Ссылка безопасна!", `Домен '${domain}' находится в белом списке.`, "safe");
                return;
            }

            const domainName = domain.split('.')[0];
            let isPhishing = false;
            let matchedTrusted = "";

            // Check Similarity (Phishing)
            for (const trusted of state.whitelist) {
                const trustedName = trusted.split('.')[0];
                const sim = similarity(domainName, trustedName);

                if (sim >= 0.75 && domain !== trusted) {
                    isPhishing = true;
                    matchedTrusted = trusted;
                    break;
                }
            }

            if (isPhishing) {
                state.danger++;
                updateStats();
                logToDashboard(`ФИШИНГ: ${domain} (похож на ${matchedTrusted})`, "danger");
                showToast("🚨 ФИШИНГ ОБНАРУЖЕН!", `Похоже на '${matchedTrusted}', но это '${domain}'. Не переходите!`, "danger");
            } else {
                // If not in whitelist and not phishing -> Warning (Unknown site)
                // The prompt says "Notification should appear even if site is safe" -> If it's not detected as phishing, we treat it as potentially safe but with caution, or just safe for this logic.
                // Let's assume passed checks = safe for this simulation.
                state.safe++; // Counting as safe/checked
                updateStats();
                logToDashboard(`Проверка: ${domain} - НЕ В СПИСКЕ`, "warning");
                showToast("✅ Ссылка проверена", `Домен '${domain}' не вызывает подозрений, но его нет в белом списке.`, "safe");
            }
        }

        // --- UI ACTIONS ---
        function analyzeInput() {
            const input = document.getElementById('link-input');
            const val = input.value;
            if (val) {
                analyzeLink(val);
                input.value = '';
            }
        }

        async function pasteAndAnalyze() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('link-input').value = text;
                analyzeLink(text);
            } catch (err) {
                showToast("Ошибка буфера", "Нет доступа к буферу обмена. Вставьте вручную.", "warning");
            }
        }

        function clearLogs() {
            document.getElementById('log-container').innerHTML = '';
            logToDashboard("Журнал очищен.", "info");
        }

        function logToDashboard(msg, type) {
            const container = document.getElementById('log-container');
            const div = document.createElement('div');
            const time = new Date().toLocaleTimeString();
            
            let color = "text-slate-300";
            if (type === 'success') color = "text-green-400";
            if (type === 'danger') color = "text-red-400";
            if (type === 'warning') color = "text-yellow-400";

            div.innerHTML = `<span class="text-slate-500">[${time}]</span> <span class="${color}">${msg}</span>`;
            container.prepend(div);
        }

        // --- TERMINAL LOGIC ---
        function printToTerminal(text) {
            const output = document.getElementById('terminal-output');
            output.innerHTML += `\n${text}`;
            output.scrollTop = output.scrollHeight;
        }

        function handleTerminalInput(e) {
            if (e.key === 'Enter') {
                const input = e.target;
                const val = input.value.trim();
                input.value = '';

                // Echo command
                printToTerminal(`<span class="text-green-300">admin@linkguard:~$ ${val}</span>`);

                if (state.terminalStep === 'menu') {
                    processMenuCommand(val);
                } else if (state.terminalStep === 'adding_domain') {
                    if (val) {
                        if (!state.whitelist.includes(val)) {
                            state.whitelist.push(val);
                            saveWhitelist();
                            printToTerminal(`✅ Домен '${val}' успешно добавлен.`);
                        } else {
                            printToTerminal(`ℹ️ Домен '${val}' уже в списке.`);
                        }
                    } else {
                        printToTerminal(`❌ Отмена добавления.`);
                    }
                    state.terminalStep = 'menu';
                    printMenuPrompt();
                }
            }
        }

        function printMenuPrompt() {
            printToTerminal(`\nВыберите действие (1-6): `);
        }

        function processMenuCommand(cmd) {
            switch(cmd) {
                case '1':
                    state.terminalStep = 'adding_domain';
                    printToTerminal(`Введите домен для добавления (например, mysite.com):`);
                    break;
                case '2':
                    printToTerminal(`🔄 Перезапуск служб...`);
                    setTimeout(() => {
                        state.scanned = 0;
                        state.safe = 0;
                        state.danger = 0;
                        CONFIG.isActive = true;
                        updateStats();
                        clearLogs();
                        logToDashboard("Система перезапущена администратором", "info");
                        printToTerminal(`✅ LinkGuard успешно перезапущен.`);
                        printMenuPrompt();
                    }, 1000);
                    break;
                case '3':
                    CONFIG.isActive = !CONFIG.isActive;
                    if (CONFIG.isActive) {
                         printToTerminal(`✅ LinkGuard ВКЛЮЧЕН.`);
                         document.getElementById('status-text').textContent = "АКТИВНО";
                         document.getElementById('status-text').className = "text-2xl font-bold text-green-400 mt-1";
                         document.getElementById('status-icon').className = "h-12 w-12 rounded-full bg-green-900/50 flex items-center justify-center text-green-400 text-2xl animate-pulse";
                    } else {
                        printToTerminal(`🛑 LinkGuard ВЫКЛЮЧЕН.`);
                        document.getElementById('status-text').textContent = "ОСТАНОВЛЕНО";
                        document.getElementById('status-text').className = "text-2xl font-bold text-red-500 mt-1";
                        document.getElementById('status-icon').className = "h-12 w-12 rounded-full bg-red-900/50 flex items-center justify-center text-red-400 text-2xl";
                    }
                    printMenuPrompt();
                    break;
                case '4':
                    printToTerminal(`\n--- СТАТУС СИСТЕМЫ ---`);
                    printToTerminal(`Состояние: ${CONFIG.isActive ? "🟢 РАБОТАЕТ" : "🔴 ОСТАНОВЛЕН"}`);
                    printToTerminal(`Проверено: ${state.scanned}`);
                    printToTerminal(`Белый список: ${state.whitelist.length} доменов`);
                    printMenuPrompt();
                    break;
                case '5':
                    printToTerminal(`\n--- БЕЛЫЙ СПИСОК (Первые 50) ---`);
                    printToTerminal(state.whitelist.slice(0, 50).join(', '));
                    if (state.whitelist.length > 50) printToTerminal(`... и еще ${state.whitelist.length - 50}`);
                    printMenuPrompt();
                    break;
                case '6':
                    document.getElementById('terminal-output').innerHTML = `=============================================\n  🛡️ LinkGuard Manager v2.0\n=============================================`;
                    printMenuPrompt();
                    break;
                default:
                    printToTerminal(`❌ Неизвестная команда. Введите число от 1 до 6.`);
                    printMenuPrompt();
            }
        }

        // Start
        init();

    </script>
</body>
</html>
