// Xử lý dropdown của avatar
document.getElementById('avatarBtn').addEventListener('click', function (e) {
    e.preventDefault();
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
});

// Ẩn dropdown khi nhấp ra ngoài
document.addEventListener('click', function (e) {
    const avatar = document.getElementById('avatarBtn');
    const dropdown = document.getElementById('dropdownMenu');
    if (!avatar.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
    }
});

// Xử lý lịch và hiển thị tên người dùng khi trang tải
document.addEventListener('DOMContentLoaded', function () {
    // Hiển thị tên người dùng trong feedback
    const feedbackMessage = document.getElementById('feedbackMessage');
    if (currentUser && currentUser !== 'Guest') {
        feedbackMessage.textContent = `Hey ${currentUser}, start getting feedback! Let me tell you how you can use Pronounce.`;
    } else {
        feedbackMessage.textContent = `Hey Guest, start getting feedback! Let me tell you how you can use Pronounce.`;
    }

    // Xử lý lịch
    const calendarTable = document.getElementById('calendar-table').getElementsByTagName('tbody')[0];
    const currentMonthYear = document.getElementById('current-month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    function renderCalendar(month, year) {
        calendarTable.innerHTML = '';
        // Sử dụng 'en-US' để hiển thị tháng bằng tiếng Anh
        currentMonthYear.textContent = `${new Date(year, month).toLocaleString('en-US', { month: 'long' })} ${year}`;

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
});