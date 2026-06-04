export class Router {
    constructor(contentContainerId, queueManager) {
        this.contentContainer = document.getElementById(contentContainerId);
        this.queueManager = queueManager;
        this.routes = {}; // routeName -> { url: '', ControllerClass: Class }
        this.activeController = null;
    }

    addRoute(routeName, htmlUrl, ControllerClass) {
        this.routes[routeName] = { url: htmlUrl, ControllerClass };
    }

    async navigate(routeName) {
        const route = this.routes[routeName];
        if (!route) {
            this.contentContainer.innerHTML = `<div class="p-8 text-[#d0c5af]"><h2 class="text-3xl font-headline">404 - Modül Henüz Aktif Değil</h2><p class="mt-4 font-light opacity-60">Bu sayfa ('${routeName}') henüz koda dökülmedi.</p></div>`;
            return;
        }

        // Fade out
        this.contentContainer.style.opacity = '0';
        
        try {
            // Statik dosyayı lokalde fetch ile çağırıyoruz. (CORS hatası almamak için Live Server / FastAPI şart)
            const response = await fetch(route.url);
            if (!response.ok) throw new Error("HTTP error " + response.status);
            const html = await response.text();
            
            // Eski denetleyiciyi (Controller) çöpe at (Memory Cleanup)
            if (this.activeController && typeof this.activeController.destroy === 'function') {
                this.activeController.destroy();
            }

            // HTML'i sayfaya enjekte et (Animasyon zamanlaması)
            setTimeout(() => {
                try {
                    this.contentContainer.innerHTML = html;
                    
                    // Yeni denetleyiciyi ayaklandır
                    if (route.ControllerClass) {
                        this.activeController = new route.ControllerClass(this.queueManager);
                        this.activeController.init();
                    }
                } catch(inErr) {
                    console.error("Controller Init Hatası:", inErr);
                    this.contentContainer.innerHTML += `<div class="p-4 bg-error text-black m-4 rounded"><b>JS Error:</b> ${inErr.message} <br> ${inErr.stack}</div>`;
                } finally {
                    // Fade in (Her durumda görünür yap)
                    this.contentContainer.style.opacity = '1';
                }
            }, 300);
            
        } catch (err) {
            console.error("Router Fetch Hatası:", err);
            this.contentContainer.style.opacity = '1';
            this.contentContainer.innerHTML = `
                <div class="p-8 mt-10 text-center text-error border border-error/20 bg-error/5 rounded-xl max-w-2xl mx-auto">
                    <span class="material-symbols-outlined text-5xl mb-4">gpp_bad</span>
                    <h2 class="text-2xl font-bold font-headline">Same-Origin (CORS) Hatası veya Dosya Yüklenemedi</h2>
                    <p class="text-sm opacity-80 mt-4 leading-relaxed">${err.message}<br/>Dinamik JavaScript modüllerini (ES6) ve yerel HTML dosyalarını tarayıcıya <b>çift tıklayarak (\`file:///\`)</b> açtınız. SPA mimarisi güvenlik gereği bunu engeller. <br/><br/>Lütfen VS Code <b>Live Server</b> eklentisini veya <b>FastAPI</b> sunucunuzu kullanınız.</p>
                </div>`;
        }
    }
}
