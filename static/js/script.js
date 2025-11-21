document.addEventListener("DOMContentLoaded", function () {
    const runButton = document.getElementById("run-button");
    const stopButton = document.getElementById("stop-button");
    const statusText = document.getElementById("status-text");
    const logContainer = document.getElementById("log-container");
    const reportContent = document.getElementById("report-content");
    const chartImage = document.getElementById("chart-image");
    const noChartMessage = document.getElementById("no-chart-message");
    const resultsPanel = document.getElementById("results-panel");
    const timestamp = document.getElementById("timestamp");
    const emailStatus = document.getElementById("email-text");
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    // Tab switching functionality
    tabButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));

            // Add active class to clicked button and corresponding content
            button.classList.add("active");
            const tabId = button.getAttribute("data-tab");
            document.getElementById(`${tabId}-tab`).classList.add("active");

            // If visualization tab is selected, refresh the chart
            if (tabId === "visualization") {
                refreshChart();
            }
        });
    });

    function updateStatus() {
        fetch("/status")
            .then(response => response.json())
            .then(data => {
                statusText.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
                document.querySelector(".status").className = `status ${data.status}`;

                if (data.status === "running") {
                    resultsPanel.style.display = "block";
                    logContainer.innerHTML = data.messages.join("<br>");
                    logContainer.scrollTop = logContainer.scrollHeight;
                    timestamp.textContent = "Started: " + data.timestamp;
                }

                if (data.status === "completed") {
                    logContainer.innerHTML = data.messages.join("<br>");
                    logContainer.scrollTop = logContainer.scrollHeight;
                    emailStatus.textContent = data.email_sent ? "📧 Email sent successfully!" : "📧 Waiting to send email...";
                    fetchReport();
                    refreshChart();
                }

                if (data.status === "error") {
                    logContainer.innerHTML = `<span class='error'>${data.messages.join("<br>")}</span>`;
                    logContainer.scrollTop = logContainer.scrollHeight;
                }
            })
            .catch(error => console.error("Error fetching status:", error));
    }

    function fetchReport() {
        fetch("/report")
            .then(response => response.json())
            .then(data => {
                reportContent.textContent = data.content || "Report not available";
            })
            .catch(error => {
                console.error("Error fetching report:", error);
                reportContent.textContent = "Error loading report";
            });
    }

    function refreshChart() {
        // Add timestamp to force browser to reload the image
        const timestamp = new Date().getTime();
        chartImage.src = `/static/sentinel_output/forest_classification.png?t=${timestamp}`;
        
        // Show/hide chart and message based on image load
        chartImage.onload = function() {
            chartImage.style.display = "block";
            noChartMessage.style.display = "none";
        };
        
        chartImage.onerror = function() {
            chartImage.style.display = "none";
            noChartMessage.style.display = "block";
        };
    }

    runButton.addEventListener("click", () => {
        fetch("/run-analysis", { method: "POST" })
            .then(() => {
                statusText.textContent = "Running...";
                document.querySelector(".status").className = "status running";
                resultsPanel.style.display = "block";
                logContainer.innerHTML = "Initializing analysis...";
                timestamp.textContent = "";
                emailStatus.textContent = "📧 Waiting to send email...";
                reportContent.textContent = "Analysis in progress...";
                chartImage.style.display = "none";
                noChartMessage.style.display = "block";
                noChartMessage.textContent = "Analysis in progress...";
            })
            .catch(error => console.error("Error starting analysis:", error));
    });

    stopButton.addEventListener("click", () => {
        statusText.textContent = "Stopped";
        document.querySelector(".status").className = "status idle";
        resultsPanel.style.display = "none";
        logContainer.innerHTML = "";
        timestamp.textContent = "";
    });

    // Initial status check
    updateStatus();
    
    // Regular status updates
    setInterval(updateStatus, 2000);  // Check every 2 seconds
});
