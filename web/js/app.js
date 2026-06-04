import { QueueManager } from './QueueManager.js';
import { Router } from './Router.js';
import { ConverterPage } from './pages/ConverterPage.js';
import { DocStationPage } from './pages/DocStationPage.js';
import { ResizerPage } from './pages/ResizerPage.js';
import { OptimizerPage } from './pages/OptimizerPage.js';
import { GifStudioPage } from './pages/GifStudioPage.js';
import { TextExtractPage } from './pages/TextExtractPage.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Init Sınıflar (Globaller Layout üzerine kurulu)
    const queueManager = new QueueManager('queue-container', 'queue-item-template');
    const router = new Router('page-content', queueManager);

    // 2. Sayfaları (Rotalar) sisteme tanıt
    router.addRoute('converter', 'pages/converter.html', ConverterPage);
    router.addRoute('doc_station', 'pages/doc_station.html', DocStationPage);
    router.addRoute('resizer', 'pages/resizer.html', ResizerPage);
    router.addRoute('optimizer', 'pages/optimizer.html', OptimizerPage);
    router.addRoute('gif_studio', 'pages/gif_studio.html', GifStudioPage);
    router.addRoute('text_extract', 'pages/text_extract.html', TextExtractPage);


    // 3. Menü Sekmesi tıklama görevleri
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Aktif renkleri temizle
            navTabs.forEach(t => {
                t.className = "nav-tab flex items-center gap-4 py-3 px-4 text-[#d0c5af] opacity-60 hover:opacity-100 hover:bg-[#353534] transition-colors duration-300 font-['Epilogue'] tracking-wider uppercase font-bold text-sm cursor-pointer";
            });

            // Tıklanana Noire stili sarı rengi ve sol barı ekle
            tab.className = "nav-tab flex items-center gap-4 py-3 px-4 text-[#f2ca50] border-l-2 border-[#f2ca50] bg-[#2a2a2a] transition-all font-['Epilogue'] tracking-wider uppercase font-bold text-sm cursor-pointer";
            
            // Asenkron Route sayfasını çek (Örn: pages/converter.html)
            const routeName = tab.getAttribute('data-route');
            router.navigate(routeName);
        });
    });

    // 4. Varsayılan olarak başlarken Converter sayfasını Layout içerisine yükle!
    router.navigate('converter');

    // 5. Modal Yönetimi
    const modals = {
        'help': document.getElementById('help-modal'),
        'settings': document.getElementById('settings-modal'),
        'profile': document.getElementById('profile-modal')
    };

    const openModal = (modalId) => {
        const modal = modals[modalId];
        if(!modal) return;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        setTimeout(() => {
            const content = modal.querySelector('.modal-content');
            if(content) {
                content.classList.remove('scale-95', 'opacity-0');
                content.classList.add('scale-100', 'opacity-100');
            }
        }, 10);
    };

    const closeModal = (modal) => {
        const content = modal.querySelector('.modal-content');
        if(content) {
            content.classList.remove('scale-100', 'opacity-100');
            content.classList.add('scale-95', 'opacity-0');
        }
        setTimeout(() => {
            modal.classList.remove('flex');
            modal.classList.add('hidden');
        }, 300);
    };

    // Modal Tetikleyici Eventleri
    const btnHelp = document.getElementById('btn-help');
    const btnSettings = document.getElementById('btn-settings');
    const btnProfile = document.getElementById('btn-profile');

    if(btnHelp) btnHelp.addEventListener('click', () => openModal('help'));
    if(btnSettings) btnSettings.addEventListener('click', () => openModal('settings'));
    if(btnProfile) btnProfile.addEventListener('click', () => openModal('profile'));

    // Modal Kapatma Tuşları ve Arkaplan tıklamaları
    Object.values(modals).forEach(modal => {
        if(!modal) return;
        const closeBtn = modal.querySelector('.modal-close');
        const backdrop = modal.querySelector('.modal-backdrop');
        if(closeBtn) closeBtn.addEventListener('click', () => closeModal(modal));
        if(backdrop) backdrop.addEventListener('click', () => closeModal(modal));
    });
});
