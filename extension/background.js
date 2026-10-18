chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "save") {
        fetch("http://127.0.0.1:8000/remember", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: request.text, agent_id: "browser_web" })
        })
        .then(res => res.json())
        .then(data => sendResponse({ success: true, id: data.id }))
        .catch(err => sendResponse({ success: false, error: err.toString() }));
        return true; 
    }
    
    if (request.action === "recall") {
        fetch("http://127.0.0.1:8000/recall")
        .then(res => res.json())
        .then(data => sendResponse({ success: true, memories: data }))
        .catch(err => sendResponse({ success: false, error: err.toString() }));
        return true;
    }
});