document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    const graphContainer = document.querySelector('.graph-container');
    const daysInMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate();
    const currentMonth = new Date().toLocaleString('default', { month: 'long' });
    document.querySelector('.month-label').textContent = currentMonth;

    const loginDates = JSON.parse(document.getElementById('login-dates').textContent);
    console.log('Login Dates:', loginDates);

    for (let i = 1; i <= daysInMonth; i++) {
        const dateStr = `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        console.log(`Processing date: ${dateStr}`);
        const box = document.createElement('div');
        box.classList.add('graph-box');
        if (loginDates.includes(dateStr)) {
            box.classList.add('active');
            box.setAttribute('data-date', `Active on ${currentMonth} ${i}`);
            console.log(`Active on: ${dateStr}`);
        } else {
            box.classList.add('inactive');
            box.setAttribute('data-date', `Inactive on ${currentMonth} ${i}`);
            console.log(`Inactive on: ${dateStr}`);
        }
        graphContainer.appendChild(box);
    }
});