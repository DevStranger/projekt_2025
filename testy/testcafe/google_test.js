import { Selector, ClientFunction } from 'testcafe';

fixture `Google Calendar Integration Test with Simulated OAuth Callback`
    .page `http://127.0.0.1:5000/my_google_calendar`;

const simulateCallback = ClientFunction(() => {
    window.location.href = 'http://127.0.0.1:5000/google-calendar/callback?state=testState&code=TEST_CODE&scope=https://www.googleapis.com/auth/calendar.readonly';
});

const getLocation = ClientFunction(() => document.location.href);

test('Simulate Google Calendar login and callback', async t => {
    const loadEventsButton = Selector('#loadEventsBtn');
    const loginButton = Selector('#loginGoogleBtn');

    await t.setNativeDialogHandler(() => true);
    await t.click(loadEventsButton);

    await t
        .expect(loginButton.exists)
        .ok('Przycisk logowania do Google nie został znaleziony.')
        .click(loginButton);

    await simulateCallback();

    await t
        .expect(getLocation()).contains('/google-calendar/callback', 'Nie znaleziono przekierowania do callbacku.')
        .expect(getLocation()).match(/code=TEST_CODE/, 'Parametr code nie został przekazany poprawnie.');
});
