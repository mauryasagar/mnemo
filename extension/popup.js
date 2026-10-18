document.getElementById('saveBtn').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    document.getElementById('status').innerText = "Saving...";
    
    chrome.tabs.sendMessage(tab.id, {action: "trigger_save"}, (response) => {
        if (response && response.success) {
            document.getElementById('status').innerText = "Saved successfully";
        } else {
            document.getElementById('status').innerText = "Error saving";
        }
    });
});

document.getElementById('injectBtn').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    document.getElementById('status').innerText = "Injecting...";
    
    chrome.tabs.sendMessage(tab.id, {action: "trigger_inject"}, (response) => {
        if (response && response.success) {
            document.getElementById('status').innerText = "Injected successfully";
        } else {
            document.getElementById('status').innerText = "Error injecting";
        }
    });
});