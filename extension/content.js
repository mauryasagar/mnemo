chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // --- HANDLE SAVE ---
    if (request.action === "trigger_save") {
        let sessionText = "";
        const messages = document.querySelectorAll('[data-message-author-role]');
        
        if (messages.length > 0) {
            sessionText = "Chat Session:\n";
            messages.forEach(msg => {
                sessionText += `\n[${msg.getAttribute('data-message-author-role')}]: ${msg.innerText.trim()}`;
            });
        } else {
            const mainChat = document.querySelector('main');
            if (mainChat) sessionText = mainChat.innerText.trim();
        }

        if (!sessionText || sessionText.trim() === "") {
            sendResponse({success: false, error: "No text found"});
            return;
        }
        if (sessionText.length > 2000) sessionText = sessionText.substring(0, 2000) + "\n...[Truncated]";

        chrome.runtime.sendMessage({ action: "save", text: sessionText }, (bgResponse) => {
            sendResponse(bgResponse);
        });
        return true; // keep channel open for async
    }

    // --- HANDLE INJECT ---
    if (request.action === "trigger_inject") {
        chrome.runtime.sendMessage({ action: "recall" }, (bgResponse) => {
            if (bgResponse && bgResponse.success && bgResponse.memories.length > 0) {
                const memText = bgResponse.memories.map(m => `- ${m.text}`).join('\n');
                const contextString = `[System Context: Use these facts to answer my next question:\n${memText}]\n\n`;
                
                const inputBox = document.querySelector('#prompt-textarea') || 
                                 document.querySelector('rich-textarea div[contenteditable="true"]') ||
                                 document.querySelector('textarea') || 
                                 document.querySelector('div[contenteditable="true"]');
                
                if (inputBox) {
                    inputBox.focus();
                    if (inputBox.tagName === 'TEXTAREA') {
                        inputBox.value = contextString + inputBox.value;
                    } else {
                        inputBox.innerText = contextString + inputBox.innerText;
                        inputBox.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    sendResponse({success: true});
                } else {
                    sendResponse({success: false, error: "Input box not found"});
                }
            } else {
                sendResponse({success: false, error: "No memories found"});
            }
        });
        return true; // keep channel open for async
    }
});