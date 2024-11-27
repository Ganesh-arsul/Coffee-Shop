const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const app = express();

// Middleware to parse JSON data
app.use(bodyParser.json());

// Create a MySQL connection
const db = mysql.createConnection({
    host: 'localhost',  // Default host for XAMPP MySQL
    user: 'root',       // MySQL default user in XAMPP
    password: '',       // MySQL default password is empty
    database: 'cafe_management', // The name of your database
});

// Connect to MySQL
db.connect(err => {
    if (err) {
        console.error('Could not connect to MySQL:', err);
    } else {
        console.log('Connected to MySQL');
    }
});

// POST endpoint to save the order
app.post('/saveOrder', (req, res) => {
    const orderData = req.body;
    console.log("Order received:", orderData);

    // Insert each order item into the MySQL database
    orderData.forEach(item => {
        const query = 'INSERT INTO orders (coffee_name, size, quantity, price, total) VALUES (?, ?, ?, ?, ?)';
        const values = [item.name, item.size, item.quantity, item.price, item.total];

        db.query(query, values, (err, result) => {
            if (err) {
                console.error('Error inserting order:', err);
                return;
            }
            console.log('Order saved to database:', result);
        });
    });

    // Respond with a success message
    res.status(200).send({ message: 'Order saved successfully!' });
});

// Start the server on port 3000
app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});

const cors = require('cors');
app.use(cors());
