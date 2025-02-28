document.getElementById('addDeckBtn').addEventListener('click', function () {
    const modal = document.getElementById('addDeckModal');
    modal.style.display = 'block';
});

document.getElementById('closeAddDeckModal').addEventListener('click', function () {
    const modal = document.getElementById('addDeckModal');
    modal.style.display = 'none';
});

// Xử lý form tạo deck (tự động ẩn modal khi submit thành công)
document.getElementById('createDeckForm').addEventListener('submit', function (e) {
    e.preventDefault();
    // Gửi form (giả sử backend xử lý và reload trang hoặc trả về phản hồi)
    this.submit();
    document.getElementById('addDeckModal').style.display = 'none';
});

// Xử lý nhấp vào deck để hiển thị cards
document.getElementById('deckGrid').addEventListener('click', function (e) {
    const deckBlock = e.target.closest('.deck-block');
    if (deckBlock) {
        const deckId = deckBlock.getAttribute('data-deck-id');
        const deckName = deckBlock.querySelector('h3').textContent.trim(); // Thêm .trim() để loại bỏ khoảng trắng thừa
        showDeckCards(deckId, deckName);
    }
});

function showDeckCards(deckId, deckName) {
    const modal = document.getElementById('deckCardsModal');
    const cardGrid = document.getElementById('cardGrid');
    const deckModalTitle = document.getElementById('deckModalTitle');

    // Validate deckId
    if (!deckId || isNaN(deckId)) { // Kiểm tra deckId hợp lệ
        console.error('Invalid deck ID:', deckId);
        cardGrid.innerHTML = '<p>Invalid deck</p>';
        modal.style.display = 'block';
        return;
    }

    fetch(`/vocabulary/api/cards?deck_id=${deckId}`, {
        method: 'GET',
        credentials: 'include' // Quan trọng: Gửi cookie session
    })
        .then(response => {
            if (response.status === 401) { // Xử lý riêng trường hợp unauthorized
                window.location.href = '/login'; // Redirect đến trang đăng nhập
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data); // Debug log

            // Xử lý dữ liệu trống
            if (!data.cards || data.cards.length === 0) {
                cardGrid.innerHTML = '<p>No cards in this deck yet!</p>';
                return;
            }

            // Xây dựng card grid
            cardGrid.innerHTML = '';
            data.cards.forEach(card => {
                const cardElement = document.createElement('div');
                cardElement.classList.add('card');
                cardElement.innerHTML = `
                <div class="card-front">${escapeHTML(card.front)}</div>
                <div class="card-back">${escapeHTML(card.back)}</div>
            `;
                cardElement.addEventListener('click', () => cardElement.classList.toggle('flipped'));
                cardGrid.appendChild(cardElement);
            });
        })
        .catch(error => {
            console.error('Fetch error:', error);
            cardGrid.innerHTML = '<p>Error loading cards. Check console for details.</p>';
        })
        .finally(() => {
            deckModalTitle.textContent = deckName;
            modal.style.display = 'block'; // Luôn hiển thị modal dù thành công hay thất bại
        });
}

// Hàm escape HTML để phòng XSS
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

document.getElementById('closeDeckCardsModal').addEventListener('click', function () {
    const modal = document.getElementById('deckCardsModal');
    modal.style.display = 'none';
});

document.addEventListener('click', function (e) {
    const addDeckModal = document.getElementById('addDeckModal');
    const deckCardsModal = document.getElementById('deckCardsModal');

    if (e.target === addDeckModal) {
        addDeckModal.style.display = 'none';
    }
    if (e.target === deckCardsModal) {
        deckCardsModal.style.display = 'none';
    }
});