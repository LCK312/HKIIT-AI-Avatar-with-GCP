// Submit a comment
document.getElementById('reviewForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form default submission behavior

    const comment = document.getElementById('comment').value;
    const movieId = 1; // 假設當前電影的 ID 是 1
    const userId = 123; // 假設當前用戶的 ID 是 123

    fetch('/api/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movieId, userId, comment }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('評論提交成功：', data);
        alert('評論已提交！');
    })
    .catch(error => {
        console.error('評論提交失敗：', error);
        alert('評論提交失敗，請重試！');
    });
});

// Submit rating
document.getElementById('ratingForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const rating = document.getElementById('rating').value;
    const movieId = 1; // 假設當前電影的 ID 是 1
    const userId = 123; // 假設當前用戶的 ID 是 123

    fetch('/api/ratings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movieId, userId, rating }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('評分提交成功：', data);
        alert('評分已提交！');
    })
    .catch(error => {
        console.error('評分提交失敗：', error);
        alert('評分提交失敗，請重試！');
    });
});