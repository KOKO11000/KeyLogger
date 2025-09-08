 // ---------- נתונים ואחסון ----------
    const STORAGE_KEY = 'devicesData_v2_mac';
    const todayYMD = () => new Date().toISOString().slice(0,10);

    /** מבנה פריט:
     * { id, mac, location, tags: [..], online: boolean, history: [ { date, summary, metrics } ] }
     */
    function loadDevices() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        try { return JSON.parse(raw); } catch {}
      }
      // Seed דמו ראשוני
      const seed = [
        { id:'PC-01', mac:'AA:BB:CC:11:22:33', location:'חדר עבודה', tags:['אימון','דסקטופ'], online:true, history:[
          { date: todayYMD(), summary:'אימון בוקר', metrics:{ sessions:2, words:420, wpm:36 } },
          { date: '2025-09-07', summary:'אימון ערב', metrics:{ sessions:1, words:200, wpm:32 } },
        ] },
        { id:'LAPTOP-17', mac:'00:1A:2B:3C:4D:5E', location:'סלון', tags:['נייד'], online:false, history:[
          { date: '2025-09-06', summary:'אימון כללי', metrics:{ sessions:1, words:150, wpm:28 } },
        ] },
        { id:'STUDIO-MINI', mac:'DE:AD:BE:EF:00:01', location:'סטודיו', tags:['טבלט'], online:true, history:[
          { date: todayYMD(), summary:'סקירה מהירה', metrics:{ sessions:1, words:120, wpm:30 } },
        ] },
      ];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(seed));
      return seed;
    }
    function saveDevices(list) { localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); }

    let devices = loadDevices();
    let selectedId = devices[0]?.id || null;

    // ---------- DOM refs ----------
    const listEl = document.getElementById('deviceList');
    const selNameEl = document.getElementById('selName');
    const qEl = document.getElementById('q');
    const panel = document.getElementById('panel');

    const btnDownloadAll = document.getElementById('btnDownloadAll');
    const btnAddDevice = document.getElementById('btnAddDevice');
    const btnHistory = document.getElementById('btnHistory');
    const btnMore = document.getElementById('btnMore');

    const deviceModal = document.getElementById('deviceModal');
    const deviceForm = document.getElementById('deviceForm');
    const deviceModalTitle = document.getElementById('deviceModalTitle');
    const mName = document.getElementById('mName');
    const mMac = document.getElementById('mMac');
    const mLocation = document.getElementById('mLocation');
    const mTags = document.getElementById('mTags');
    const mOnline = document.getElementById('mOnline');

    const moreModal = document.getElementById('moreModal');
    const toggleOnlineBtn = document.getElementById('toggleOnlineBtn');
    const renameBtn = document.getElementById('renameBtn');
    const changeMacBtn = document.getElementById('changeMacBtn');
    const retagBtn = document.getElementById('retagBtn');
    const deleteBtn = document.getElementById('deleteBtn');

    // ---------- עזר: MAC ----------
    function normalizeMac(s){
      const hex = (s||'').toUpperCase().replace(/[^0-9A-F]/g,'');
      if (hex.length !== 12) return null;
      return hex.match(/.{2}/g).join(':'); // AA:BB:CC:DD:EE:FF
    }

    // ---------- ציור הרשימה ----------
    function renderList() {
      listEl.innerHTML = '';
      const term = (qEl.value || '').trim().toLowerCase();
      devices.forEach(d => {
        const hay = [d.id, d.location, d.mac, ...(d.tags||[])].join(' ').toLowerCase();
        if (term && !hay.includes(term)) return;

        const li = document.createElement('li');
        li.className = 'device' + (d.id === selectedId ? ' is-selected' : '');
        li.tabIndex = 0; li.role = 'option'; li.dataset.id = d.id;
        li.innerHTML = `
          <span class="badge"><span class="dot ${d.online ? 'online':'offline'}" aria-hidden="true"></span> ${escapeHTML(d.id)}</span>
          <span class="muted"><span class="mac">${escapeHTML(d.mac)}</span> · ${escapeHTML(d.location || '—')}</span>
          <span class="tags">${(d.tags||[]).map(t => `<span class="tag">${escapeHTML(t)}</span>`).join('')}</span>
        `;
        li.addEventListener('click', () => selectDevice(d.id));
        listEl.appendChild(li);
      });
      updateActionsState();
    }

    function selectDevice(id) {
      selectedId = id;
      selNameEl.textContent = id || '—';
      const d = devices.find(x=>x.id===id);
      panel.innerHTML = d ? `בחרת <b>${escapeHTML(d.id)}</b>\nMAC: <span class="mac">${escapeHTML(d.mac)}</span>\nמיקום: ${escapeHTML(d.location||'—')}` : '—';
      renderList();
    }

    function updateActionsState() {
      const hasSel = !!devices.find(d => d.id === selectedId);
      btnHistory.disabled = !hasSel;
      btnMore.disabled = !hasSel;
      selNameEl.textContent = hasSel ? selectedId : '—';
    }

    qEl.addEventListener('input', renderList);

    // ---------- כפתור: הורדה — כל היומנים היומיים ----------
    btnDownloadAll.addEventListener('click', () => {
      const ymd = todayYMD();
      const todayPayload = devices.map(d => {
        const todays = (d.history||[]).filter(h => h.date === ymd);
        return { device: d.id, mac: d.mac, date: ymd, entries: todays };
      });
      const blob = new Blob([ JSON.stringify({ date: ymd, data: todayPayload }, null, 2) ], { type: 'application/json;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `daily_logs_${ymd}.json`;
      document.body.appendChild(a);
      a.click();
      URL.revokeObjectURL(a.href);
      a.remove();
      panel.textContent = `נוצר קובץ daily_logs_${ymd}.json עם יומנים של ${todayPayload.length} מחשבים.`;
    });

    // ---------- כפתור: הוספת מחשב ----------
    btnAddDevice.addEventListener('click', () => {
      deviceModalTitle.textContent = 'הוספת מחשב';
      mName.value = ''; mMac.value = ''; mLocation.value=''; mTags.value=''; mOnline.value='true';
      deviceModal.returnValue = '';
      deviceModal.showModal();
      setTimeout(() => mName.focus(), 50);
    });

    deviceForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const id = mName.value.trim();
      const macNorm = normalizeMac(mMac.value);
      if (!id) return alert('שם מחשב חובה');
      if (!macNorm) return alert('MAC לא תקין — ודאי שיש 12 תווים הקסדצימליים (0-9,A-F)');
      const macExists = devices.some(d => d.mac === macNorm && (!deviceModalTitle.textContent.includes('עריכת') || d.id !== selectedId));
      if (macExists) return alert('MAC כבר קיים ברשימה.');

      const payload = {
        id,
        mac: macNorm,
        location: mLocation.value.trim(),
        tags: mTags.value.split(',').map(s => s.trim()).filter(Boolean),
        online: mOnline.value === 'true',
        history: []
      };

      if (deviceModalTitle.textContent.includes('הוספת')) {
        const idExists = devices.some(d => d.id.toLowerCase() === id.toLowerCase());
        if (idExists) return alert('שם מחשב כבר קיים. בחרי שם אחר.');
        devices.push(payload);
        saveDevices(devices);
        selectDevice(id);
      } else {
        // מצב עריכה
        const idx = devices.findIndex(d => d.id === selectedId);
        if (idx >= 0) {
          devices[idx].id = payload.id;
          devices[idx].mac = payload.mac;
          devices[idx].location = payload.location;
          devices[idx].tags = payload.tags;
          devices[idx].online = payload.online;
          selectedId = payload.id;
          saveDevices(devices);
        }
      }
      deviceModal.close();
      renderList();
    });

    // ---------- כפתור: צפייה בהיסטוריה ----------
    btnHistory.addEventListener('click', () => {
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      const hist = d.history || [];
      if (hist.length === 0) {
        panel.textContent = `אין היסטוריה ל-${d.id}.`;
        return;
      }
      const byDate = groupBy(hist, x => x.date);
      const lines = [`היסטוריה עבור ${d.id} (MAC ${d.mac}):`];
      Object.keys(byDate).sort().forEach(dt => {
        const arr = byDate[dt];
        const sumSessions = arr.reduce((a,c)=>a+(c.metrics?.sessions||0),0);
        const sumWords = arr.reduce((a,c)=>a+(c.metrics?.words||0),0);
        const avgWpm = avg(arr.map(x=>x.metrics?.wpm).filter(n=>Number.isFinite(n)));
        lines.push(`• ${dt} — סשנים: ${sumSessions}, מילים: ${sumWords}, WPM ממוצע: ${avgWpm ?? '—'}`);
      });
      lines.push('', 'הורד/י JSON של ההיסטוריה למחשב זה:');
      panel.innerHTML = escapeHTML(lines.join('\n')) + '\n';
      const btn = document.createElement('button');
      btn.className = 'btn';
      btn.textContent = 'הורדת היסטוריה (JSON)';
      btn.addEventListener('click', () => {
        const blob = new Blob([ JSON.stringify({ device: d.id, mac: d.mac, history: d.history }, null, 2) ], { type: 'application/json;charset=utf-8' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `history_${d.id}.json`;
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(a.href);
        a.remove();
      });
      panel.appendChild(btn);
    });

    // ---------- כפתור: עוד אפשרויות ----------
    btnMore.addEventListener('click', () => {
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      moreModal.showModal();
    });

    // פעולות במודאל "עוד אפשרויות"
    toggleOnlineBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const idx = devices.findIndex(x => x.id === selectedId);
      if (idx < 0) return;
      devices[idx].online = !devices[idx].online;
      saveDevices(devices);
      renderList();
    });

    renameBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      const nv = prompt('שם חדש למחשב:', d.id);
      if (!nv) return;
      if (devices.some(x => x.id.toLowerCase() === nv.toLowerCase() && x !== d)) {
        alert('שם זה כבר קיים.');
        return;
      }
      d.id = nv.trim();
      selectedId = d.id;
      saveDevices(devices);
      renderList();
    });

    changeMacBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      const nvRaw = prompt('MAC חדש (אפשר להדביק בכל פורמט):', d.mac);
      if (nvRaw == null) return;
      const macNorm = normalizeMac(nvRaw);
      if (!macNorm) return alert('MAC לא תקין — 12 ספרות/אותיות HEX (0-9, A-F).');
      if (devices.some(x => x.mac === macNorm && x !== d)) {
        return alert('MAC זה כבר קיים ברשימה.');
      }
      d.mac = macNorm;
      saveDevices(devices);
      renderList();
    });

    retagBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      const loc = prompt('מיקום:', d.location || '');
      const tags = prompt('תגיות מופרדות בפסיק:', (d.tags||[]).join(', '));
      d.location = (loc||'').trim();
      d.tags = (tags||'').split(',').map(s=>s.trim()).filter(Boolean);
      saveDevices(devices);
      renderList();
    });

    deleteBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      if (!confirm(`למחוק את "${d.id}"? אי אפשר לבטל.`)) return;
      devices = devices.filter(x => x !== d);
      saveDevices(devices);
      selectedId = devices[0]?.id || null;
      panel.textContent = 'נמחק. בחרי מחשב אחר מהרשימה.';
      renderList();
    });

    // ---------- עזר ----------
    function groupBy(arr, keyFn){ return arr.reduce((m,x)=>{ const k=keyFn(x); (m[k]=m[k]||[]).push(x); return m; }, {}); }
    function avg(arr){ if(!arr.length) return null; const sum=arr.reduce((a,c)=>a+Number(c||0),0); return Math.round((sum/arr.length)*10)/10; }
    function escapeHTML(str){ return (str??'').toString().replace(/[&<>"']/g, s=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[s])); }

    // עריכת מחשב קיים דרך מודאל "הוספה" (ממלא גם MAC)
    function editCurrentViaModal(){
      const d = devices.find(x => x.id === selectedId);
      if (!d) return;
      deviceModalTitle.textContent = 'עריכת מחשב';
      mName.value = d.id;
      mMac.value = d.mac;
      mLocation.value = d.location || '';
      mTags.value = (d.tags||[]).join(', ');
      mOnline.value = d.online ? 'true':'false';
      deviceModal.showModal();
    }

    // פתיחת עריכה בדאבל-קליק
    listEl.addEventListener('dblclick', (e) => {
      const li = e.target.closest('.device');
      if (!li) return;
      selectDevice(li.dataset.id);
      editCurrentViaModal();
    });

    // ---------- אתחול ----------
    function renderEmptyHint(){
      panel.textContent = 'אין מחשבים. לחצי "הוספת מחשב" כדי להתחיל.';
    }
    function init(){
      if (selectedId) selNameEl.textContent = selectedId;
      renderList();
      if (!devices.length) renderEmptyHint();
    }
    init();