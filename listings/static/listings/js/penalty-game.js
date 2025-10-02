// ========================================
// PENALTY SHOOTER PRO - JAVASCRIPT COMPLET
// Version 2.0 Ultra Premium
// ========================================

// Configuration globale
const CONFIG = {
    VERSION: '2.0.0',
    DEBUG: false,
    HAPTIC_ENABLED: true,
    SOUND_ENABLED: true,
    PARTICLES_ENABLED: true,
    API_ENDPOINTS: {
        CHARACTERS: '/api/characters/',
        DIFFICULTIES: '/api/difficulties/',
        SAVE_SCORE: '/api/save-score/',
        HIGHSCORES: '/api/highscores/',
        STATS: '/api/statistics/',
        PLAYER_STATS: '/api/player-stats/'
    }
};

// État du jeu
let gameState = {
    currentScreen: 'menu',
    selectedCharacter: null,
    selectedDifficulty: null,
    score: 0,
    level: 1,
    attempts: 5,
    combo: 0,
    maxCombo: 0,
    totalShots: 0,
    successfulShots: 0,
    luckyShots: 0,
    perfectShots: 0,
    highShots: 0,
    midShots: 0,
    lowShots: 0,
    isPaused: false,
    isAnimating: false,
    shootPower: 0,
    shootAngle: 0,
    shootHeight: 'mid',
    windSpeed: 0,
    windDirection: 1,
    goalkeeperPosition: { x: 50, y: 50 },
    goalkeeperSpeed: 500,
    obstacles: [],
    defenders: [],
    soundEnabled: localStorage.getItem('soundEnabled') !== 'false',
    hapticEnabled: localStorage.getItem('hapticEnabled') !== 'false',
    particlesEnabled: localStorage.getItem('particlesEnabled') !== 'false'
};

// Sons du jeu
const sounds = {
    kick: new Audio('data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAABAAEAEhEAAA=='),
    goal: new Audio('data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAEgEgAwAA'),
    miss: new Audio('data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAIBAAEBAA='),
    whistle: new Audio('data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAGCAAFEgA=')
};

// ========================================
// FONCTIONS UTILITAIRES
// ========================================

function vibrate(pattern) {
    if (gameState.hapticEnabled && 'vibrate' in navigator) {
        navigator.vibrate(pattern);
    }
}

function playSound(soundName) {
    if (gameState.soundEnabled && sounds[soundName]) {
        sounds[soundName].play().catch(e => console.log('Audio error:', e));
    }
}

