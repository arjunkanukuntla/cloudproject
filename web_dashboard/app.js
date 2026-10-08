// Interactive Live Dashboard & ESP32 Hardware Simulator Logic

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const badgeText = document.getElementById('status-badge-text');
    const badgeContainer = document.getElementById('system-status-badge');
    const alertLamp = document.getElementById('alert-lamp');
    const onboardLed = document.getElementById('onboard-led');
    
    const metricTotal = document.getElementById('metric-total-buckets');
    const metricPublic = document.getElementById('metric-public-buckets');
    const metricMqtt = document.getElementById('metric-mqtt-messages');
    
    const bucketTableBody = document.getElementById('bucket-table-body');
    const logStream = document.getElementById('mqtt-log-stream');
    
    const btnTriggerAlert = document.getElementById('btn-trigger-alert');
    const btnClearAlert = document.getElementById('btn-clear-alert');
    const btnRunScan = document.getElementById('btn-run-scan');

    let mqttMsgCount = 4;
    let isAlertActive = false;

    // Default Bucket Dataset
    let bucketState = [
        { name: "prod-customer-backups-2026", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false },
        { name: "static-website-assets-cdn", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false },
        { name: "internal-finance-reports", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false }
    ];

    // Initialize UI
    renderBucketTable();

    // Event Listeners
    btnTriggerAlert.addEventListener('click', () => {
        triggerSecurityAlert();
    });

    btnClearAlert.addEventListener('click', () => {
        clearSecurityAlert();
    });

    btnRunScan.addEventListener('click', () => {
        appendLog("[Scanner] Running manual S3 bucket security audit...", "info");
        setTimeout(() => {
            if (isAlertActive) {
                appendLog("[Scanner] Security Audit Complete: PUBLIC S3 BUCKET EXPOSED!", "alert");
            } else {
                appendLog("[Scanner] Security Audit Complete: All buckets secure.", "success");
            }
        }, 500);
    });

    // Tab Navigation Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });

    function triggerSecurityAlert() {
        isAlertActive = true;
        mqttMsgCount++;
        metricMqtt.textContent = mqttMsgCount;

        // Add vulnerable test bucket
        bucketState = [
            { name: "test-vulnerable-lamp-x892a", pab: "DISABLED ⚠️", policy: "PUBLIC READ 🚨", acl: "AllUsers 🚨", isPublic: true },
            { name: "prod-customer-backups-2026", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false },
            { name: "static-website-assets-cdn", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false }
        ];

        renderBucketTable();
        metricTotal.textContent = bucketState.length;
        metricPublic.textContent = "1";

        // Update Lamp Hardware Visualizer
        alertLamp.classList.remove('active-safe');
        alertLamp.classList.add('active-alert');

        // Update Badge
        badgeContainer.className = 'badge badge-alert';
        badgeText.textContent = 'DANGER: PUBLIC S3 DETECTED!';

        // Log MQTT Message
        const timestamp = new Date().toLocaleTimeString();
        appendLog(`[${timestamp}] [MQTT Alert] Topic: cloud/security/alerts`, "alert");
        appendLog(`[payload] {"status": "ALERT", "public_buckets_count": 1, "public_buckets": ["test-vulnerable-lamp-x892a"]}`, "alert");
    }

    function clearSecurityAlert() {
        isAlertActive = false;
        mqttMsgCount++;
        metricMqtt.textContent = mqttMsgCount;

        // Remove vulnerable test bucket
        bucketState = [
            { name: "prod-customer-backups-2026", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false },
            { name: "static-website-assets-cdn", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false },
            { name: "internal-finance-reports", pab: "ENABLED", policy: "SECURE", acl: "PRIVATE", isPublic: false }
        ];

        renderBucketTable();
        metricTotal.textContent = bucketState.length;
        metricPublic.textContent = "0";

        // Update Lamp Hardware Visualizer
        alertLamp.classList.remove('active-alert');
        alertLamp.classList.add('active-safe');

        // Update Badge
        badgeContainer.className = 'badge badge-ok';
        badgeText.textContent = 'SYSTEM SECURE';

        // Log MQTT Message
        const timestamp = new Date().toLocaleTimeString();
        appendLog(`[${timestamp}] [MQTT Status] Topic: cloud/security/alerts`, "success");
        appendLog(`[payload] {"status": "OK", "public_buckets_count": 0, "public_buckets": []}`, "success");
    }

    function renderBucketTable() {
        bucketTableBody.innerHTML = '';
        bucketState.forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${b.name}</strong></td>
                <td>${b.pab}</td>
                <td>${b.policy}</td>
                <td>${b.acl}</td>
                <td>
                    ${b.isPublic 
                        ? '<span class="tag-public">EXPOSED PUBLIC</span>' 
                        : '<span class="tag-secure">SECURE</span>'}
                </td>
            `;
            bucketTableBody.appendChild(tr);
        });
    }

    function appendLog(message, type) {
        const line = document.createElement('div');
        line.className = `log-line log-${type}`;
        line.textContent = message;
        logStream.appendChild(line);
        logStream.scrollTop = logStream.scrollHeight;
    }
});
