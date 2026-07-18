/**
 * DocuMind AI — Frontend Client
 *
 * Handles file uploads, chat interactions, SSE streaming,
 * history retrieval, and UI states.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ─── DOM Elements ─────────────────────────────────────────────
    const fileInput = document.getElementById('file-input');
    const uploadZone = document.getElementById('upload-zone');
    const uploadProgress = document.getElementById('upload-progress');
    const uploadFilename = document.getElementById('upload-filename');
    const uploadStatus = document.getElementById('upload-status');
    const progressFill = document.getElementById('progress-fill');
    
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menu-toggle');
    const documentPanel = document.getElementById('document-panel');
    const docName = document.getElementById('doc-name');
    const docMeta = document.getElementById('doc-meta');
    const summaryText = document.getElementById('summary-text');
    const uploadSection = document.getElementById('upload-section');
    
    const headerStatus = document.getElementById('header-status');
    const chatContainer = document.getElementById('chat-container');
    const welcomeState = document.getElementById('welcome-state');
    const messagesContainer = document.getElementById('messages');
    
    const chatForm = document.getElementById('chat-form');
    const questionInput = document.getElementById('question-input');
    const sendButton = document.getElementById('send-button');
    const followUpChipsContainer = document.getElementById('follow-up-chips');
    
    const sourcesPanel = document.getElementById('sources-panel');
    const sourcesClose = document.getElementById('sources-close');
    const sourcesList = document.getElementById('sources-list');
    
    const toastContainer = document.getElementById('toast-container');

    // ─── Application State ─────────────────────────────────────────
    let activeDocumentId = null;
    let activeSessionId = null;
    let isGenerating = false;

    // ─── Sidebar Toggle (Mobile) ──────────────────────────────────
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target) && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        }
    });

    // ─── Toast Notifications ──────────────────────────────────────
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);

        // Remove toast after animation completes
        toast.addEventListener('animationend', (e) => {
            if (e.animationName === 'toastOut') {
                toast.remove();
            }
        });
    }

    // ─── Drag & Drop Event Listeners ─────────────────────────────
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.remove('drag-over');
        }, false);
    });

    uploadZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileUpload(fileInput.files[0]);
        }
    });

    // ─── File Upload Handler ──────────────────────────────────────
    async function handleFileUpload(file) {
        // Validate file extension
        const allowedExtensions = ['.pdf', '.docx'];
        const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        
        if (!allowedExtensions.includes(fileExtension)) {
            showToast('Only PDF and DOCX files are supported.', 'error');
            return;
        }

        // Show progress UI
        uploadZone.style.display = 'none';
        uploadProgress.style.display = 'block';
        uploadFilename.textContent = file.name;
        uploadStatus.textContent = 'Uploading...';
        progressFill.style.width = '10%';

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Simulated incremental progress for design aesthetic
            const progressInterval = setInterval(() => {
                const currentWidth = parseFloat(progressFill.style.width);
                if (currentWidth < 85) {
                    progressFill.style.width = `${currentWidth + 10}%`;
                }
            }, 200);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            clearInterval(progressInterval);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to upload document.');
            }

            progressFill.style.width = '100%';
            uploadStatus.textContent = 'Processing...';

            const result = await response.json();
            
            // Set active document
            activeDocumentId = result.document_id;
            activeSessionId = null; // Clear previous session for new document

            // Update UI with document details
            showToast('Document uploaded and processed successfully!', 'success');
            
            setTimeout(() => {
                // Update Sidebar
                uploadProgress.style.display = 'none';
                uploadSection.style.display = 'none';
                
                docName.textContent = result.filename;
                docMeta.textContent = `${result.pages} Pages • ${result.chunks} Chunks`;
                summaryText.textContent = result.summary || 'No summary available.';
                documentPanel.style.display = 'block';

                // Update Header
                headerStatus.textContent = `Active: ${result.filename}`;
                
                // Enable Input
                questionInput.disabled = false;
                questionInput.placeholder = "Ask a question about this document...";
                sendButton.disabled = false;
                
                // Clear any existing chat messages
                messagesContainer.innerHTML = '';
                welcomeState.style.display = 'none';
                followUpChipsContainer.style.display = 'none';
                sourcesPanel.style.display = 'none';

                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                }
            }, 600);

        } catch (error) {
            console.error('Upload error:', error);
            showToast(error.message || 'Error uploading file.', 'error');
            
            // Reset upload UI on error
            progressFill.style.width = '0%';
            uploadProgress.style.display = 'none';
            uploadZone.style.display = 'block';
        }
    }

    // ─── Textarea Auto-Resize ─────────────────────────────────────
    questionInput.addEventListener('input', () => {
        questionInput.style.height = 'auto';
        questionInput.style.height = `${Math.min(questionInput.scrollHeight - 10, 120)}px`;
    });

    // Handle Enter to submit, Shift+Enter for new line
    questionInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // ─── Sample Questions Click ──────────────────────────────────
    document.querySelectorAll('.sample-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const question = chip.getAttribute('data-question');
            if (activeDocumentId && !isGenerating) {
                questionInput.value = question;
                chatForm.dispatchEvent(new Event('submit'));
            } else if (!activeDocumentId) {
                showToast('Please upload a document first.', 'info');
            }
        });
    });

    // ─── Chat Form Submission ────────────────────────────────────
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question || !activeDocumentId || isGenerating) return;

        // Clear input & reset height
        questionInput.value = '';
        questionInput.style.height = 'auto';
        
        // Hide welcome state if visible
        welcomeState.style.display = 'none';
        
        // Disable input during generation
        toggleInputState(true);

        // Add human message to chat
        appendMessage('human', question);
        scrollToBottom();

        // Add dummy assistant message with loading spinner
        const assistantMessageEl = appendMessage('assistant', '');
        const contentEl = assistantMessageEl.querySelector('.message-content');
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        contentEl.appendChild(indicator);
        scrollToBottom();

        // Hide old follow-ups & sources
        followUpChipsContainer.style.display = 'none';
        followUpChipsContainer.innerHTML = '';

        try {
            // Streaming SSE Chat Request
            const response = await fetch('/chat/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    document_id: activeDocumentId,
                    question: question,
                    session_id: activeSessionId
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Streaming failed.');
            }

            // Remove typing indicator before writing stream
            indicator.remove();
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            let assistantText = '';
            let currentSources = [];
            let currentFollowUps = [];
            
            let buffer = '';
            let currentEvent = null;

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                
                // Keep the last partial line in buffer
                buffer = lines.pop();

                for (const line of lines) {
                    const trimmedLine = line.trim();
                    if (!trimmedLine) {
                        currentEvent = null;
                        continue;
                    }

                    if (line.startsWith('event:')) {
                        currentEvent = line.substring(6).trim();
                    } else if (line.startsWith('data:')) {
                        // Keep spacing intact: strip only the prefix "data:" and one optional space
                        let dataPayload = line.substring(5);
                        if (dataPayload.startsWith(' ')) {
                            dataPayload = dataPayload.substring(1);
                        }

                        if (currentEvent) {
                            handleSSEEvent(currentEvent, dataPayload, contentEl, (text) => {
                                assistantText += text;
                                
                                // Check if we have hit the follow-up questions marker
                                const followUpMarkerIndex = assistantText.indexOf('FOLLOW_UP:');
                                if (followUpMarkerIndex !== -1) {
                                    // Truncate the displayed text up to the marker
                                    const cleanText = assistantText.substring(0, followUpMarkerIndex).trim();
                                    contentEl.textContent = cleanText;
                                } else {
                                    // Handle partial match checking for "FOLLOW_UP:"
                                    const marker = 'FOLLOW_UP:';
                                    let showText = assistantText;
                                    for (let len = marker.length; len > 0; len--) {
                                        const sub = marker.substring(0, len);
                                        if (assistantText.endsWith(sub)) {
                                            showText = assistantText.substring(0, assistantText.length - len);
                                            break;
                                        }
                                    }
                                    contentEl.textContent = showText;
                                }
                                scrollToBottom();
                            }, (sources) => {
                                currentSources = sources;
                            }, (followUps) => {
                                currentFollowUps = followUps;
                            }, (sessionInfo) => {
                                if (sessionInfo && sessionInfo.session_id) {
                                    activeSessionId = sessionInfo.session_id;
                                }
                            });
                        }
                    }
                }
            }

            // Flush remaining buffer if any
            if (buffer.trim()) {
                const lines = buffer.split('\n');
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (trimmed.startsWith('event:')) {
                        // Safe parsing if event matches
                    }
                }
            }

            // Finalize message rendering
            if (currentSources.length > 0) {
                appendSourcesButton(assistantMessageEl, currentSources);
            }

            if (currentFollowUps.length > 0) {
                renderFollowUps(currentFollowUps);
            }

        } catch (error) {
            console.error('Streaming error:', error);
            indicator.remove();
            contentEl.textContent = 'An error occurred while generating the answer. Please try again.';
            contentEl.style.color = 'var(--error)';
            showToast('Error generating response.', 'error');
        } finally {
            toggleInputState(false);
            scrollToBottom();
        }
    });

    // ─── SSE Event Router ──────────────────────────────────────────
    function handleSSEEvent(type, dataStr, contentEl, onToken, onSources, onFollowUps, onDone) {
        try {
            switch (type) {
                case 'token':
                    onToken(dataStr);
                    break;

                case 'sources':
                    const sources = JSON.parse(dataStr);
                    onSources(sources);
                    break;

                case 'follow_ups':
                    const followUps = JSON.parse(dataStr);
                    onFollowUps(followUps);
                    break;

                case 'done':
                    if (dataStr) {
                        const doneData = JSON.parse(dataStr);
                        onDone(doneData);
                    }
                    break;

                case 'error':
                    throw new Error(dataStr);
            }
        } catch (e) {
            console.error('Error handling SSE event:', e);
        }
    }

    // ─── Message UI Builders ──────────────────────────────────────
    function appendMessage(role, text) {
        const messageEl = document.createElement('div');
        messageEl.className = `message ${role}`;
        
        const avatarEl = document.createElement('div');
        avatarEl.className = 'message-avatar';
        avatarEl.textContent = role === 'human' ? 'U' : 'AI';

        const contentEl = document.createElement('div');
        contentEl.className = 'message-content';
        contentEl.textContent = text;

        messageEl.appendChild(avatarEl);
        messageEl.appendChild(contentEl);
        
        messagesContainer.appendChild(messageEl);
        return messageEl;
    }

    function appendSourcesButton(messageEl, sources) {
        const contentEl = messageEl.querySelector('.message-content');
        const btn = document.createElement('button');
        btn.className = 'message-sources-btn';
        btn.innerHTML = `
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
            </svg>
            View Sources (${sources.length})
        `;
        
        btn.addEventListener('click', () => {
            renderSourcesPanel(sources);
        });

        contentEl.appendChild(btn);
    }

    // ─── Sources Panel ────────────────────────────────────────────
    function renderSourcesPanel(sources) {
        sourcesList.innerHTML = '';
        sources.forEach(src => {
            const item = document.createElement('div');
            item.className = 'source-item';
            item.innerHTML = `
                <div class="source-meta">Page ${src.page} • Score ${src.score}</div>
                <div class="source-preview">${src.preview}</div>
            `;
            sourcesList.appendChild(item);
        });
        sourcesPanel.style.display = 'block';
    }

    sourcesClose.addEventListener('click', () => {
        sourcesPanel.style.display = 'none';
    });

    // ─── Follow-Up Questions ──────────────────────────────────────
    function renderFollowUps(followUps) {
        followUpChipsContainer.innerHTML = '';
        
        followUps.forEach(q => {
            const chip = document.createElement('button');
            chip.className = 'follow-up-chip';
            chip.textContent = q;
            chip.addEventListener('click', () => {
                if (!isGenerating) {
                    questionInput.value = q;
                    chatForm.dispatchEvent(new Event('submit'));
                }
            });
            followUpChipsContainer.appendChild(chip);
        });
        
        followUpChipsContainer.style.display = 'flex';
    }

    // ─── Helper Functions ──────────────────────────────────────────
    function toggleInputState(disabled) {
        isGenerating = disabled;
        questionInput.disabled = disabled;
        sendButton.disabled = disabled;
        
        if (!disabled) {
            questionInput.focus();
        }
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
