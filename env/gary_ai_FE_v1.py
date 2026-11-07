// similar html by AI - only upload data for accurate pH value //

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>pH Strip Analyzer - Photo & Gliding Interface</title>
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
        display: flex;
        justify-content: center;
    }
    .container {
        width: 100%;
        max-width: 440px;
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        box-sizing: border-box;
    }
    h1 {
        font-size: 22px;
        font-weight: 800;
        color: #1e293b;
        margin: 0 0 4px 0;
    }
    p.subtitle {
        font-size: 13px;
        color: #64748b;
        margin: 0 0 16px 0;
    }

    /* Mode Switcher Tabs */
    .tab-group {
        display: flex;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .tab-btn {
        flex: 1;
        padding: 8px 12px;
        border: none;
        background: transparent;
        font-size: 13px;
        font-weight: 700;
        color: #64748b;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .tab-btn.active {
        background: #ffffff;
        color: #0f172a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Viewport Panels */
    .panel {
        display: none;
    }
    .panel.active {
        display: block;
    }

    /* Camera Viewport */
    .viewport-container {
        position: relative;
        width: 100%;
        height: 260px;
        background: #0f172a;
        border-radius: 12px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    video, img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    #canvas {
        display: none;
    }
    .sample-box {
        position: absolute;
        width: 40px;
        height: 40px;
        border: 2px dashed #00ffcc;
        box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.4);
        pointer-events: none;
        box-sizing: border-box;
    }
    .sample-box::after {
        content: "PAD TARGET";
        position: absolute;
        top: -18px;
        left: 50%;
        transform: translateX(-50%);
        color: #00ffcc;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }

    /* Action Buttons */
    .action-panel {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 12px;
    }
    .btn {
        background: #1e293b;
        color: #ffffff;
        border: none;
        padding: 10px;
        font-weight: 700;
        font-size: 13px;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
    }
    .btn-secondary {
        background: #e2e8f0;
        color: #334155;
    }
    #fileInput {
        display: none;
    }

    /* RGB Gliding Sliders */
    .slider-group {
        margin-bottom: 12px;
    }
    .slider-label-row {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        margin-bottom: 4px;
    }
    input[type="range"] {
        width: 100%;
        margin: 0;
        cursor: pointer;
    }

    /* Active Picked Color Header */
    .color-window {
        width: 100%;
        height: 44px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 12px;
        box-sizing: border-box;
        margin: 16px 0;
        transition: background-color 0.15s ease;
    }
    .color-tag {
        background: rgba(15, 23, 42, 0.85);
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 4px;
        font-family: monospace;
    }

    /* Dynamic Result Card */
    .result-card {
        text-align: center;
        padding-top: 12px;
        border-top: 1px solid #f1f5f9;
    }
    .metric-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }
    .ph-output {
        font-size: 48px;
        font-weight: 900;
        margin: 4px 0;
        transition: color 0.15s ease;
    }
    .unit {
        font-size: 18px;
        font-weight: 500;
        color: #64748b;
    }
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid transparent;
    }
    .delta-info {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 8px;
    }
</style>
</head>
<body>

<div class="container">
    <h1>pH Strip Analyzer</h1>
    <p class="subtitle">Capture photo or fine-tune color sliders</p>

    <!-- Mode Selector Tabs -->
    <div class="tab-group">
        <button class="tab-btn active" onclick="switchMode('photo')">Photo Capture</button>
        <button class="tab-btn" onclick="switchMode('slider')">Manual Gliding</button>
    </div>

    <!-- Panel A: Camera & Image Upload -->
    <div id="photoPanel" class="panel active">
        <div class="viewport-container">
            <video id="webcam" autoplay playsinline></video>
            <img id="uploadedImage" style="display: none;" alt="Uploaded pH Strip">
            <div class="sample-box"></div>
        </div>
        <canvas id="canvas"></canvas>

        <div class="action-panel">
            <button class="btn" id="snapBtn">Analyze Pad</button>
            <button class="btn btn-secondary" onclick="document.getElementById('fileInput').click()">Upload Photo</button>
            <input type="file" id="fileInput" accept="image/*">
        </div>
    </div>

    <!-- Panel B: Manual RGB Gliding Sliders -->
    <div id="sliderPanel" class="panel">
        <div class="slider-group">
            <div class="slider-label-row">
                <span>Red (R)</span>
                <span id="rVal" style="color: #e74c3c;">180</span>
            </div>
            <input type="range" id="sliderR" min="0" max="255" value="180">
        </div>

        <div class="slider-group">
            <div class="slider-label-row">
                <span>Green (G)</span>
                <span id="gVal" style="color: #2ecc71;">100</span>
            </div>
            <input type="range" id="sliderG" min="0" max="255" value="100">
        </div>

        <div class="slider-group">
            <div class="slider-label-row">
                <span>Blue (B)</span>
                <span id="bVal" style="color: #3498db;">80</span>
            </div>
            <input type="range" id="sliderB" min="0" max="255" value="80">
        </div>
    </div>

    <!-- Active Extracted RGB indicator -->
    <div id="colorWindow" class="color-window">
        <span style="font-size: 12px; font-weight: 700; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.6);">Active Color Sample</span>
        <div id="colorTag" class="color-tag">RGB(180, 100, 80)</div>
    </div>

    <!-- Dynamic Result Card -->
    <div class="result-card">
        <div class="metric-label">Matched Calibration Reading</div>
        <div id="phOutput" class="ph-output">-- <span class="unit">pH</span></div>
        <div id="badge" class="badge">Processing...</div>
        <div id="deltaInfo" class="delta-info">Color Distance (&Delta;E): --</div>
    </div>
