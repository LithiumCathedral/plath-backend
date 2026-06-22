const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const app = express();

// Configuration for stable environment routing
const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0'; // Essential for Railway proxy binding

// Middleware to parse incoming form payloads
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/**
 * 1. Catch legacy POST submissions from the generation form
 * Serializes the payload and securely hands it over to the GET route via URL query
 */
app.post('/generate-report', (req, res) => {
    try {
        const { name, dob } = req.body;
        
        if (!name || !dob) {
            return res.status(400).send("Error: Name and Date of Birth fields are required.");
        }

        // Package form attributes into a flat string matrix payload
        const rawPayload = JSON.stringify({ name, dob });
        const encodedPayload = encodeURIComponent(rawPayload);

        // Redirect seamlessly to keep storage completely stateless
        res.redirect(`/report?p=${encodedPayload}`);
    } catch (error) {
        res.status(500).send("Failed to process initialization vector payload.");
    }
});

/**
 * 2. The Stateless Report Generator Route
 * Spawns engine.py to compute vectors and serves the canvas template
 */
app.get('/report', (req, res) => {
    const payload = req.query.p;
    if (!payload) {
        return res.status(400).send('Missing calculation token payload.');
    }

    // Defensive execution of the Python engine module
    const pythonProcess = spawn('python3', [path.join(__dirname, 'engine.py'), payload]);

    let outputData = "";
    let errorData = "";

    pythonProcess.stdout.on('data', (data) => {
        outputData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Engine process exited with code ${code}. Error: ${errorData}`);
            return res.status(500).send("Internal calculation processing engine error.");
        }

        try {
            const result = JSON.parse(outputData);
            if (result.error) {
                return res.status(500).send(`Engine Error Matrix: ${result.error}`);
            }
            
            // Deliver the interactive narrative canvas file straight to the user
            res.sendFile(path.join(__dirname, 'report-template.html'));
        } catch (e) {
            res.status(500).send("Parsing failure on engine output telemetry matrix.");
        }
    });
});

/**
 * 3. System Initialization
 */
app.listen(PORT, HOST, () => {
    console.log(
