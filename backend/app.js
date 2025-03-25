const express = require('express');
const cors = require('cors');

const app = express();

// Middleware to handle JSON and CORS
app.use(cors());
app.use(express.json());

// Example route for login
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    
    // Dummy credentials for validation
    if (email === 'admin@example.com' && password === 'password') {
        return res.json({
            success: true,
            user: { username: 'admin', email }
        });
    } else {
        return res.json({ success: false, message: 'Invalid credentials' });
    }
});

// Start the server on port 5000
const port = 5000;
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
