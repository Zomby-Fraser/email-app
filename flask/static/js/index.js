async function login(event) {
    event.preventDefault();
    const user = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user=${user}&password=${password}`
    });
    if (response.ok) {
        console.log('Update Successful.');
        window.location.href = '/accounts';
    }
    else {
        console.error('Update failed:', response.status, response.statusText);
    }
}

