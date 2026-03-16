import { getUsageSummary } from "./api.js";
import { showToast } from "./ui.js";

const BASE_URL = "http://127.0.0.1:5000";

// ===============================
// SHOW NO PLAN STATE
// ===============================
function showNoPlanState() {
    const noPlan = document.getElementById("noPlanState");
    const dashboard = document.getElementById("dashboardContent");

    if (noPlan) noPlan.style.display = "block";
    if (dashboard) dashboard.style.display = "none";
}

// ===============================
// CHECK SUBSCRIPTION
// ===============================
async function checkSubscription() {
    const userId = localStorage.getItem("user_id");

    if (!userId) {
        window.location.href = "signin.html";
        return false;
    }

    try {
        const res = await fetch(`${BASE_URL}/subscription/${userId}`);

        if (!res.ok) {
            showNoPlanState();
            return false;
        }

        const data = await res.json();
        const subscription = data.subscription;

        if (!subscription || subscription.status !== "active") {
            showNoPlanState();
            return false;
        }

        // Show dashboard
        document.getElementById("dashboardContent").style.display = "block";
        document.getElementById("noPlanState").style.display = "none";

        // Update plan name
        const planNameEl = document.getElementById("planName");
        if (planNameEl) {
            planNameEl.textContent = subscription.plan_id;
        }

        return true;

    } catch (err) {
        console.error("Subscription check failed:", err);
        showNoPlanState();
        return false;
    }
}

// ===============================
// LOAD USAGE SUMMARY
// ===============================
async function loadUsageSummary() {
    const userId = localStorage.getItem("user_id");

    try {
        const data = await getUsageSummary(userId);

        const unitsEl = document.getElementById("units");
        const limitEl = document.getElementById("limit");
        const rewardEl = document.getElementById("rewardPoints");
        const percentageEl = document.getElementById("percentage");

        if (unitsEl) unitsEl.textContent = data.total_units || 0;
        if (limitEl) limitEl.textContent = data.included_units || 0;

        if (rewardEl) {
            rewardEl.textContent = `🎁 Reward points: ${data.reward_points || 0}`;
        }

        if (percentageEl && data.included_units > 0) {
            const percent = Math.min(
                100,
                Math.round((data.total_units / data.included_units) * 100)
            );
            percentageEl.textContent = percent + "%";
        }

    } catch (error) {
        console.error("Usage summary error:", error);
        showToast("Failed to load usage summary", "error");
    }
}

// ===============================
// INIT
// ===============================
document.addEventListener("DOMContentLoaded", async () => {
    const hasSubscription = await checkSubscription();

    if (hasSubscription) {
        await loadUsageSummary();
    }
});