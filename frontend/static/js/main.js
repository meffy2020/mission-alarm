const API_URL = "";

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function getToken() {
    return localStorage.getItem("access_token");
}

function getAuthHeaders() {
    const token = getToken();
    return token ? { "Authorization": `Bearer ${token}` } : {};
}

async function checkAuth() {
    if (!getToken()) {
        window.location.href = "/";
    }
}

function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "/";
}
