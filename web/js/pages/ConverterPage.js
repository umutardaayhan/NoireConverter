export class ConverterPage {
    constructor(queueManager) {
        this.queueManager = queueManager;
        
        // Event temizliği için fonksiyon referanslarını saklarız
        this.boundHandleFiles = this.handleFiles.bind(this);
        this.boundProcessFiles = this.processFiles.bind(this);
    }

    init() {
        this.dropzone = document.getElementById('dropzone');
        this.fileInput = document.getElementById('file-input');
        this.browseBtn = document.getElementById('browse-btn');
        this.btnStart = document.getElementById('btn-start');
        this.btnText = document.getElementById('btn-text');
        this.targetFormat = document.getElementById('target-format');
        this.qualitySlider = document.getElementById('quality-slider');
        this.qualityVal = document.getElementById('quality-val');

        this.bindEvents();
    }

    bindEvents() {
        if(this.qualitySlider) {
            this.qualitySlider.addEventListener('input', (e) => {
                this.qualityVal.textContent = e.target.value + '%';
            });
        }

        if(this.browseBtn) {
            this.browseBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.fileInput.click();
            });
        }
        
        if(this.dropzone) {
            this.dropzone.addEventListener('click', () => this.fileInput.click());
            this.dropzone.addEventListener('dragover', (e) => { e.preventDefault(); this.dropzone.classList.add('dragover'); });
            this.dropzone.addEventListener('dragleave', () => this.dropzone.classList.remove('dragover'));
            this.dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                this.dropzone.classList.remove('dragover');
                if (e.dataTransfer.files.length > 0) this.handleFiles(e.dataTransfer.files);
            });
        }

        if(this.fileInput) {
            this.fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) this.handleFiles(e.target.files);
            });
        }

        if(this.btnStart) {
            this.btnStart.addEventListener('click', this.boundProcessFiles);
        }
    }

    handleFiles(files) {
        const formatStr = this.targetFormat.options[this.targetFormat.selectedIndex].text;
        Array.from(files).forEach(file => {
            this.queueManager.addFile(file, formatStr);
        });
        this.fileInput.value = ''; 
    }

    async processFiles() {
        const waitingFiles = this.queueManager.getWaitingFiles();
        if (waitingFiles.length === 0) return;

        this.btnText.textContent = "PROCESSING...";
        this.btnStart.style.pointerEvents = 'none';
        this.btnStart.classList.add('opacity-70');

        for (let f of waitingFiles) {
            this.queueManager.updateStatus(f, 'PROCESSING', 10);
            
            const formData = new FormData();
            formData.append('file', f.file);
            const cleanFormat = f.targetFormatStr.replace(/^TO\s+/i, '').trim().toLowerCase();
            formData.append('target_format', cleanFormat);
            formData.append('quality', this.qualitySlider ? parseInt(this.qualitySlider.value) : 100);

            try {
                this.queueManager.updateStatus(f, 'PROCESSING', 50);
                const response = await fetch('/api/v1/convert', { method: 'POST', body: formData });
                
                if (!response.ok) {
                    throw new Error("API Error: " + response.status);
                }
                
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                
                const disposition = response.headers.get('content-disposition');
                let filename = 'converted_media.' + f.targetFormatStr.toLowerCase();
                if (disposition && disposition.indexOf('filename=') !== -1) {
                    const matches = /filename="([^"]*)"/.exec(disposition) || /filename=([^;]*)/.exec(disposition);
                    if (matches != null && matches[1]) { 
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }
                a.download = filename;
                
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);
                
                this.queueManager.updateStatus(f, 'DONE');
                
            } catch (err) {
                console.error(err);
                f.status = 'ERROR';
                const el = document.getElementById(f.id);
                if (el) {
                    el.classList.add('bg-error/10');
                    el.querySelector('.status-text').textContent = 'Error';
                    el.querySelector('.status-text').classList.add('text-error');
                    el.querySelector('.progress-bar').classList.add('bg-error');
                }
            }
        }

        this.btnText.textContent = "START PROCESS";
        this.btnStart.style.pointerEvents = 'auto';
        this.btnStart.classList.remove('opacity-70');
    }

    destroy() {
        // Garbage Collector (GC) optimizasyonu: Sayfa değiştiğinde bu objenin DOM referansları koparılır.
        this.dropzone = null;
        this.fileInput = null;
        this.btnStart = null;
    }
}