function createParticles(x, y, type = 'success') {
    if (!gameState.particlesEnabled) return;

    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle-effect';
        particle.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: ${Math.random() * 10 + 5}px;
            height: ${Math.random() * 10 + 5}px;
            background: ${type === 'success' ? 
                `hsl(${Math.random() * 60 + 100}, 70%, 50%)` : 
                `hsl(${Math.random() * 60}, 70%, 50%)`};
            border-radius: 50%;
            pointer-events: none;
            z-index: 3000;
            animation: particleFly 1s ease-out forwards;
        `;
        
        const angle = (Math.PI * 2 * i) / 10;
        const velocity = Math.random() * 100 + 50;
        particle.style.setProperty('--tx', `${Math.cos(angle) * velocity}px`);
        particle.style.setProperty('--ty', `${Math.sin(angle) * velocity}px`);
        
        document.body.appendChild(particle);
        setTimeout(() => particle.remove(), 1000);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ========================================
// INITIALISATION
// ========================================

async function initGame() {
    console.log('🎮 Penalty Shooter Pro v' + CONFIG.VERSION);
    
    // Masquer le splash screen après animation
    setTimeout(() => {
        const splash = document.getElementById('splashScreen');
        if (splash) splash.style.display = 'none';
    }, 3000);
    
    // Charger les ressources
    await loadGameResources();
    
    // Initialiser les contrôles
    initTouchControls();
    initPWA();
    initKonamiCode();
    
    // Démarrer les animations
    startBackgroundAnimations();
    
    // Vérifier le plein écran
    checkFullscreen();
}

async function loadGameResources() {
    try {
        // Charger les personnages
        const charactersResponse = await fetch(CONFIG.API_ENDPOINTS.CHARACTERS);
        const characters = await charactersResponse.json();
        renderCharacters(characters);
        
        // Charger les difficultés
        const difficultiesResponse = await fetch(CONFIG.API_ENDPOINTS.DIFFICULTIES);
        const difficulties = await difficultiesResponse.json();
        renderDifficulties(difficulties);
        
        console.log('✅ Ressources chargées');
    } catch (error) {
        console.error('❌ Erreur de chargement:', error);
    }
}

// ========================================
// RENDU DES ÉLÉMENTS
// ========================================

function renderCharacters(characters) {
    const container = document.getElementById('characterList');
    container.innerHTML = '';
    
    characters.forEach((char, index) => {
        const card = document.createElement('div');
        card.className = 'characterCard slide-in-up';
        card.style.animationDelay = `${index * 0.1}s`;
        
        const avatarContent = char.image_url ? 
            `<img src="${char.image_url}" alt="${char.name}">` :
            char.emoji;
        
        card.innerHTML = `
            <div class="character-header">
                <div class="character-avatar">
                    ${avatarContent}
                </div>
                <div class="character-info">
                    <h3>${char.name}</h3>
                    <p>${char.description}</p>
                </div>
            </div>
            <div class="character-stats">
                <div class="stat-bar">
                    <label>Puissance</label>
                    <div class="stat-bar-bg">
                        <div class="stat-bar-fill" style="width: ${char.power}%;" data-value="${char.power}"></div>
                    </div>
                </div>
                <div class="stat-bar">
                    <label>Précision</label>
                    <div class="stat-bar-bg">
                        <div class="stat-bar-fill" style="width: ${char.precision}%;" data-value="${char.precision}"></div>
                    </div>
                </div>
                <div class="stat-bar">
                    <label>Chance</label>
                    <div class="stat-bar-bg">
                        <div class="stat-bar-fill" style="width: ${char.luck}%;" data-value="${char.luck}"></div>
                    </div>
                </div>
                <div class="stat-bar">
                    <label>Courbe</label>
                    <div class="stat-bar-bg">
                        <div class="stat-bar-fill" style="width: ${char.curve}%;" data-value="${char.curve}"></div>
                    </div>
                </div>
            </div>
        `;
        
        card.onclick = () => selectCharacter(char);
        container.appendChild(card);
    });
}

function renderDifficulties(difficulties) {
    const container = document.getElementById('difficultyList');
    container.innerHTML = '';
    
    difficulties.forEach((diff, index) => {
        const card = document.createElement('div');
        card.className = `difficultyCard ${diff.difficulty_id} slide-in-up`;
        card.style.animationDelay = `${index * 0.1}s`;
        
        card.innerHTML = `
            <h3>${diff.emoji} ${diff.name}</h3>
            <p>${diff.description}</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">x${diff.score_multiplier}</div>
                    <div class="stat-label">Points</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${diff.goalkeeper_speed}ms</div>
                    <div class="stat-label">Vitesse</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${diff.wind_max}km/h</div>
                    <div class="stat-label">Vent Max</div>
                </div>
            </div>
            ${diff.difficulty_id === 'impossible' ? '<div class="badge gold">DÉFI ULTIME</div>' : ''}
        `;
        
        card.onclick = () => selectDifficulty(diff);
        container.appendChild(card);
    });
}

// ========================================
// NAVIGATION
// ========================================

function showScreen(screenId) {
    document.querySelectorAll('#menuScreen, #gameScreen, #characterSelect, #difficultySelect').forEach(screen => {
        screen.style.display = 'none';
    });
    document.getElementById(screenId).style.display = 'flex';
    gameState.currentScreen = screenId;
}

function showCharacterSelect() {
    vibrate(20);
    showScreen('characterSelect');
}

function showDifficultySelect() {
    vibrate(20);
    showScreen('difficultySelect');
}

function backToMenu() {
    vibrate(20);
    showScreen('menuScreen');
    resetGame();
}

function backToCharacterSelect() {
    vibrate(20);
    showScreen('characterSelect');
}

function selectCharacter(character) {
    gameState.selectedCharacter = character;
    vibrate(50);
    showDifficultySelect();
}

function selectDifficulty(difficulty) {
    gameState.selectedDifficulty = difficulty;
    vibrate(50);
    startGame();
}

// ========================================
// GAMEPLAY
// ========================================

function startGame() {
    console.log('🎮 Démarrage:', gameState.selectedCharacter.name, gameState.selectedDifficulty.name);
    
    resetGameState();
    showScreen('gameScreen');
    setupDifficulty();
    startGoalkeeperAnimation();
    initShootingControls();
    
    playSound('whistle');
    vibrate([100, 50, 100]);
}

function resetGameState() {
    gameState.score = 0;
    gameState.level = 1;
    gameState.attempts = 5;
    gameState.combo = 0;
    gameState.maxCombo = 0;
    gameState.totalShots = 0;
    gameState.successfulShots = 0;
    gameState.isAnimating = false;
    
    updateUI();
}

function setupDifficulty() {
    const diff = gameState.selectedDifficulty;
    
    gameState.goalkeeperSpeed = diff.goalkeeper_speed;
    
    const goalkeeper = document.getElementById('goalkeeper');
    const scale = diff.goalkeeper_size;
    goalkeeper.style.transform = `translate(-50%, -50%) scale(${scale})`;
    
    if (diff.wind_max > 0) {
        document.getElementById('windIndicator').style.display = 'flex';
        gameState.windSpeed = Math.random() * diff.wind_max;
        gameState.windDirection = Math.random() > 0.5 ? 1 : -1;
        updateWindIndicator();
    }
    
    createObstacles(diff.obstacles_count);
    createDefenders(diff.defenders_count);
}

function startGoalkeeperAnimation() {
    const goalkeeper = document.getElementById('goalkeeper');
    const goalArea = document.getElementById('goalArea');
    
    function moveGoalkeeper() {
        if (gameState.isAnimating || gameState.isPaused) return;
        
        const maxX = goalArea.offsetWidth - goalkeeper.offsetWidth;
        const maxY = goalArea.offsetHeight - goalkeeper.offsetHeight;
        
        const newX = Math.random() * maxX;
        const newY = Math.random() * maxY;
        
        goalkeeper.style.left = newX + 'px';
        goalkeeper.style.top = newY + 'px';
        
        setTimeout(moveGoalkeeper, gameState.goalkeeperSpeed);
    }
    
    moveGoalkeeper();
}

function initShootingControls() {
    let angle = 0;
    let angleDirection = 1;
    let powerDirection = 1;
    let power = 0;
    
    function animateAngle() {
        if (gameState.isAnimating || gameState.isPaused) return;
        
        angle += angleDirection * 2;
        if (angle >= 45 || angle <= -45) {
            angleDirection *= -1;
        }
        
        document.getElementById('angleLine').style.transform = `rotate(${angle}deg)`;
        document.getElementById('angleIndicator').textContent = `${Math.abs(angle)}°`;
        
        requestAnimationFrame(animateAngle);
    }
    
    function animatePower() {
        if (gameState.isAnimating || gameState.isPaused) return;
        
        power += powerDirection * 2;
        if (power >= 100 || power <= 0) {
            powerDirection *= -1;
        }
        
        document.getElementById('powerFill').style.width = power + '%';
        
        requestAnimationFrame(animatePower);
    }
    
    animateAngle();
    animatePower();
    
    gameState.shootAngle = angle;
    gameState.shootPower = power;
    
    setInterval(() => {
        gameState.shootAngle = angle;
        gameState.shootPower = power;
    }, 50);
}

function selectHeight(height, event) {
    if (event) event.stopPropagation();
    
    document.querySelectorAll('.heightZone').forEach(zone => {
        zone.classList.remove('selected');
    });
    
    event.target.classList.add('selected');
    gameState.shootHeight = height;
    
    vibrate(30);
}

async function shoot() {
    if (gameState.isAnimating) return;
    
    gameState.isAnimating = true;
    gameState.totalShots++;
    
    // Comptabiliser les hauteurs
    if (gameState.shootHeight === 'high') gameState.highShots++;
    else if (gameState.shootHeight === 'mid') gameState.midShots++;
    else gameState.lowShots++;
    
    vibrate([50, 30, 100]);
    playSound('kick');
    
    const ball = document.getElementById('ball');
    const goalkeeper = document.getElementById('goalkeeper');
    const goalArea = document.getElementById('goalArea');
    
    const angle = gameState.shootAngle;
    const power = gameState.shootPower;
    const height = gameState.shootHeight;
    const character = gameState.selectedCharacter;
    
    // Calculer la position cible
    let targetX = 50 + (angle * 1.5);
    let targetY = height === 'high' ? 20 : height === 'low' ? 70 : 45;
    
    // Ajouter de la courbe
    if (character.curve > 50) {
        targetX += (Math.random() - 0.5) * (character.curve / 10);
    }
    
    // Influence du vent
    if (gameState.windSpeed > 0) {
        targetX += gameState.windDirection * (gameState.windSpeed / 10);
    }
    
    // Ajuster avec la précision
    const precisionOffset = (100 - character.precision) / 20;
    targetX += (Math.random() - 0.5) * precisionOffset;
    targetY += (Math.random() - 0.5) * precisionOffset;
    
    // Limiter aux bords
    targetX = Math.max(5, Math.min(95, targetX));
    targetY = Math.max(5, Math.min(95, targetY));
    
    // Animation du ballon
    ball.classList.add('spinning');
    ball.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    ball.style.left = targetX + '%';
    ball.style.bottom = (100 - targetY) + '%';
    
    // Faire plonger le gardien
    setTimeout(() => {
        goalkeeper.classList.add('diving');
    }, 200);
    
    // Vérifier le résultat
    setTimeout(() => {
        checkGoal(targetX, targetY);
    }, 800);
}

function checkGoal(ballX, ballY) {
    const goalkeeper = document.getElementById('goalkeeper');
    const goalArea = document.getElementById('goalArea');
    
    const goalkeeperRect = goalkeeper.getBoundingClientRect();
    const goalAreaRect = goalArea.getBoundingClientRect();
    
    const goalkeeperX = ((goalkeeperRect.left - goalAreaRect.left) / goalAreaRect.width) * 100;
    const goalkeeperY = ((goalkeeperRect.top - goalAreaRect.top) / goalAreaRect.height) * 100;
    const goalkeeperWidth = (goalkeeperRect.width / goalAreaRect.width) * 100;
    const goalkeeperHeight = (goalkeeperRect.height / goalAreaRect.height) * 100;
    
    const isBlocked = 
        ballX >= goalkeeperX && 
        ballX <= goalkeeperX + goalkeeperWidth &&
        ballY >= goalkeeperY && 
        ballY <= goalkeeperY + goalkeeperHeight;
    
    // Vérifier les obstacles
    let hitObstacle = false;
    gameState.obstacles.forEach(obstacle => {
        if (ballX >= obstacle.x && ballX <= obstacle.x + obstacle.width &&
            ballY >= obstacle.y && ballY <= obstacle.y + obstacle.height) {
            hitObstacle = true;
        }
    });
    
    // Coup de chance
    const luckyShot = Math.random() * 100 < gameState.selectedCharacter.luck;
    
    if ((!isBlocked && !hitObstacle) || luckyShot) {
        goalScored(luckyShot);
    } else {
        goalMissed();
    }
}

function goalScored(isLucky) {
    gameState.successfulShots++;
    gameState.combo++;
    
    if (isLucky) gameState.luckyShots++;
    if (gameState.shootPower > 90) gameState.perfectShots++;
    
    const basePoints = 10;
    const comboBonus = gameState.combo * 5;
    const difficultyMultiplier = gameState.selectedDifficulty.score_multiplier;
    const powerBonus = Math.floor(gameState.shootPower / 10);
    
    const points = Math.floor((basePoints + comboBonus + powerBonus) * difficultyMultiplier);
    gameState.score += points;
    
    if (gameState.combo > gameState.maxCombo) {
        gameState.maxCombo = gameState.combo;
    }
    
    showMessage('BUT ! +' + points, 'goal');
    updateComboCounter();
    createConfetti();
    checkAchievements();
    triggerComboEffects();
    
    playSound('goal');
    vibrate([100, 50, 100, 50, 200]);
    
    if (gameState.successfulShots % 5 === 0) {
        levelUp();
    }
    
    resetBall();
    updateUI();
}

function goalMissed() {
    gameState.combo = 0;
    gameState.attempts--;
    
    showMessage('RATÉ !', 'miss');
    hideComboCounter();
    
    playSound('miss');
    vibrate([200, 100, 200]);
    
    if (gameState.attempts <= 0) {
        gameOver();
    } else {
        resetBall();
        updateUI();
    }
}

function levelUp() {
    gameState.level++;
    gameState.attempts = Math.min(gameState.attempts + 2, 5);
    gameState.goalkeeperSpeed = Math.max(200, gameState.goalkeeperSpeed - 50);
    
    showMessage('NIVEAU ' + gameState.level + ' !', 'goal');
    vibrate([100, 100, 100, 100, 100]);
}

function resetBall() {
    setTimeout(() => {
        const ball = document.getElementById('ball');
        const goalkeeper = document.getElementById('goalkeeper');
        
        ball.classList.remove('spinning');
        ball.style.transition = 'none';
        ball.style.left = '50%';
        ball.style.bottom = '100px';
        
        goalkeeper.classList.remove('diving');
        
        gameState.isAnimating = false;
        
        // Changer le vent
        if (gameState.selectedDifficulty.wind_max > 0) {
            gameState.windSpeed = Math.random() * gameState.selectedDifficulty.wind_max;
            gameState.windDirection = Math.random() > 0.5 ? 1 : -1;
            updateWindIndicator();
        }
    }, 1000);
}

// ========================================
// UI ET AFFICHAGE
// ========================================

function updateUI() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('level').textContent = gameState.level;
    document.getElementById('attempts').textContent = gameState.attempts;
}

function showMessage(text, type = '') {
    const message = document.getElementById('gameMessage');
    message.textContent = text;
    message.className = 'message show ' + type;
    
    setTimeout(() => {
        message.classList.remove('show');
    }, 2000);
}

function updateComboCounter() {
    const counter = document.getElementById('comboCounter');
    const value = document.getElementById('comboValue');
    
    value.textContent = gameState.combo;
    counter.classList.add('show');
    
    if (gameState.combo >= 10) {
        counter.classList.add('high-combo');
    }
}

function hideComboCounter() {
    const counter = document.getElementById('comboCounter');
    counter.classList.remove('show', 'high-combo');
}

function updateWindIndicator() {
    const arrow = document.getElementById('windArrow');
    const speed = document.getElementById('windSpeed');
    
    speed.textContent = Math.round(gameState.windSpeed) + ' km/h';
    arrow.style.transform = `rotate(${gameState.windDirection * 45}deg)`;
}

// ========================================
// ÉLÉMENTS DE JEU
// ========================================

function createObstacles(count) {
    const container = document.getElementById('obstacles');
    container.innerHTML = '';
    gameState.obstacles = [];
    
    for (let i = 0; i < count; i++) {
        const obstacle = document.createElement('div');
        obstacle.className = 'obstacle';
        
        const width = Math.random() * 30 + 20;
        const height = Math.random() * 30 + 20;
        const x = Math.random() * (100 - width);
        const y = Math.random() * (100 - height);
        
        obstacle.style.width = width + '%';
        obstacle.style.height = height + '%';
        obstacle.style.left = x + '%';
        obstacle.style.top = y + '%';
        
        container.appendChild(obstacle);
        gameState.obstacles.push({ x, y, width, height });
    }
}

function createDefenders(count) {
    const goalArea = document.getElementById('goalArea');
    
    for (let i = 0; i < count; i++) {
        const defender = document.createElement('div');
        defender.className = 'defender';
        defender.innerHTML = '🏃';
        defender.style.top = Math.random() * 50 + 25 + '%';
        defender.style.animationDuration = (Math.random() * 2 + 2) + 's';
        
        goalArea.appendChild(defender);
    }
}

function createConfetti() {
    if (!gameState.particlesEnabled) return;
    
    const container = document.createElement('div');
    container.className = 'victory-effect';
    
    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 70%, 50%)`;
        container.appendChild(confetti);
    }
    
    document.body.appendChild(container);
    setTimeout(() => container.remove(), 3000);
}

