// Get form and result elements
const form = document.getElementById('interrogationForm');
const resultDiv = document.getElementById('result');
const resetBtn = document.getElementById('resetBtn');

// Handle form submission
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const subject = document.getElementById('subject').value;
    const lessonsPerWeek = document.getElementById('lessonsPerWeek').value;
    const studentsPerLesson = document.getElementById('studentsPerLesson').value;
    
    // Display results
    document.getElementById('resultSubject').textContent = subject;
    document.getElementById('resultLessons').textContent = lessonsPerWeek;
    document.getElementById('resultStudents').textContent = studentsPerLesson;
    
    // Hide form and show result
    form.style.display = 'none';
    resultDiv.classList.remove('hidden');
    
    // Store data for potential future use
    const interrogationData = {
        subject: subject,
        lessonsPerWeek: parseInt(lessonsPerWeek),
        studentsPerLesson: parseInt(studentsPerLesson),
        timestamp: new Date().toISOString()
    };
    
    console.log('Dati interrogazione:', interrogationData);
});

// Handle reset button
resetBtn.addEventListener('click', function() {
    // Reset form
    form.reset();
    
    // Show form and hide result
    form.style.display = 'block';
    resultDiv.classList.add('hidden');
});
