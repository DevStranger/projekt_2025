function loadNotes() {
    const notesList = document.getElementById('notes-list');

    fetch('/my_notes')
        .then(response => {
            if (!response.ok) {
                throw new Error('Nie udało się załadować notatek.');
            }
            return response.json(); // Zwraca listę plików w formacie JSON
        })
        .then(notes => {
            if (notes.length === 0) {
                notesList.innerHTML = '<li>Brak notatek do wyświetlenia.</li>';
                return;
            }

            notes.forEach(note => {
                const noteItem = document.createElement('li');
                const noteLink = document.createElement('a');

                noteLink.href = `/notes/${note}`; 
                noteLink.textContent = note; 
                noteLink.download = note; // Dodanie możliwości pobrania pliku

                noteItem.appendChild(noteLink); 
                notesList.appendChild(noteItem);
            });
        })
        .catch(error => {
            notesList.innerHTML = `<li>Błąd: ${error.message}</li>`;
        });
}

document.addEventListener('DOMContentLoaded', loadNotes);