// ========================================
// FIN DE PARTIE
// ========================================

async function gameOver() {
    gameState.isAnimating = true;
    
    const accuracy = gameState.totalShots > 0 ? 
        Math.round((gameState.successfulShots / gameState.totalShots) * 100) : 0;
    
    await saveScore();
    saveLocalProgress();
    
    const modal = document.getElementById('gameOverModal');
    const content = document.getElementById('gameOverContent');
    
    content.innerHTML = `
        <div class="stats" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
            <div class="stat">
                <div class="stat-value">${gameState.score}</div>
                <div class="stat-label">Score Final</div>
            </div>
            <div class="stat">
                <div class="stat-value">${gameState.level}</div>
                <div class="stat-label">Niveau Atteint</div>
            </div>
            <div class="stat">
                <div class="stat-value">${accuracy}%</div>
                <div class="stat-label">Précision</div>
            </div>
            <div class="stat">
                <div class="stat-value">${gameState.maxCombo}</div>
                <div class="stat-label">Combo Max</div>
            </div>
        </div>
        ${gameState.score > 100 ? '<div class="badge gold">🏆 NOUVELLE PERFORMANCE !</div>' : ''}
    `;
    
    showModal('gameOverModal');
    playSound('whistle');
    vibrate([200, 100, 200, 100, 500]);
}

