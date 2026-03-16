import { BASE_URL } from "./config.js";

export async function registerUserAPI(user_id, name, email) {
    console.log(`📝 Registering user: ${user_id}, ${name}, ${email}`);
    
    try {
        const response = await fetch(`${BASE_URL}/register`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ 
                user_id,
                name,
                email
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Registration failed with status ${response.status}`);
        }

        return { 
            success: true, 
            data,
            message: data.message || "Registration successful"
        };
        
    } catch (error) {
        return { 
            success: false, 
            error: error.message,
            message: `Registration failed: ${error.message}`
        };
    }
}
export async function getUsageSummary(userId) {
    const response = await fetch(`${BASE_URL}/usage/summary/${userId}`);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Failed to fetch usage summary");
    }

    return data;
}
export async function subscribeUser(userId, planId) {
    try {
        const response = await fetch(`${BASE_URL}/plan/subscribe`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                plan_id: planId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Subscription failed");
        }

        return {
            success: true,
            data,
            message: data.message || "Subscribed successfully"
        };

    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}