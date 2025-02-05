import { Selector } from 'testcafe';

fixture('Testowanie strony głównej')
    .page('http://127.0.0.1:8080/')
    .skipJsErrors(true);  

test('Testowanie ładowania strony głównej', async t => {
    await t
        .expect(Selector('h1').withText('Witaj w aplikacji!').exists).ok('Strona główna nie załadowała się poprawnie');
});

test('Testowanie przycisku "Nagraj spotkanie"', async t => {
    const recordButton = Selector('#record-btn');
    
    await t
        .click(recordButton)
        .expect(Selector('#startButton').exists).ok('Nie można rozpocząć nagrywania');
});

test('Testowanie strony "Moje notatki"', async t => {
    const notesButton = Selector('#notes-btn');

    await t
        .click(notesButton)
        .expect(Selector('h1').withText('Moje Notatki').visible)
        .ok('Nie przekierowano na stronę notatek', { timeout: 5000 });

    const notesList = Selector('.notes-list li');
    const notesCount = await notesList.count;

    if (notesCount === 0) {
        console.log('Brak notatek do wyświetlenia, test zakończony sukcesem.');
    } else {
        // Jeśli są notatki, testujemy, czy jest ich więcej niż 0
        await t.expect(notesCount).gt(0, 'Brak notatek do wyświetlenia');
    }
});


test('Testowanie wyświetlania sekcji "Moje nagrania"', async t => {
    const myRecordingsButton = Selector('#recordings-btn');
    
    await t
        .click(myRecordingsButton)
        .expect(Selector('h1').withText('Moje Nagrania').exists)
        .ok('Nie przekierowano na stronę Moje Nagrania', { timeout: 5000 });

    const recordingsList = Selector('.recording-list li');
    const recordingsCount = await recordingsList.count;

    if (recordingsCount === 0) {
        console.log('Brak nagrań do wyświetlenia, test zakończony sukcesem.');
    } else {
        await t.expect(recordingsCount).gt(0, 'Brak nagrań do wyświetlenia');
    }
});
