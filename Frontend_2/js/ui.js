// js/ui.js

export function $id(id) {
    const el = document.getElementById(id);
    if (!el && id) {
        console.warn(`Element #${id} not found`);
    }
    return el;
}

export function showMessage(message, type = "info") {
    console.log(`${type.toUpperCase()}: ${message}`);
    
    const resultElement = $id("subscribeResult");

    if (!resultElement) {
        showToast(message, type);
        return;
    }

    const styles = {
        success: { background: "#f0fdf4", color: "#166534", border: "1px solid #bbf7d0" },
        error: { background: "#fef2f2", color: "#991b1b", border: "1px solid #fecaca" },
        warning: { background: "#fffbeb", color: "#92400e", border: "1px solid #fed7aa" },
        info: { background: "#f0f9ff", color: "#1e40af", border: "1px solid #bae6fd" }
    };

    const style = styles[type] || styles.info;

    resultElement.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <span>${type === 'success' ? '✅' :
                    type === 'error' ? '❌' :
                    type === 'warning' ? '⚠️' : 'ℹ️'}</span>
            <span>${message}</span>
        </div>
    `;

    resultElement.style.background = style.background;
    resultElement.style.color = style.color;
    resultElement.style.border = style.border;
    resultElement.style.padding = "12px";
    resultElement.style.borderRadius = "8px";
    resultElement.style.marginTop = "15px";

    setTimeout(() => {
        resultElement.style.opacity = '0';
        setTimeout(() => {
            resultElement.innerHTML = '';
            resultElement.style.opacity = '1';
        }, 300);
    }, 5000);
}

export function showToast(message, type = "info") {
    document.querySelectorAll('.smartpower-toast').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = 'smartpower-toast';

    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background: ${type === 'success' ? '#10b981' :
                     type === 'error' ? '#ef4444' :
                     type === 'warning' ? '#f59e0b' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
    `;

    toast.innerHTML = `
        <span>${type === 'success' ? '✅' :
                type === 'error' ? '❌' :
                type === 'warning' ? '⚠️' : 'ℹ️'}</span>
        <span>${message}</span>
    `;

    document.body.appendChild(toast);

    setTimeout(() => toast.remove(), 3000);
}