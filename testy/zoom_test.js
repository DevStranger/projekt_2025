import { Selector, ClientFunction } from 'testcafe'; 

fixture('Zoom Login and OAuth Redirection') 
    .page('http://localhost:5000/my_events'); 

test('Simulate Zoom login and verify OAuth redirection', async t => {
    const zoomLoginBtn = Selector('#zoomLoginBtn'); 
  
    await t
        .expect(zoomLoginBtn.exists)
        .ok('Brak przycisku logowania do Zooma')
        .click(zoomLoginBtn); 

    const getLocation = ClientFunction(() => document.location.href); 

    const location = await getLocation();
    await t
        .expect(location.includes('zoom.us/oauth/authorize') || location.includes('zoom.us/signin'))
        .ok('Nie przekierowano do strony logowania Zooma'); 
  
    if (location.includes('zoom.us/signin')) {
        await t
            .expect(location)
            .contains('signin', 'Strona logowania Zooma nie zawiera "signin" w URL');
    } else {

        await t
            .expect(location)
            .contains('response_type=code', 'Brak parametru response_type=code w URL')
            .expect(location)
            .contains('redirect_uri=http://localhost:5000/zoom/callback', 'Brak parametru redirect_uri w URL');
    }
});
