function delete_ticket(ticketID) {
    fetch('/delete-ticket',{
        method: 'POST',
        body: JSON.stringify({ ticketID: ticketID}),
    }).then((_res) => {
        window.location.href="/";
    });
}

const selectElement = document.querySelector('#ticketDept');

selectElement.addEventListener('change', (event) => {
  const result = document.querySelector('.result');
  result.textContent = `You like ${event.target.value}`;
});

