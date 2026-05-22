// ==UserScript==
// @name         HKT Ticket Helper
// @namespace    hkt-ticket-helper
// @version      3.0
// @description  Semi-auto ticket helper for HKT Ticketing
// @match        *://*/*
// @run-at       document-idle
// @noframes
// @charset      UTF-8
// ==/UserScript==

(function () {
    'use strict';

    // Only run on hkt.hkticketing.com
    if (window.location.hostname !== 'hkt.hkticketing.com') return;

    console.log('[HKT] Running on: ' + window.location.href);

    // ============================
    // CONFIG
    // ============================
    var CONFIG = {
        projectId: '50000001244002',
        eventName: 'The Weeknd: After Hours Til Dawn Tour',
        saleStartTime: '2026-05-21T10:00:00+08:00',
        preferZones: ['VIP', 'Standing', 'Floor', '1680', '1280', '980', '680'],
        ticketCount: 2,
        refreshIntervalBeforeSale: 2000,
        refreshIntervalAfterSale: 500,
        startRefreshBeforeSale: 120,
        buyerInfo: { name: '', phone: '', email: '', idNumber: '' },
        autoSubmit: false,
        playSound: true,
        debug: true
    };

    var P = '[HKT]';
    function log() { if (!CONFIG.debug) return; var a = [P].concat([].slice.call(arguments)); console.log.apply(console, a); }
    function warn() { var a = [P].concat([].slice.call(arguments)); console.warn.apply(console, a); }

    function getTimeUntilSale() { return new Date(CONFIG.saleStartTime).getTime() - Date.now(); }

    function setInputValue(input, value) {
        var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(input, value);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function humanClick(el, delay) {
        delay = delay || 50;
        return new Promise(function (r) {
            setTimeout(function () {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                setTimeout(function () {
                    el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                    el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                    el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                    log('Clicked:', (el.textContent || '').trim().substring(0, 40));
                    r();
                }, delay + Math.random() * 80);
            }, delay);
        });
    }

    function playAlert() {
        if (!CONFIG.playSound) return;
        try {
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            [523.25, 659.25, 783.99, 1046.50].forEach(function (f, i) {
                var o = ctx.createOscillator(), g = ctx.createGain();
                o.connect(g); g.connect(ctx.destination);
                o.frequency.value = f; o.type = 'sine'; g.gain.value = 0.3;
                o.start(ctx.currentTime + i * 0.15); o.stop(ctx.currentTime + i * 0.15 + 0.15);
            });
        } catch (e) {}
    }

    var state = { phase: 'idle', attemptCount: 0 };

    function selectZone() {
        log('Selecting zone...'); state.phase = 'selecting';
        var all = document.querySelectorAll(
            '[class*="zone"],[class*="price"],[class*="ticket"],[class*="area"],' +
            '[class*="seat"],[class*="grade"],[class*="section"],[class*="block"],[class*="tier"]'
        );
        log('Zone elements: ' + all.length);
        for (var p = 0; p < CONFIG.preferZones.length; p++) {
            var nm = CONFIG.preferZones[p].toLowerCase();
            for (var i = 0; i < all.length; i++) {
                var t = (all[i].textContent || '').toLowerCase();
                if (t.indexOf(nm) !== -1) {
                    if (all[i].classList.contains('disabled') || all[i].classList.contains('sold-out') ||
                        all[i].classList.contains('unavailable') || all[i].querySelector('.sold-out,.disabled,[disabled]')) {
                        log('Zone ' + CONFIG.preferZones[p] + ' sold out');
                        continue;
                    }
                    log('Selected: ' + CONFIG.preferZones[p]);
                    humanClick(all[i]); return true;
                }
            }
        }
        warn('No zone matched'); return false;
    }

    function selectQuantity() {
        log('Setting qty: ' + CONFIG.ticketCount);
        var inp = document.querySelector('input[class*="qty"],input[class*="number"],input[class*="count"],input[type="number"]');
        if (inp) { setInputValue(inp, '' + CONFIG.ticketCount); return; }
        var plus = document.querySelector('[class*="plus"],[class*="increase"]');
        if (plus) { for (var i = 1; i < CONFIG.ticketCount; i++) humanClick(plus, 100); }
    }

    function fillBuyerInfo() {
        log('Filling info...'); state.phase = 'filling';
        var map = { name:['name','fullName','realName','contactName'], phone:['phone','mobile','tel','contactPhone'], email:['email','mail','contactEmail'], idNumber:['id','identity','passport','idCard'] };
        for (var key in map) {
            if (!map.hasOwnProperty(key)) continue;
            var val = CONFIG.buyerInfo[key]; if (!val) continue;
            var found = false;
            for (var k = 0; k < map[key].length && !found; k++) {
                var kw = map[key][k];
                var sels = ['input[name*="'+kw+'" i]','input[placeholder*="'+kw+'" i]','input[aria-label*="'+kw+'" i]','input[class*="'+kw+'" i]','input[id*="'+kw+'" i]'];
                for (var s = 0; s < sels.length; s++) {
                    var inp = document.querySelector(sels[s]);
                    if (inp && !inp.value) { setInputValue(inp, val); log('Filled ' + key); found = true; break; }
                }
            }
            if (!found) warn('Not found: ' + key);
        }
    }

    function submitOrder() {
        log('Looking for submit...'); state.phase = 'submitting';
        var sels = ['button[class*="submit"]','button[class*="confirm"]','button[class*="purchase"]','button[class*="buy"]','button[class*="order"]','button[class*="next"]','button[type="submit"]'];
        for (var i = 0; i < sels.length; i++) {
            var btn = document.querySelector(sels[i]);
            if (btn && !btn.disabled) {
                if (CONFIG.autoSubmit) { log('AUTO SUBMIT!'); humanClick(btn); playAlert(); }
                else {
                    log('Ready! Highlighted button');
                    btn.style.cssText = 'outline:4px solid #ff4444!important;outline-offset:2px!important;animation:blink 0.5s infinite;';
                    playAlert();
                    if (!document.getElementById('hkt-blink')) {
                        var st = document.createElement('style'); st.id = 'hkt-blink';
                        st.textContent = '@keyframes blink{50%{outline-color:transparent}}';
                        document.head.appendChild(st);
                    }
                }
                return true;
            }
        }
        warn('Submit not found'); return false;
    }

    function interceptRequests() {
        var origOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function (m, u) {
            if (u && (u.indexOf('api')!==-1||u.indexOf('ticket')!==-1||u.indexOf('order')!==-1||u.indexOf('project')!==-1||u.indexOf('activity')!==-1||u.indexOf('seat')!==-1)) log('[XHR] '+m+' '+u);
            return origOpen.apply(this, arguments);
        };
        if (window.fetch) {
            var origFetch = window.fetch;
            window.fetch = function (input, init) {
                var u = typeof input==='string'?input:(input&&input.url);
                if (u && (u.indexOf('api')!==-1||u.indexOf('ticket')!==-1||u.indexOf('order')!==-1||u.indexOf('project')!==-1||u.indexOf('activity')!==-1||u.indexOf('seat')!==-1)) log('[Fetch] '+(init&&init.method||'GET')+' '+u);
                return origFetch.apply(this, arguments);
            };
        }
        log('Interceptor active');
    }

    function mainLoop() {
        var ms = getTimeUntilSale();
        if (ms > CONFIG.startRefreshBeforeSale * 1000) {
            if (state.attemptCount % 60 === 0) log('Waiting... ' + Math.round(ms/60000) + ' min');
            state.attemptCount++;
            setTimeout(mainLoop, 10000);
            return;
        }
        if (ms > -60000) {
            state.phase = 'refreshing'; state.attemptCount++;
            log('Refresh #' + state.attemptCount + ' (' + Math.round(ms/1000) + 's)');
            location.reload();
            setTimeout(mainLoop, ms > 0 ? CONFIG.refreshIntervalBeforeSale : CONFIG.refreshIntervalAfterSale);
            return;
        }
        log('>>> SALE! <<<');
        try {
            if (!selectZone()) { setTimeout(mainLoop, CONFIG.refreshIntervalAfterSale); return; }
            selectQuantity();
            var nb = document.querySelector('button[class*="next"],button[class*="buy"],button[class*="purchase"],button[class*="select"],button[class*="confirm"]');
            if (nb) {
                humanClick(nb);
                setTimeout(function () { fillBuyerInfo(); submitOrder(); state.phase = 'done'; log('DONE!'); }, 1500);
            } else {
                fillBuyerInfo(); submitOrder(); state.phase = 'done'; log('DONE!');
            }
        } catch (err) { console.error(P, err); setTimeout(mainLoop, CONFIG.refreshIntervalAfterSale); }
    }

    function analyzePage() {
        console.group('=== HKT Analysis ===');
        var btns = document.querySelectorAll('button,[role="button"],a[class*="btn"]');
        log('Buttons: ' + btns.length);
        for (var i = 0; i < btns.length; i++) { var b = btns[i]; console.log('  BTN[' + i + '] "' + (b.textContent || '').trim().substring(0, 50) + '" cls=' + b.className, b); }
        var inps = document.querySelectorAll('input,select,textarea');
        log('Inputs: ' + inps.length);
        for (var j = 0; j < inps.length; j++) { var inp = inps[j]; console.log('  INP[' + j + ']', { type: inp.type, name: inp.name, ph: inp.placeholder, cls: inp.className, id: inp.id }); }
        var zones = document.querySelectorAll('[class*="zone"],[class*="price"],[class*="ticket"],[class*="area"],[class*="seat"],[class*="section"]');
        log('Zones: ' + zones.length);
        for (var k = 0; k < zones.length; k++) { console.log('  ZONE[' + k + '] "' + (zones[k].textContent || '').trim().substring(0, 80) + '" cls=' + zones[k].className, zones[k]); }
        var res = performance.getEntriesByType('resource').filter(function (r) { return r.initiatorType === 'xmlhttprequest' || r.initiatorType === 'fetch'; });
        log('API requests: ' + res.length);
        for (var m = 0; m < res.length; m++) console.log('  API[' + m + '] ' + res[m].name);
        console.groupEnd();
    }

    // ============================
    // PANEL
    // ============================
    function createPanel() {
        var old = document.getElementById('hkt-p');
        if (old) old.remove();

        var css = '#hkt-p{position:fixed;top:10px;right:10px;z-index:2147483646;background:rgba(0,0,0,0.92);color:#fff;padding:16px 20px;border-radius:12px;font-family:Arial,sans-serif;font-size:13px;min-width:280px;box-shadow:0 4px 20px rgba(0,0,0,0.5)}#hkt-p h3{margin:0 0 12px;font-size:15px}#hkt-p .r{display:flex;justify-content:space-between;padding:3px 0;font-size:12px}#hkt-p .l{color:#aaa}#hkt-p .v{color:#fff;font-weight:500}#hkt-p .vr{color:#4fc3f7}#hkt-p .vg{color:#66bb6a}#hkt-p .b{width:100%;margin-top:8px;padding:8px;border:none;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600}#hkt-p .b:active{transform:scale(0.97)}#hkt-p .bg{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}#hkt-p .bp{background:linear-gradient(135deg,#f093fb,#f5576c);color:#fff}#hkt-p .bx{background:0 0;color:#888;width:auto;margin:0;padding:0 4px;font-size:16px;position:absolute;top:8px;right:12px}';
        var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

        var d = document.createElement('div'); d.id = 'hkt-p';
        d.innerHTML = '<button class="bx" id="hkt-x">-</button>' +
            '<h3>HKT Ticket Helper</h3>' +
            '<div class="r"><span class="l">Event</span><span class="v" style="max-width:180px;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + CONFIG.eventName + '</span></div>' +
            '<div class="r"><span class="l">Status</span><span class="v" id="hkt-s">Idle</span></div>' +
            '<div class="r"><span class="l">Countdown</span><span class="v" id="hkt-t">--:--:--</span></div>' +
            '<div class="r"><span class="l">Attempts</span><span class="v" id="hkt-n">0</span></div>' +
            '<div class="r"><span class="l">Zones</span><span class="v">' + CONFIG.preferZones.join(' > ') + '</span></div>' +
            '<div class="r"><span class="l">Qty</span><span class="v">' + CONFIG.ticketCount + '</span></div>' +
            '<button class="b bg" id="hkt-go">START</button>' +
            '<button class="b bp" id="hkt-a">Analyze Page</button>';
        document.body.appendChild(d);

        setInterval(function () {
            var el = document.getElementById('hkt-t'); if (!el) return;
            var ms = getTimeUntilSale();
            if (ms > 0) {
                var h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000), s = Math.floor((ms % 60000) / 1000);
                el.textContent = (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
                el.className = 'v';
            } else { el.textContent = 'ON SALE!'; el.className = 'v vr'; }
        }, 1000);

        setInterval(function () {
            var se = document.getElementById('hkt-s'), ne = document.getElementById('hkt-n');
            if (se) {
                var mp = { idle: 'Idle', refreshing: 'Refreshing...', selecting: 'Selecting...', filling: 'Filling...', submitting: 'Submitting...', done: 'DONE!' };
                se.textContent = mp[state.phase] || state.phase;
                se.className = 'v' + (state.phase === 'done' ? ' vg' : state.phase !== 'idle' ? ' vr' : '');
            }
            if (ne) ne.textContent = state.attemptCount;
        }, 500);

        document.getElementById('hkt-go').addEventListener('click', function () { log('START!'); mainLoop(); });
        document.getElementById('hkt-a').addEventListener('click', function () { analyzePage(); });

        var min = false;
        document.getElementById('hkt-x').addEventListener('click', function () {
            min = !min;
            var ch = d.querySelectorAll(':scope > div, :scope > button:not(.bx)');
            for (var i = 0; i < ch.length; i++) ch[i].style.display = min ? 'none' : '';
            document.getElementById('hkt-x').textContent = min ? '+' : '-';
        });

        log('Panel ready!');
    }

    // ============================
    // INIT
    // ============================
    interceptRequests();
    createPanel();
    log('All systems go. URL: ' + window.location.href);

    // Watch for SPA URL changes
    var lastUrl = window.location.href;
    setInterval(function () {
        if (window.location.href !== lastUrl) {
            lastUrl = window.location.href;
            log('URL changed: ' + lastUrl);
            setTimeout(createPanel, 800);
        }
    }, 500);

})();
