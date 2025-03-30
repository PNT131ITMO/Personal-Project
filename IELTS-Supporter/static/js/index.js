document.getElementById('avatarBtn').addEventListener('click', function (e) {
    e.preventDefault();
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
});

document.addEventListener('click', function (e) {
    const avatar = document.getElementById('avatarBtn');
    const dropdown = document.getElementById('dropdownMenu');
    if (!avatar.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const feedbackMessage = document.getElementById('feedbackMessage');
    if (currentUser && currentUser !== 'Guest') {
        feedbackMessage.textContent = `Hey ${currentUser}, start getting feedback! Let me tell you how you can use Pronounce.`;
    } else {
        feedbackMessage.textContent = `Hey Guest, start getting feedback! Let me tell you how you can use Pronounce.`;
    }

    const calendarTable = document.getElementById('calendar-table').getElementsByTagName('tbody')[0];
    const currentMonthYear = document.getElementById('current-month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    function renderCalendar(month, year) {
        calendarTable.innerHTML = '';
        currentMonthYear.textContent = `${new Date(year, month).toLocaleString('en-US', {month: 'long'})} ${year}`;

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        let date = 1;

        for (let i = 0; i < 6; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td');
                if (i === 0 && j < firstDay) {
                    cell.textContent = '';
                } else if (date > daysInMonth) {
                    break;
                } else {
                    cell.textContent = date;
                    const today = new Date();
                    if (date === today.getDate() &&
                        month === today.getMonth() &&
                        year === today.getFullYear()) {
                        cell.classList.add('today');
                    }
                    date++;
                }
                row.appendChild(cell);
            }
            calendarTable.appendChild(row);
        }
    }

    prevMonthBtn.addEventListener('click', function () {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar(currentMonth, currentYear);
    });

    nextMonthBtn.addEventListener('click', function () {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar(currentMonth, currentYear);
    });

    renderCalendar(currentMonth, currentYear);

    var modal = document.getElementById("myModal");

    var btn = document.querySelector(".calendar-btn");

    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Handle form submission (AJAX)
    document.getElementById("todo-form").addEventListener("submit", function(event) {
        event.preventDefault();

        var taskText = document.getElementById("todo-text").value;
        var taskDate = document.getElementById("todo-date").value;

        fetch('/todo/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `task=${taskText}&due_date=${taskDate}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error adding todo:', data.error);
                alert('Error adding todo: ' + data.error);
            } else {
                console.log('Todo added:', data);
                var todoList = document.querySelector(".plan-list"); // Correct selector
                var newTodoItem = document.createElement("li");
                newTodoItem.textContent = data.task;
                todoList.appendChild(newTodoItem);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('Error adding todo: ' + error);
        })
        .finally(() => {
            modal.style.display = "none"; // Close the modal
        });
    });
});
