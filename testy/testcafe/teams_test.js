import { Selector, ClientFunction } from 'testcafe';

fixture `Teams Integration Test`
    .page `http://localhost:5000/my_events2`;

test('Simulate Teams login and callback with mocked OAuth', async t => {
    const loginButton = Selector('#loginTeamsBtn');
  
    const overrideLocation = ClientFunction(() => {
        window.history.pushState({}, '', '/teams/callback?state=testState&code=TEST_CODE');
    });

    await t
        .expect(loginButton.exists)
        .ok('Nie znaleziono przycisku logowania do Teams.')
        .click(loginButton);

    await overrideLocation();

    const getLocation = ClientFunction(() => document.location.href);

    await t
        .expect(getLocation()).contains('/teams/callback', 'Nie znaleziono przekierowania do callbacku Teams.')
        .expect(getLocation()).contains('code=TEST_CODE', 'Parametr code nie został przekazany poprawnie.');
});
