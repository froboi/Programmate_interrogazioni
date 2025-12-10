// Store programs in localStorage
let programmi = [];

// Utility function to escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Generate unique ID
function generateId() {
    return Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}

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
        id: generateId(),
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
        <div class="result-item"><strong>Materia:</strong> ${escapeHtml(programma.materia)}</div>
        <div class="result-item"><strong>Frequenza settimanale:</strong> ${programma.frequenza} ${programma.frequenza === 1 ? 'volta' : 'volte'}</div>
        <div class="result-item"><strong>Alunni per lezione:</strong> ${programma.alunni}</div>
        <div class="result-item"><strong>Data creazione:</strong> ${escapeHtml(programma.dataCreazione)}</div>
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
    
    // Clear previous content
    programmiList.innerHTML = '';
    
    // Create program items using DOM manipulation for security
    programmi.forEach(p => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'programma-item';
        
        const h3 = document.createElement('h3');
        h3.textContent = p.materia;
        
        const freqP = document.createElement('p');
        const freqStrong = document.createElement('strong');
        freqStrong.textContent = 'Frequenza: ';
        freqP.appendChild(freqStrong);
        freqP.appendChild(document.createTextNode(`${p.frequenza} ${p.frequenza === 1 ? 'volta' : 'volte'} alla settimana`));
        
        const alunniP = document.createElement('p');
        const alunniStrong = document.createElement('strong');
        alunniStrong.textContent = 'Alunni per lezione: ';
        alunniP.appendChild(alunniStrong);
        alunniP.appendChild(document.createTextNode(p.alunni));
        
        const dataP = document.createElement('p');
        const dataStrong = document.createElement('strong');
        dataStrong.textContent = 'Creato il: ';
        dataP.appendChild(dataStrong);
        dataP.appendChild(document.createTextNode(p.dataCreazione));
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = 'Elimina';
        deleteBtn.addEventListener('click', () => deleteProgramma(p.id));
        
        itemDiv.appendChild(h3);
        itemDiv.appendChild(freqP);
        itemDiv.appendChild(alunniP);
        itemDiv.appendChild(dataP);
        itemDiv.appendChild(deleteBtn);
        
        programmiList.appendChild(itemDiv);
    });
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
    try {
        const saved = localStorage.getItem('programmi');
        if (saved) {
            programmi = JSON.parse(saved);
        }
    } catch (error) {
        console.error('Error loading programs from localStorage:', error);
        programmi = [];
        // Clear corrupted data
        localStorage.removeItem('programmi');
    }
}