</div>

<script>
    /**
     * 1. CUSTOM PH CALIBRATION DATASET
     * Insert your empirical photo readings here.
     */
    const CALIBRATION_DATA = [
        { ph: 1.0,  rgb: [238, 48,  40],  label: "Strongly Acidic" },
        { ph: 2.0,  rgb: [243, 98,  45],  label: "Strongly Acidic" },
        { ph: 3.0,  rgb: [246, 138, 48],  label: "Acidic" },
        { ph: 4.0,  rgb: [251, 184, 41],  label: "Acidic" },
        { ph: 5.0,  rgb: [253, 219, 36],  label: "Weakly Acidic" },
        { ph: 6.0,  rgb: [178, 206, 54],  label: "Weakly Acidic" },
        { ph: 7.0,  rgb: [96,  177, 69],  label: "Neutral" },
        { ph: 8.0,  rgb: [37,  154, 88],  label: "Weakly Alkaline" },
        { ph: 9.0,  rgb: [0,   138, 118], label: "Alkaline" },
        { ph: 10.0, rgb: [10,  115, 142], label: "Alkaline" },
        { ph: 11.0, rgb: [34,  84,  144], label: "Strongly Alkaline" },
        { ph: 12.0, rgb: [48,  57,  125], label: "Strongly Alkaline" },
        { ph: 13.0, rgb: [52,  36,  96],  label: "Strongly Alkaline" },
        { ph: 14.0, rgb: [42,  23,  66],  label: "Extremely Alkaline" }
    ];

    /**
     * 2. COLOR SPACE CONVERSION (sRGB -> XYZ -> CIELAB)
     */
    function rgbToLab([r, g, b]) {
        let rN = r / 255, gN = g / 255, bN = b / 255;
        rN = rN > 0.04045 ? Math.pow((rN + 0.055) / 1.055, 2.4) : rN / 12.92;
        gN = gN > 0.04045 ? Math.pow((gN + 0.055) / 1.055, 2.4) : gN / 12.92;
        bN = bN > 0.04045 ? Math.pow((bN + 0.055) / 1.055, 2.4) : bN / 12.92;

        let x = (rN * 0.4124 + gN * 0.3576 + bN * 0.1805) / 0.95047;
        let y = (rN * 0.2126 + gN * 0.7152 + bN * 0.0722) / 1.00000;
        let z = (rN * 0.0193 + gN * 0.1192 + bN * 0.9505) / 1.08883;

        const f = t => t > 0.008856 ? Math.cbrt(t) : (7.787 * t) + (16 / 116);
        const fx = f(x), fy = f(y), fz = f(z);

        return [(116 * fy) - 16, 500 * (fx - fy), 200 * (fy - fz)];
    }

    function deltaE76(lab1, lab2) {
        const dL = lab1[0] - lab2[0], da = lab1[1] - lab2[1], db = lab1[2] - lab2[2];
        return Math.sqrt(dL * dL + da * da + db * db);
    }

    const processedCalibration = CALIBRATION_DATA.map(item => ({
        ...item,
        lab: rgbToLab(item.rgb)
    }));

    function findBestPhMatch(inputRgb) {
        const inputLab = rgbToLab(inputRgb);
        let bestMatch = null;
        let minDistance = Infinity;

        for (const entry of processedCalibration) {
            const distance = deltaE76(inputLab, entry.lab);
            if (distance < minDistance) {
                minDistance = distance;
                bestMatch = entry;
            }
        }
        return { match: bestMatch, deltaE: minDistance };
    }

    /**
     * 3. UI STATE & EXECUTION ROUTER
     */
    let currentMode = 'photo'; // 'photo' or 'slider'
    let isCameraActive = false;

    const webcam = document.getElementById('webcam');
    const uploadedImage = document.getElementById('uploadedImage');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const fileInput = document.getElementById('fileInput');
    const snapBtn = document.getElementById('snapBtn');

    const sliderR = document.getElementById('sliderR');
    const sliderG = document.getElementById('sliderG');
    const sliderB = document.getElementById('sliderB');

    const rValText = document.getElementById('rVal');
    const gValText = document.getElementById('gVal');
    const bValText = document.getElementById('bVal');

    const colorWindow = document.getElementById('colorWindow');
    const colorTag = document.getElementById('colorTag');
    const phOutput = document.getElementById('phOutput');
    const badge = document.getElementById('badge');
    const deltaInfo = document.getElementById('deltaInfo');

    function switchMode(mode) {
        currentMode = mode;
        const tabs = document.querySelectorAll('.tab-btn');
        tabs[0].classList.toggle('active', mode === 'photo');
        tabs[1].classList.toggle('active', mode === 'slider');

        document.getElementById('photoPanel').classList.toggle('active', mode === 'photo');
        document.getElementById('sliderPanel').classList.toggle('active', mode === 'slider');

        if (mode === 'slider') {
            updateFromSliders();
        }
    }

    // Update Result UI Card
    function renderResult(rgb) {
        colorWindow.style.backgroundColor = `rgb(${rgb.join(',')})`;
        colorTag.textContent = `RGB(${rgb.join(',')})`;

        const { match, deltaE } = findBestPhMatch(rgb);
        const refHex = `rgb(${match.rgb.join(',')})`;

        phOutput.innerHTML = `${match.ph.toFixed(1)} <span class="unit">pH</span>`;
        phOutput.style.color = refHex;

        badge.textContent = match.label;
        badge.style.color = refHex;
        badge.style.backgroundColor = `rgba(${match.rgb.join(',')}, 0.12)`;
        badge.style.borderColor = refHex;

        deltaInfo.textContent = `Color Distance (\u0394E): ${deltaE.toFixed(2)}`;
    }

    // Photo extraction logic
    function extractTargetRGB() {
        const sourceElement = isCameraActive ? webcam : uploadedImage;
        const sourceWidth = isCameraActive ? webcam.videoWidth : uploadedImage.naturalWidth;
        const sourceHeight = isCameraActive ? webcam.videoHeight : uploadedImage.naturalHeight;

        if (!sourceWidth || !sourceHeight) return null;

        canvas.width = sourceWidth;
        canvas.height = sourceHeight;
        ctx.drawImage(sourceElement, 0, 0, sourceWidth, sourceHeight);

                const sampleWidth = Math.min(40, sourceWidth);
        const sampleHeight = Math.min(40, sourceHeight);
        const startX = Math.floor((sourceWidth - sampleWidth) / 2);
        const startY = Math.floor((sourceHeight - sampleHeight) / 2);

        const imgData = ctx.getImageData(startX, startY, sampleWidth, sampleHeight).data;
        let r = 0, g = 0, b = 0, total = 0;

        for (let i = 0; i < imgData.length; i += 4) {
            r += imgData[i];
            g += imgData[i + 1];
            b += imgData[i + 2];
            total++;
        }

        return [Math.round(r / total), Math.round(g / total), Math.round(b / total)];
    }

    // Slider gliding handler
    function updateFromSliders() {
        const r = parseInt(sliderR.value, 10);
        const g = parseInt(sliderG.value, 10);
        const b = parseInt(sliderB.value, 10);

        rValText.textContent = r;
        gValText.textContent = g;
        bValText.textContent = b;

        renderResult([r, g, b]);
    }

    // Start Camera
    async function startCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: { ideal: "environment" } }
            });
            webcam.srcObject = stream;
            isCameraActive = true;
        } catch (err) {
            console.warn("Camera access unavailable. Upload photo or use sliders.", err);
        }
    }

    // File input handler
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
                        reader.onload = (event) => {
                uploadedImage.onload = () => {
                    uploadedImage.style.display = 'block';
                    webcam.style.display = 'none';
                    isCameraActive = false;

                    const rgb = extractTargetRGB();
                    if (rgb) renderResult(rgb);
                };
                uploadedImage.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    // Event listeners
    snapBtn.addEventListener('click', () => {
        const rgb = extractTargetRGB();
        if (rgb) {
            // Also sync sliders to extracted photo color for manual fine-tuning
            sliderR.value = rgb[0];
            sliderG.value = rgb[1];
            sliderB.value = rgb[2];
            rValText.textContent = rgb[0];
            gValText.textContent = rgb[1];
            bValText.textContent = rgb[2];

            renderResult(rgb);
        }
    });

    sliderR.addEventListener('input', updateFromSliders);
    sliderG.addEventListener('input', updateFromSliders);
    sliderB.addEventListener('input', updateFromSliders);

    // Initial setup
        window.addEventListener('load', () => {
        startCamera();
        updateFromSliders();
    });
</script>

</body>
</html>
