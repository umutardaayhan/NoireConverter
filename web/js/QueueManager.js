export class QueueManager {
    constructor(containerId, templateId) {
        this.container = document.getElementById(containerId);
        this.template = document.getElementById(templateId);
        this.queuedFiles = [];
        this.bindGlobalEvents();
    }

    bindGlobalEvents() {
        const clearBtn = document.getElementById('clear-queue');
        if(clearBtn) {
            clearBtn.addEventListener('click', () => {
                const toRemove = this.queuedFiles.filter(f => f.status === 'DONE');
                toRemove.forEach(f => {
                    const el = document.getElementById(f.id);
                    if(el) el.remove();
                });
                this.queuedFiles = this.queuedFiles.filter(f => f.status !== 'DONE');
            });
        }
    }

    addFile(file, targetFormatStr) {
        const fileData = {
            file: file,
            id: 'queue_' + Math.random().toString(36).substr(2, 9),
            status: 'WAITING',
            targetFormatStr: targetFormatStr
        };
        this.queuedFiles.push(fileData);
        this.renderItem(fileData);
        return fileData;
    }

    renderItem(fileData) {
        const templateNode = this.template.content.cloneNode(true);
        const itemNode = templateNode.querySelector('.queue-item');
        itemNode.id = fileData.id;

        itemNode.querySelector('.file-name').textContent = fileData.file.name;
        itemNode.querySelector('.file-size').textContent = this.formatBytes(fileData.file.size);
        itemNode.querySelector('.target-badge').textContent = fileData.targetFormatStr;
        
        itemNode.querySelector('.remove-btn').addEventListener('click', () => {
            if(fileData.status === 'PROCESSING') return; // İşlenirken iptal edilmez
            this.queuedFiles = this.queuedFiles.filter(f => f.id !== fileData.id);
            itemNode.remove();
        });

        this.container.appendChild(itemNode);
    }

    updateStatus(fileData, status, progressVal = null) {
        const itemNode = document.getElementById(fileData.id);
        if (!itemNode) return;
        fileData.status = status;
        
        const iconBox = itemNode.querySelector('.status-icon-box');
        const icon = itemNode.querySelector('.status-icon');
        const progressBar = itemNode.querySelector('.progress-bar');
        const statusText = itemNode.querySelector('.status-text');
        const progressText = itemNode.querySelector('.progress-text');

        iconBox.className = "status-icon-box w-10 h-10 rounded flex items-center justify-center transition-colors";
        icon.className = "status-icon material-symbols-outlined";

        if (status === 'PROCESSING') {
            itemNode.classList.add('bg-surface-container-high');
            iconBox.classList.add('bg-primary/10', 'animate-pulse');
            icon.classList.add('text-primary');
            icon.textContent = 'motion_photos_on';
            statusText.textContent = 'Processing...';
            statusText.className = "status-text text-[10px] text-primary uppercase font-bold tracking-widest";
            if (progressVal !== null) {
                progressBar.style.width = progressVal + '%';
                progressText.textContent = progressVal + '%';
            }
        } 
        else if (status === 'DONE') {
            itemNode.classList.remove('bg-surface-container-high');
            itemNode.classList.add('bg-green-900/10');
            iconBox.classList.add('bg-green-900/40');
            icon.classList.add('text-green-500');
            icon.textContent = 'check_circle';
            progressBar.className = "progress-bar h-full bg-green-500 transition-all duration-300 w-full";
            statusText.textContent = 'Done ✓';
            statusText.className = "status-text text-[10px] text-green-500 uppercase font-bold tracking-widest";
            progressText.textContent = '100%';
        }
    }

    getWaitingFiles() { return this.queuedFiles.filter(f => f.status === 'WAITING'); }

    formatBytes(bytes, decimals = 2) {
        if (!+bytes) return '0 Bytes';
        const k = 1024, dm = decimals < 0 ? 0 : decimals, sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }
}
