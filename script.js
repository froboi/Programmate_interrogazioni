// Store programs in localStorage
let programmi = [];

// Load programs from localStorage on page load
window.addEventListener('DOMContentLoaded', () => {
    loadProgrammi();
    displayProgrammi();
});

// Handle form submission
document.getElementById('interrogazioniForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const materia = document.getElementById('materia').value;
    const frequenza = document.getElementById('frequenza').value;
    const alunni = document.getElementById('alunni').value;
    
    // Create program object
    const programma = {
        id: Date.now(),
        materia: materia,
        frequenza: parseInt(frequenza),
        alunni: parseInt(alunni),
        dataCreazione: new Date().toLocaleDateString('it-IT')
    };
    
    // Save to array and localStorage
    programmi.push(programma);
    saveProgrammi();
    
    // Display result
    displayResult(programma);
    
    // Show saved programs
    displayProgrammi();
    
    // Reset form
    document.getElementById('interrogazioniForm').reset();
});

// Handle reset button
document.getElementById('resetBtn').addEventListener('click', () => {
    document.getElementById('result').classList.add('hidden');
    document.getElementById('interrogazioniForm').classList.remove('hidden');
});

// Display result after submission
function displayResult(programma) {
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    
    resultContent.innerHTML = `
        <div class="result-item"><strong>Materia:</strong> ${programma.materia}</div>
        <div class="result-item"><strong>Frequenza settimanale:</strong> ${programma.frequenza} ${programma.frequenza === 1 ? 'volta' : 'volte'}</div>
        <div class="result-item"><strong>Alunni per lezione:</strong> ${programma.alunni}</div>
        <div class="result-item"><strong>Data creazione:</strong> ${programma.dataCreazione}</div>
    `;
    
    resultDiv.classList.remove('hidden');
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

// Display all saved programs
function displayProgrammi() {
    const programmiDiv = document.getElementById('programmiSalvati');
    const programmiList = document.getElementById('programmiList');
    
    if (programmi.length === 0) {
        programmiDiv.classList.add('hidden');
        return;
    }
    
    programmiDiv.classList.remove('hidden');
    
    programmiList.innerHTML = programmi.map(p => `
        <div class="programma-item">
            <h3>${p.materia}</h3>
            <p><strong>Frequenza:</strong> ${p.frequenza} ${p.frequenza === 1 ? 'volta' : 'volte'} alla settimana</p>
            <p><strong>Alunni per lezione:</strong> ${p.alunni}</p>
            <p><strong>Creato il:</strong> ${p.dataCreazione}</p>
            <button class="delete-btn" onclick="deleteProgramma(${p.id})">Elimina</button>
        </div>
    `).join('');
}

// Delete a program
function deleteProgramma(id) {
    if (confirm('Sei sicuro di voler eliminare questo programma?')) {
        programmi = programmi.filter(p => p.id !== id);
        saveProgrammi();
        displayProgrammi();
        
        // Hide result if visible
        document.getElementById('result').classList.add('hidden');
    }
}

// Save programs to localStorage
function saveProgrammi() {
    localStorage.setItem('programmi', JSON.stringify(programmi));
}

// Load programs from localStorage
function loadProgrammi() {
    const saved = localStorage.getItem('programmi');
    if (saved) {
        programmi = JSON.parse(saved);
    }
}