async function saveScore() {
    const data = {
        character_id: gameState.selectedCharacter.id,
        difficulty_id: gameState.selectedDifficulty.id,
        score: gameState.score,
        level_reached: gameState.level,
        total_shots: gameState.totalShots,
        successful_shots: gameState.successfulShots,
        lucky_shots: gameState.luckyShots,
        max_combo: gameState.maxCombo,
        perfect_shots: gameState.perfectShots,
        high_shots: gameState.highShots,
        mid_shots: gameState.midShots,
        low_shots: gameState.lowShots
    };
    
    try {
        const response = await fetch(CONFIG.API_ENDPOINTS.SAVE_SCORE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('Score sauvegardé:', result);
    } catch (error) {
        console.error('Erreur sauvegarde:', error);
    }
}

// ========================================
// CONTRÔLES DU JEU
// ========================================

function pauseGame() {
    gameState.isPaused = true;
    showModal('pauseModal');
    vibrate(50);
}

function resumeGame() {
    gameState.isPaused = false;
    hideModal('pauseModal');
    vibrate(50);
}

function restartGame() {
    hideModal('gameOverModal');
    startGame();
}

function quitGame() {
    hideModal('pauseModal');
    backToMenu();
}

function resetGame() {
    gameState = {
        ...gameState,
        score: 0,
        level: 1,
        attempts: 5,
        combo: 0,
        isPaused: false,
        isAnimating: false
    };
}

// ========================================
// MENUS ET MODALS
// ========================================

async function showHighScores() {
    vibrate(20);
    
    try {
        const response = await fetch(CONFIG.API_ENDPOINTS.HIGHSCORES);
        const scores = await response.json();
        
        let content = '<div style="max-height: 400px; overflow-y: auto;">';
        scores.forEach((score, index) => {
            content += `
                <div class="score-entry">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 24px; margin-right: 10px;">
                                ${index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '#' + (index + 1)}
                            </span>
                            <strong>${score.player}</strong>
                        </div>
                        <div style="text-align: right;">
                            <div class="stat-value">${score.score} pts</div>
                            <div style="color: rgba(255,255,255,0.6); font-size: 12px;">
                                Niveau ${score.level} • ${score.accuracy}%
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        content += '</div>';
        
        showModalWithContent('Classement', content);
    } catch (error) {
        console.error('Erreur chargement scores:', error);
    }
}

function showControls() {
    vibrate(20);
    
    const content = `
        <div style="padding: 20px;">
            <div style="margin-bottom: 20px;">
                <h3 style="color: #667eea; margin-bottom: 10px;">📱 Contrôles Tactiles</h3>
                <p style="color: rgba(255,255,255,0.8);">• Touchez le bouton TIR pour shooter</p>
                <p style="color: rgba(255,255,255,0.8);">• Sélectionnez la hauteur avant de tirer</p>
                <p style="color: rgba(255,255,255,0.8);">• L'angle et la puissance bougent automatiquement</p>
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="color: #764ba2; margin-bottom: 10px;">🎯 Conseils</h3>
                <p style="color: rgba(255,255,255,0.8);">• Visez les coins pour éviter le gardien</p>
                <p style="color: rgba(255,255,255,0.8);">• Maintenez votre combo pour plus de points</p>
                <p style="color: rgba(255,255,255,0.8);">• Attention au vent dans les niveaux difficiles</p>
            </div>
            <div>
                <h3 style="color: #f093fb; margin-bottom: 10px;">🏆 Objectifs</h3>
                <p style="color: rgba(255,255,255,0.8);">• Marquez 5 buts pour passer au niveau suivant</p>
                <p style="color: rgba(255,255,255,0.8);">• Battez votre meilleur score</p>
                <p style="color: rgba(255,255,255,0.8);">• Débloquez tous les personnages</p>
            </div>
        </div>
    `;
    
    showModalWithContent('Contrôles', content);
}

async function showStats() {
    vibrate(20);
    
    try {
        const response = await fetch(CONFIG.API_ENDPOINTS.STATS);
        const stats = await response.json();
        
        const content = `
            <div style="padding: 20px;">
                <div class="stats" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                    <div class="stat">
                        <div class="stat-value">${stats.total_games}</div>
                        <div class="stat-label">Parties Jouées</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${stats.total_players}</div>
                        <div class="stat-label">Joueurs Actifs</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${Math.round(stats.average_score)}</div>
                        <div class="stat-label">Score Moyen</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${stats.highest_score}</div>
                        <div class="stat-label">Meilleur Score</div>
                    </div>
                </div>
            </div>
        `;
        
        showModalWithContent('Statistiques Globales', content);
    } catch (error) {
        console.error('Erreur chargement stats:', error);
    }
}

async function showProfile() {
    vibrate(20);
    
    try {
        const response = await fetch(CONFIG.API_ENDPOINTS.PLAYER_STATS);
        const stats = await response.json();
        
        if (stats.games_played === 0) {
            showModalWithContent('Mon Profil', '<p style="text-align: center; color: rgba(255,255,255,0.6);">Aucune partie jouée pour le moment</p>');
            return;
        }
        
        const content = `
            <div style="padding: 20px;">
                <div class="stats" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                    <div class="stat">
                        <div class="stat-value">${stats.games_played}</div>
                        <div class="stat-label">Parties</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${Math.round(stats.average_score)}</div>
                        <div class="stat-label">Score Moyen</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${stats.best_score}</div>
                        <div class="stat-label">Meilleur Score</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${stats.overall_accuracy}%</div>
                        <div class="stat-label">Précision</div>
                    </div>
                </div>
            </div>
        `;
        
        showModalWithContent('Mon Profil', content);
    } catch (error) {
        console.error('Erreur chargement profil:', error);
    }
}

function showGameSettings() {
    const content = `
        <div style="padding: 20px;">
            <div style="margin-bottom: 25px;">
                <label style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <span>🔊 Sons</span>
                    <input type="checkbox" ${gameState.soundEnabled ? 'checked' : ''} onchange="toggleSound(this.checked)" style="width: 50px; height: 30px;">
                </label>
                <label style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <span>📳 Vibrations</span>
                    <input type="checkbox" ${gameState.hapticEnabled ? 'checked' : ''} onchange="toggleHaptic(this.checked)" style="width: 50px; height: 30px;">
                </label>
                <label style="display: flex; align-items: center; justify-content: space-between;">
                    <span>✨ Particules</span>
                    <input type="checkbox" ${gameState.particlesEnabled ? 'checked' : ''} onchange="toggleParticles(this.checked)" style="width: 50px; height: 30px;">
                </label>
            </div>
            <button class="btn secondary" onclick="hideAllModals()">Fermer</button>
        </div>
    `;
    
    showModalWithContent('Paramètres', content);
}

// ========================================
// GESTION DES MODALS
// ========================================

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    const overlay = document.getElementById('modalOverlay');
    
    modal.style.display = 'block';
    overlay.classList.add('show');
    
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    const overlay = document.getElementById('modalOverlay');
    
    modal.classList.remove('show');
    overlay.classList.remove('show');
    
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

function hideAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('show');
        modal.style.display = 'none';
    });
    document.getElementById('modalOverlay').classList.remove('show');
}

function showModalWithContent(title, content) {
    const modalHtml = `
        <div class="modal show" id="tempModal" style="display: block;">
            <h2>${title}</h2>
            ${content}
            <button class="btn secondary" onclick="hideTempModal()" style="margin-top: 20px;">Fermer</button>
        </div>
    `;
    
    const tempContainer = document.createElement('div');
    tempContainer.innerHTML = modalHtml;
    document.body.appendChild(tempContainer.firstElementChild);
    
    document.getElementById('modalOverlay').classList.add('show');
}

function hideTempModal() {
    const modal = document.getElementById('tempModal');
    if (modal) {
        modal.remove();
    }
    document.getElementById('modalOverlay').classList.remove('show');
}

// ========================================
// PARAMÈTRES
// ========================================

function toggleSound(enabled) {
    gameState.soundEnabled = enabled;
    localStorage.setItem('soundEnabled', enabled);
    vibrate(20);
}

function toggleHaptic(enabled) {
    gameState.hapticEnabled = enabled;
    localStorage.setItem('hapticEnabled', enabled);
    vibrate(20);
}

function toggleParticles(enabled) {
    gameState.particlesEnabled = enabled;
    localStorage.setItem('particlesEnabled', enabled);
    vibrate(20);
}

// ========================================
// CONTRÔLES TACTILES
// ========================================

function initTouchControls() {
    // Prévenir le zoom
    document.addEventListener('touchstart', (e) => {
        if (e.touches.length > 1) {
            e.preventDefault();
        }
    }, { passive: false });
    
    // Gestion du swipe
    let touchStartY = 0;
    let touchStartX = 0;
    
    document.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
        touchStartX = e.touches[0].clientX;
    });
    
    document.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].clientY;
        const touchEndX = e.changedTouches[0].clientX;
        const diffY = touchStartY - touchEndY;
        const diffX = touchStartX - touchEndX;
        
        // Swipe vers le haut pour tirer
        if (Math.abs(diffY) > Math.abs(diffX) && diffY > 50 && gameState.currentScreen === 'gameScreen') {
            shoot();
        }
    });
}

// ========================================
// FEATURES SPÉCIALES
// ========================================

function initPWA() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(e => console.log('SW registration failed'));
    }
    
    // Installer l'app
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
    });
}

function initKonamiCode() {
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    let konamiIndex = 0;
    
    document.addEventListener('keydown', (e) => {
        if (e.key === konamiCode[konamiIndex]) {
            konamiIndex++;
            if (konamiIndex === konamiCode.length) {
                activateGodMode();
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });
}

function activateGodMode() {
    document.body.classList.add('god-mode');
    showMessage('MODE DIEU ACTIVÉ !', 'goal');
    vibrate([100, 50, 100, 50, 100, 50, 200]);
    gameState.selectedCharacter = {
        ...gameState.selectedCharacter,
        power: 100,
        precision: 100,
        luck: 100,
        curve: 100
    };
}

// ========================================
// ANIMATIONS D'ARRIÈRE-PLAN
// ========================================

function startBackgroundAnimations() {
    // Créer des particules dynamiquement
    setInterval(() => {
        if (Math.random() > 0.7 && gameState.particlesEnabled) {
            const particle = document.createElement('div');
            particle.className = Math.random() > 0.5 ? 'particle star' : 'particle glow';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = '0s';
            particle.style.animationDuration = (15 + Math.random() * 10) + 's';
            document.body.appendChild(particle);
            
            setTimeout(() => particle.remove(), 25000);
        }
    }, 3000);
}

// ========================================
// FONCTIONNALITÉS AVANCÉES
// ========================================

function checkFullscreen() {
    if (!document.fullscreenElement && 'requestFullscreen' in document.documentElement) {
        document.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(e => console.log('Fullscreen failed'));
            }
        }, { once: true });
    }
}

function handleOrientation() {
    if (window.orientation !== undefined) {
        if (Math.abs(window.orientation) === 90) {
            document.body.classList.add('landscape-mode');
        } else {
            document.body.classList.remove('landscape-mode');
        }
    }
}

function saveLocalProgress() {
    const saveData = {
        lastScore: gameState.score,
        bestScore: localStorage.getItem('bestScore') || 0,
        totalGames: (parseInt(localStorage.getItem('totalGames') || 0) + 1),
        lastPlayed: Date.now()
    };
    
    if (gameState.score > saveData.bestScore) {
        saveData.bestScore = gameState.score;
        showMessage('🏆 NOUVEAU RECORD !', 'goal');
    }
    
    Object.keys(saveData).forEach(key => {
        localStorage.setItem(key, saveData[key]);
    });
}

// ========================================
// SYSTÈME D'ACHIEVEMENTS
// ========================================

const achievements = {
    firstGoal: { 
        name: 'Premier But', 
        icon: '⚽', 
        description: 'Marquer votre premier but',
        check: () => gameState.successfulShots === 1
    },
    perfectShot: {
        name: 'Tir Parfait',
        icon: '🎯',
        description: 'Marquer avec 100% de puissance',
        check: () => gameState.shootPower >= 95
    },
    comboMaster: {
        name: 'Maître du Combo',
        icon: '🔥',
        description: 'Atteindre un combo de 10',
        check: () => gameState.combo >= 10
    },
    survivor: {
        name: 'Survivant',
        icon: '💪',
        description: 'Atteindre le niveau 10',
        check: () => gameState.level >= 10
    },
    sniper: {
        name: 'Sniper',
        icon: '🎯',
        description: '100% de précision sur 5 tirs',
        check: () => gameState.totalShots >= 5 && gameState.successfulShots === gameState.totalShots
    }
};

function checkAchievements() {
    Object.keys(achievements).forEach(key => {
        const achievement = achievements[key];
        const unlocked = localStorage.getItem('achievement_' + key);
        
        if (!unlocked && achievement.check()) {
            unlockAchievement(key, achievement);
        }
    });
}

function unlockAchievement(key, achievement) {
    localStorage.setItem('achievement_' + key, 'true');
    
    const notification = document.createElement('div');
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            padding: 20px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 20px 40px rgba(255, 215, 0, 0.6);
            z-index: 5000;
            animation: slideInRight 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        ">
            <span style="font-size: 40px;">${achievement.icon}</span>
            <div>
                <div style="font-weight: 700; font-size: 16px; color: #fff;">Succès Débloqué!</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.9);">${achievement.name}</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification.firstElementChild);
    vibrate([100, 50, 100, 50, 200]);
    playSound('goal');
    
    setTimeout(() => {
        notification.firstElementChild?.remove();
    }, 4000);
}

// ========================================
// EFFETS SPÉCIAUX
// ========================================

function triggerComboEffects() {
    if (gameState.combo >= 5) {
        document.body.style.animation = 'comboShake 0.5s';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 500);
    }
    
    if (gameState.combo >= 10) {
        createFireworks();
    }
}

function createFireworks() {
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#fdcb6e', '#6c5ce7'];
    
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight / 2;
            
            for (let j = 0; j < 20; j++) {
                const particle = document.createElement('div');
                particle.style.cssText = `
                    position: fixed;
                    left: ${x}px;
                    top: ${y}px;
                    width: 4px;
                    height: 4px;
                    background: ${colors[Math.floor(Math.random() * colors.length)]};
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 4000;
                `;
                
                const angle = (Math.PI * 2 * j) / 20;
                const velocity = 100 + Math.random() * 100;
                const lifetime = 1000 + Math.random() * 1000;
                
                particle.animate([
                    { transform: 'translate(0, 0) scale(1)', opacity: 1 },
                    { transform: `translate(${Math.cos(angle) * velocity}px, ${Math.sin(angle) * velocity + 50}px) scale(0)`, opacity: 0 }
                ], {
                    duration: lifetime,
                    easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                });
                
                document.body.appendChild(particle);
                setTimeout(() => particle.remove(), lifetime);
            }
        }, i * 200);
    }
}

// ========================================
// INITIALISATION AU CHARGEMENT
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎮 Chargement du jeu...');
    initGame();
    handleOrientation();
    
    // Anti-triche basique
    let lastScore = 0;
    setInterval(() => {
        if (gameState.score < lastScore) {
            console.warn('⚠️ Tentative de triche détectée');
            gameState.score = lastScore;
        }
        lastScore = gameState.score;
        checkAchievements();
    }, 1000);
    
    console.log('✅ Jeu prêt!');
});

// Gestion de l'orientation
window.addEventListener('orientationchange', handleOrientation);
window.addEventListener('resize', handleOrientation);

// Gestion des erreurs globales
window.addEventListener('error', (e) => {
    console.error('Erreur:', e.error);
    if (CONFIG.DEBUG) {
        alert('Une erreur est survenue: ' + e.message);
    }
});

// Messages de console stylés
console.log('%c⚽ PENALTY SHOOTER PRO ⚽', 'font-size: 30px; font-weight: bold; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px;');
console.log('%cVersion ' + CONFIG.VERSION + ' - Ultra Premium Edition', 'font-size: 16px; color: #667eea;');
console.log('%c🎮 Amusez-vous bien!', 'font-size: 14px; color: #764ba2;');

// Export des fonctions globales pour le HTML
window.showCharacterSelect = showCharacterSelect;
window.showHighScores = showHighScores;
window.showControls = showControls;
window.showStats = showStats;
window.showProfile = showProfile;
window.backToMenu = backToMenu;
window.backToCharacterSelect = backToCharacterSelect;
window.selectHeight = selectHeight;
window.shoot = shoot;
window.pauseGame = pauseGame;
window.resumeGame = resumeGame;
window.restartGame = restartGame;
window.quitGame = quitGame;
window.showGameSettings = showGameSettings;
window.toggleSound = toggleSound;
window.toggleHaptic = toggleHaptic;
window.toggleParticles = toggleParticles;
window.hideAllModals = hideAllModals;
window.hideTempModal = hideTempModal;