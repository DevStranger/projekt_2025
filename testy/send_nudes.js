import { Selector, RequestMock } from 'testcafe';

const sendNotesMock = RequestMock()
    .onRequestTo('http://localhost:5000/send_notes')
    .respond({ message: 'Notatki wysłane pomyślnie!' }, 200, { 'Access-Control-Allow-Origin': '*' });

fixture `Test wysyłania notatek`
    .page `http://localhost:5000/my_notes`
    .requestHooks(sendNotesMock);

test('Wysyłanie notatek na adres chlipciaa@gmail.com', async t => {
    await t.setNativeDialogHandler(() => true);

    const noteSearchBox = Selector('#noteSearchBox').with({ timeout: 5000 });
    await t.expect(noteSearchBox.visible).ok('Pole wyszukiwania nie jest widoczne');
    await t.selectText(noteSearchBox).pressKey('delete');

    const noteList = Selector('.notes-list').with({ timeout: 5000 });
    const firstNote = noteList.find('li').nth(0);
    const firstNoteRadio = firstNote.find('input[type="radio"][name="note_checkbox"]');
    await t.scrollIntoView(firstNote);
    await t
        .expect(noteList.childElementCount).gt(0, 'Brak wyników wyszukiwania')
        .expect(firstNote.visible).ok('Pierwsza notatka (li) nie jest widoczna')
        .expect(firstNoteRadio.exists).ok('Radio button nie istnieje dla pierwszej notatki');
    await t.click(firstNoteRadio)
        .expect(firstNoteRadio.checked).ok('Radio button nie został zaznaczony');

    const newEmailInput = Selector('#newEmail');
    await t.expect(newEmailInput.visible).ok('Pole do wpisania e-maila nie jest widoczne')
        .typeText(newEmailInput, 'chlipciaa@gmail.com', { replace: true })
        .expect(newEmailInput.value).eql('chlipciaa@gmail.com', 'Wprowadzony adres e-mail jest niepoprawny');

    const addEmailButton = Selector('.add-email-button');
    await t.expect(addEmailButton.visible).ok('Przycisk "Dodaj e-mail" nie jest widoczny')
        .click(addEmailButton);

    await t.wait(1000);

    const emailList = Selector('.email-list').with({ timeout: 5000 });
    const newEmailCheckbox = emailList.find('input[type="checkbox"][name="email_checkbox"]').withAttribute('value', 'chlipciaa@gmail.com');
    await t.expect(newEmailCheckbox.exists).ok('Nowy adres e-mail nie pojawił się na liście')
        .click(newEmailCheckbox)
        .expect(newEmailCheckbox.checked).ok('Checkbox nowego adresu e-mail nie został zaznaczony');

    const sendButton = Selector('#sendButton');
    await t.expect(sendButton.visible).ok('Przycisk "Wyślij" nie jest widoczny')
        .click(sendButton);

    await t.wait(5000);

    const dialogHistory = await t.getNativeDialogHistory();
    await t.expect(dialogHistory[0].text).eql('Notatki zostały pomyślnie wysłane!', 'Brak potwierdzenia wysyłki notatek');
});
