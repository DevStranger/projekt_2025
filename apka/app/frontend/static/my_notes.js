function searchItems(type) {
    const input = document.getElementById(type === 'note' ? 'noteSearchBox' : 'emailSearchBox').value.toLowerCase();
    const searchInContent = type === 'note' ? document.getElementById('searchInContent').checked : false;
    const listItems = document.querySelectorAll(`.${type === 'note' ? 'notes-list' : 'email-list'} .list-item`);

    listItems.forEach(item => item.style.display = '');

    if (!searchInContent || type !== 'note') {
        listItems.forEach(item => {
            const text = item.querySelector('span').textContent.toLowerCase();
            if (!text.includes(input)) {
                item.style.display = 'none';
            }
        });
    } else {
        fetch(`/search_docx?query=${encodeURIComponent(input)}`)
            .then(response => response.json())
            .then(matchingNotes => {
                const matchingSet = new Set(matchingNotes);
                listItems.forEach(item => {
                    const text = item.querySelector('span a').textContent;
                    if (!matchingSet.has(text)) {
                        item.style.display = 'none';
                    }
                });
            })
            .catch(error => {
                console.error("Błąd podczas wyszukiwania w treści:", error);
            });
    }
}



function deleteItems(type) {
    if (type !== 'email') return;

    const selectedEmails = Array.from(document.querySelectorAll('input[name="email_checkbox"]:checked')).map(cb => cb.value);

    if (selectedEmails.length === 0) {
        alert("Wybierz co najmniej jeden e-mail do usunięcia.");
        return;
    }

    fetch('/delete_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ emails: selectedEmails }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Błąd: ${data.error}`);
            } else {
                alert("E-maile zostały usunięte.");
                selectedEmails.forEach(email => {
                    const checkbox = document.querySelector(`input[value="${email}"]`);
                    if (checkbox) {
                        const listItem = checkbox.closest('.list-item');
                        listItem.remove();
                    }
                });
            }
        })
        .catch(error => {
            console.error("Błąd podczas usuwania e-maili:", error);
            alert("Wystąpił błąd podczas usuwania e-maili.");
        });
}



        function addEmail() {
    const emailInput = document.getElementById('newEmail').value.trim();

    if (!emailInput) {
        alert("Proszę wprowadzić adres e-mail.");
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput)) {
        alert("Nieprawidłowy adres e-mail!");
        return;
    }

    fetch('/add_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: emailInput }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Błąd: ${data.error}`);
            } else {
                alert("Adres e-mail dodany pomyślnie!");
                const emailList = document.querySelector('.email-list');
                const listItem = document.createElement('li');
                listItem.classList.add('list-item');
                listItem.innerHTML = `
                    <span>${emailInput}</span>
                    <input type="checkbox" value="${emailInput}" name="email_checkbox">
                `;
                emailList.appendChild(listItem);

                document.getElementById('newEmail').value = "";
            }
        })
        .catch(error => {
            console.error("Błąd podczas dodawania e-maila:", error);
            alert("Wystąpił błąd podczas dodawania e-maila.");
        });
}


function sendSelected() {
    const selectedEmails = Array.from(document.querySelectorAll('input[name="email_checkbox"]:checked')).map(cb => cb.value);
    const selectedNotes = Array.from(document.querySelectorAll('input[name="note_checkbox"]:checked')).map(cb => cb.value);

    if (selectedEmails.length === 0 || selectedNotes.length === 0) {
        alert("Wybierz co najmniej jeden adres e-mail oraz jedną notatkę.");
        return;
    }

    fetch('/send_notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ emails: selectedEmails, notes: selectedNotes }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Błąd: ${data.error}`);
            } else {
                alert("Notatki zostały pomyślnie wysłane!");
            }
        })
        .catch(error => {
            console.error("Błąd podczas wysyłania notatek:", error);
            alert("Wystąpił błąd podczas wysyłania notatek.");
        });
}
document.addEventListener("DOMContentLoaded", function () {
    const backToHomeButton = document.querySelector(".back-to-home");

    if (backToHomeButton) {
        backToHomeButton.addEventListener("click", function (event) {
            console.log("Kliknięto przycisk powrotu!");
            event.preventDefault();
            window.location.href = "/";
        });
    }
});
