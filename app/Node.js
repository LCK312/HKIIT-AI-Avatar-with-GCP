const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const app = express();

// Database connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Iloveshoto11',
    database: 'MovieWebsite',
});

db.connect((err) => {
    if (err) throw err;
    console.log('MySQL 連接成功！');
});

// middleware
app.use(bodyParser.json());

// API for submitting comments
app.post('/api/reviews', (req, res) => {
    const { movieId, userId, comment } = req.body;
    const sql = 'INSERT INTO reviews (movie_id, user_id, comment) VALUES (?, ?, ?)';
    db.query(sql, [movieId, userId, comment], (err, result) => {
        if (err) {
            console.error('資料庫錯誤：', err);
            return res.status(500).json({ error: '評論提交失敗' });
        }
        res.json({ message: '評論提交成功', reviewId: result.insertId });
    });
});

// API for submitting ratings
app.post('/api/ratings', (req, res) => {
    const { movieId, userId, rating } = req.body;
    const sql = 'INSERT INTO ratings (movie_id, user_id, rating) VALUES (?, ?, ?)';
    db.query(sql, [movieId, userId, rating], (err, result) => {
        if (err) {
            console.error('資料庫錯誤：', err);
            return res.status(500).json({ error: '評分提交失敗' });
        }
        res.json({ message: '評分提交成功', ratingId: result.insertId });
    });
});

// Start server
app.listen(3000, () => {
    console.log('伺服器運行在 http://localhost:3000');
});