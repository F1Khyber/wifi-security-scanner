/*
 * WiFi Security Scanner
 * Dashboard JavaScript
 */


/* =========================================================
   DOM ELEMENTS
   ========================================================= */

const table = document.getElementById("network-table");
const networkCountElement = document.getElementById("network-count");
const highRiskElement = document.getElementById("high-risk");
const mediumRiskElement = document.getElementById("medium-risk");
const lowRiskElement = document.getElementById("low-risk");


/* =========================================================
   LOAD NETWORKS
   ========================================================= */

async function loadNetworks() {

    if (!table) {
        console.error("Element #network-table not found");
        return;
    }

    // Show scanning state
    table.innerHTML = `
        <tr>
            <td colspan="6">
                Scanning...
            </td>
        </tr>
    `;

    try {

        const response = await fetch("/api/networks", {
            method: "GET",
            headers: {
                Accept: "application/json"
            }
        });


        /*
         * Check HTTP response
         */
        if (!response.ok) {
            throw new Error(
                `Server error: ${response.status}`
            );
        }


        /*
         * Parse JSON
         */
        const data = await response.json();

        console.log("API response:", data);


        /*
         * Check API success
         */
        if (!data || data.success !== true) {

            throw new Error(
                data?.error ||
                "Network scan failed"
            );
        }


        /*
         * Get networks
         */
        const networks = Array.isArray(data.networks)
            ? data.networks
            : [];


        console.log(
            "Networks received:",
            networks
        );


        /*
         * Update dashboard
         */
        updateStatistics(networks);

        renderNetworks(networks);


    } catch (error) {

        console.error(
            "Network scan error:",
            error
        );


        table.innerHTML = `
            <tr>
                <td colspan="6">
                    Error:
                    ${escapeHtml(error.message)}
                </td>
            </tr>
        `;


        /*
         * Reset statistics
         */
        updateStatistics([]);
    }
}


/* =========================================================
   UPDATE STATISTICS
   ========================================================= */

function updateStatistics(networks) {

    let highRisk = 0;
    let mediumRisk = 0;
    let lowRisk = 0;


    networks.forEach((network) => {

        const risk = network?.risk ?? {};


        /*
         * Get risk level
         *
         * Supports:
         *
         * risk.level
         * risk.riskLevel
         * risk.status
         */
        const riskLevel = getRiskLevel(risk);


        console.log(
            "Network:",
            network?.ssid || "Unknown"
        );

        console.log(
            "Risk:",
            risk
        );

        console.log(
            "Risk Level:",
            riskLevel
        );


        /*
         * Count risk
         */
        if (
            riskLevel === "HIGH" ||
            riskLevel === "RED"
        ) {

            highRisk++;

        } else if (
            riskLevel === "MEDIUM" ||
            riskLevel === "YELLOW"
        ) {

            mediumRisk++;

        } else if (
            riskLevel === "LOW" ||
            riskLevel === "GREEN"
        ) {

            lowRisk++;
        }
    });


    /*
     * Update DOM
     */

    if (networkCountElement) {

        networkCountElement.textContent =
            networks.length;
    }


    if (highRiskElement) {

        highRiskElement.textContent =
            highRisk;
    }


    if (mediumRiskElement) {

        mediumRiskElement.textContent =
            mediumRisk;
    }


    if (lowRiskElement) {

        lowRiskElement.textContent =
            lowRisk;
    }
}


/* =========================================================
   GET RISK LEVEL
   ========================================================= */

function getRiskLevel(risk) {

    if (!risk || typeof risk !== "object") {
        return "UNKNOWN";
    }


    /*
     * Try different possible backend field names
     */

    const value =
        risk.level ??
        risk.riskLevel ??
        risk.risk_level ??
        risk.status ??
        risk.severity ??
        "UNKNOWN";


    return String(value)
        .trim()
        .toUpperCase();
}


/* =========================================================
   GET RISK SCORE
   ========================================================= */

function getRiskScore(risk) {

    if (!risk || typeof risk !== "object") {
        return null;
    }


    /*
     * Try different possible backend field names
     */

    const value =
        risk.score ??
        risk.riskScore ??
        risk.risk_score ??
        risk.points ??
        risk.riskPoints;


    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {
        return null;
    }


    const score = Number(value);


    return Number.isFinite(score)
        ? score
        : null;
}


/* =========================================================
   GET RISK CSS CLASS
   ========================================================= */

function getRiskClass(riskLevel) {

    switch (riskLevel) {

        case "HIGH":
        case "RED":
            return "risk-red";


        case "MEDIUM":
        case "YELLOW":
            return "risk-yellow";


        case "LOW":
        case "GREEN":
            return "risk-green";


        default:
            return "risk-unknown";
    }
}


/* =========================================================
   RENDER NETWORKS
   ========================================================= */

function renderNetworks(networks) {

    if (!table) {
        console.error(
            "Element #network-table not found"
        );

        return;
    }


    /*
     * Clear table
     */

    table.innerHTML = "";


    /*
     * No networks
     */

    if (!Array.isArray(networks) || networks.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    No WiFi networks found.
                </td>
            </tr>
        `;

        return;
    }


    /*
     * Render every network
     */

    networks.forEach((network) => {

        const row =
            document.createElement("tr");


        /*
         * Basic network information
         */

        const ssid =
            network?.ssid ||
            "Hidden";


        const bssid =
            network?.bssid ||
            "Unknown";


        const security =
            network?.security ||
            network?.encryption ||
            "Unknown";


        const signal =
            network?.signal ??
            network?.signalStrength ??
            "N/A";


        const channel =
            network?.channel ??
            "N/A";


        /*
         * Risk information
         */

        const risk =
            network?.risk ?? {};


        console.log(
            "FULL RISK OBJECT:",
            risk
        );


        console.log(
            "RISK JSON:",
            JSON.stringify(
                risk,
                null,
                2
            )
        );


        /*
         * Get risk level
         */

        const riskLevel =
            getRiskLevel(risk);


        /*
         * Get risk score
         */

        const riskScore =
            getRiskScore(risk);


        /*
         * Get CSS class
         */

        const riskClass =
            getRiskClass(riskLevel);


        /*
         * Display score only
         * if backend provides one
         */

        const scoreText =
            riskScore !== null
                ? ` (${riskScore})`
                : "";


        /*
         * Create row
         */

        row.innerHTML = `

            <td>
                ${escapeHtml(ssid)}
            </td>

            <td>
                ${escapeHtml(bssid)}
            </td>

            <td>
                ${escapeHtml(security)}
            </td>

            <td>
                ${escapeHtml(signal)}
            </td>

            <td>
                ${escapeHtml(channel)}
            </td>

            <td>
                <span class="${riskClass}">
                    ${escapeHtml(
                        riskLevel
                    )}
                    ${scoreText}
                </span>
            </td>

        `;


        /*
         * Add row to table
         */

        table.appendChild(row);
    });
}


/* =========================================================
   HTML ESCAPE
   ========================================================= */

function escapeHtml(value) {

    const div =
        document.createElement("div");


    div.textContent =
        String(value);


    return div.innerHTML;
}


/* =========================================================
   INITIAL SCAN
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "WiFi Security Scanner loaded"
        );


        loadNetworks();
    }
);