import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r'C:\antigravity\115-10-27-28back'
json_path = os.path.join(target_dir, 'gallery_data.json')

with open(json_path, encoding='utf-8') as f:
    gallery_data = json.load(f)

total_images_count = sum(len(gallery_data[k]['items']) for k in gallery_data)
json_str = json.dumps(gallery_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>南投國中 115學年度國二隔宿露營 · 尖山埤探索相簿</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --accent: #f59e0b;
      --accent-glow: rgba(245, 158, 11, 0.25);
      --badge-bg: rgba(59, 130, 246, 0.15);
      --badge-border: rgba(59, 130, 246, 0.3);
      --radius: 14px;
      --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Top Banner / Hero */
    .hero {{
      background: radial-gradient(circle at 50% 20%, #1e3a8a 0%, #0f172a 75%);
      border-bottom: 1px solid var(--card-border);
      padding: 48px 20px 32px;
      text-align: center;
      position: relative;
    }}

    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-glow);
      color: var(--accent);
      border: 1px solid var(--accent);
      padding: 6px 16px;
      border-radius: 9999px;
      font-size: 0.88rem;
      font-weight: 600;
      margin-bottom: 16px;
    }}

    .hero h1 {{
      font-size: clamp(1.8rem, 4vw, 2.7rem);
      font-weight: 800;
      letter-spacing: -0.5px;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #ffffff 40%, #93c5fd 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero p {{
      color: var(--text-muted);
      font-size: clamp(0.95rem, 2vw, 1.15rem);
      max-width: 750px;
      margin: 0 auto 24px;
    }}

    /* Global Stats Pills */
    .stats-container {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
      margin-bottom: 24px;
    }}

    .stat-pill {{
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid var(--card-border);
      padding: 8px 18px;
      border-radius: 9999px;
      font-size: 0.88rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .stat-pill strong {{
      color: var(--primary);
    }}

    /* Search Bar */
    .search-box-wrapper {{
      max-width: 580px;
      margin: 0 auto;
      position: relative;
    }}

    .search-box {{
      width: 100%;
      padding: 14px 20px 14px 46px;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid var(--card-border);
      border-radius: 9999px;
      color: var(--text);
      font-size: 1rem;
      outline: none;
      transition: var(--transition);
      backdrop-filter: blur(8px);
    }}

    .search-box:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
    }}

    .search-icon {{
      position: absolute;
      left: 18px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 1.1rem;
      pointer-events: none;
    }}

    /* Main Container */
    .container {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 32px 20px;
      flex: 1;
      width: 100%;
    }}

    /* Level 1 Tabs (9 Subfolders) */
    .tabs-header {{
      margin-bottom: 24px;
    }}

    .tabs-label {{
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .tabs-nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--card-border);
    }}

    .tab-btn {{
      background: var(--card-bg);
      color: var(--text-muted);
      border: 1px solid var(--card-border);
      padding: 10px 18px;
      border-radius: 12px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      user-select: none;
    }}

    .tab-btn:hover {{
      background: #334155;
      color: var(--text);
      transform: translateY(-1px);
    }}

    .tab-btn.active {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: #ffffff;
      border-color: #3b82f6;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }}

    .tab-badge {{
      background: rgba(255, 255, 255, 0.2);
      font-size: 0.78rem;
      padding: 2px 7px;
      border-radius: 9999px;
      font-weight: 700;
    }}

    /* Subfolder Info Banner */
    .subfolder-info-bar {{
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 14px 20px;
      margin-top: 16px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .subfolder-info-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .subfolder-icon {{
      font-size: 1.6rem;
    }}

    .subfolder-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
    }}

    .subfolder-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
    }}

    /* Level 2 Sub-activity Pills */
    .filter-pills-wrapper {{
      margin-bottom: 28px;
    }}

    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .pill-btn {{
      background: rgba(15, 23, 42, 0.8);
      color: var(--text-muted);
      border: 1px solid var(--card-border);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .pill-btn:hover {{
      color: var(--text);
      border-color: var(--primary);
    }}

    .pill-btn.active {{
      background: var(--accent);
      color: #0f172a;
      border-color: var(--accent);
      font-weight: 700;
    }}

    .pill-count {{
      font-size: 0.75rem;
      background: rgba(0, 0, 0, 0.25);
      padding: 1px 6px;
      border-radius: 9999px;
    }}

    /* Active filter indicator */
    .filter-status {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-bottom: 16px;
      padding: 0 4px;
    }}

    /* Photo Grid */
    .photo-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 22px;
    }}

    .photo-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: var(--transition);
      position: relative;
    }}

    .photo-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(59, 130, 246, 0.6);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
    }}

    .media-thumb-box {{
      position: relative;
      width: 100%;
      height: 230px;
      background: #090d16;
      cursor: pointer;
      overflow: hidden;
    }}

    .media-thumb {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
      display: block;
    }}

    .photo-card:hover .media-thumb {{
      transform: scale(1.05);
    }}

    .video-badge {{
      position: absolute;
      top: 12px;
      left: 12px;
      background: rgba(220, 38, 38, 0.85);
      color: #ffffff;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 700;
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .zoom-overlay {{
      position: absolute;
      inset: 0;
      background: rgba(15, 23, 42, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: var(--transition);
    }}

    .photo-card:hover .zoom-overlay {{
      opacity: 1;
    }}

    .zoom-btn-icon {{
      background: rgba(255, 255, 255, 0.9);
      color: #0f172a;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}

    .card-body {{
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .card-meta {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
    }}

    .tag-act {{
      background: rgba(59, 130, 246, 0.2);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.4);
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
    }}

    .tag-time {{
      color: var(--text-muted);
      font-size: 0.78rem;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .tag-seq {{
      color: #a78bfa;
      background: rgba(167, 139, 250, 0.15);
      border: 1px solid rgba(167, 139, 250, 0.3);
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      margin-left: auto;
    }}

    .card-caption {{
      color: #e2e8f0;
      font-size: 0.92rem;
      line-height: 1.5;
      margin-bottom: 14px;
      flex: 1;
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 0.8rem;
    }}

    .file-tag {{
      color: var(--text-muted);
      font-family: monospace;
      font-size: 0.74rem;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 180px;
    }}

    .btn-download {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: var(--transition);
    }}

    .btn-download:hover {{
      color: #93c5fd;
      text-decoration: underline;
    }}

    /* Lightbox Modal */
    .lightbox-modal {{
      position: fixed;
      inset: 0;
      background: rgba(10, 15, 29, 0.95);
      backdrop-filter: blur(12px);
      z-index: 9999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .lightbox-modal.active {{
      display: flex;
    }}

    .lightbox-container {{
      max-width: 1100px;
      width: 100%;
      max-height: 94vh;
      background: #1e293b;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }}

    .lightbox-header {{
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--card-border);
      background: #0f172a;
    }}

    .lightbox-header-title {{
      font-weight: 700;
      font-size: 1rem;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .lightbox-close {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.6rem;
      cursor: pointer;
      line-height: 1;
      padding: 4px 8px;
      border-radius: 6px;
      transition: var(--transition);
    }}

    .lightbox-close:hover {{
      color: #ffffff;
      background: #334155;
    }}

    .lightbox-media-box {{
      flex: 1;
      min-height: 280px;
      max-height: 65vh;
      background: #000000;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}

    .lightbox-img {{
      max-width: 100%;
      max-height: 65vh;
      object-fit: contain;
    }}

    .lightbox-video {{
      max-width: 100%;
      max-height: 65vh;
    }}

    .lightbox-nav {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      cursor: pointer;
      transition: var(--transition);
      user-select: none;
    }}

    .lightbox-nav:hover {{
      background: var(--primary);
    }}

    .lightbox-prev {{ left: 16px; }}
    .lightbox-next {{ right: 16px; }}

    .lightbox-footer {{
      padding: 18px 24px;
      background: #0f172a;
      border-top: 1px solid var(--card-border);
    }}

    .lightbox-caption {{
      font-size: 1rem;
      color: #f1f5f9;
      line-height: 1.6;
      margin-bottom: 10px;
    }}

    .lightbox-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    /* Empty state */
    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
    }}
    .empty-state-icon {{
      font-size: 3rem;
      margin-bottom: 12px;
    }}

    /* Floating Back to Top Button */
    .back-to-top {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 46px;
      height: 46px;
      background: var(--primary);
      color: #ffffff;
      border: none;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.3rem;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
      opacity: 0;
      pointer-events: none;
      transition: var(--transition);
      z-index: 100;
    }}

    .back-to-top.visible {{
      opacity: 1;
      pointer-events: auto;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--card-border);
      background: #090d16;
      padding: 28px 20px;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.9rem;
    }}

    footer a {{
      color: var(--primary);
      text-decoration: none;
    }}
  </style>
</head>
<body>

  <!-- Top Hero -->
  <header class="hero">
    <div class="hero-badge">南投縣立南投國民中學 · 115學年度隔宿露營</div>
    <h1>尖山埤探索紀實 · 班級隊輔與探索相簿</h1>
    <p>台南柳營尖山埤江南渡假村兩天一夜探索回顧 · 9大班級隊輔與探索分站精彩紀實</p>
    
    <div class="stats-container">
      <div class="stat-pill">📷 總收錄 <strong>{total_images_count}</strong> 張相片與影音</div>
      <div class="stat-pill">🏷️ <strong>9</strong> 大主題班級標籤</div>
      <div class="stat-pill">⛺ <strong>12</strong> 項完整露營行程</div>
      <div class="stat-pill">✨ <strong>AI 辨識</strong> 內容文字說明</div>
    </div>

    <!-- Search Input -->
    <div class="search-box-wrapper">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" class="search-box" placeholder="搜尋活動（如：營火晚會、烤肉、帳棚、獨木橋、班級...）">
    </div>
  </header>

  <!-- Main Container -->
  <main class="container">
    
    <!-- Level 1 Tabs (9 Subfolders) -->
    <div class="tabs-header">
      <div class="tabs-label">第一層分類 · 選擇班級或探索專區</div>
      <nav class="tabs-nav" id="subfolderTabs">
        <!-- Generated by JS -->
      </nav>
    </div>

    <!-- Selected Subfolder Info Bar -->
    <div class="subfolder-info-bar" id="subfolderInfoBar">
      <div class="subfolder-info-left">
        <span class="subfolder-icon" id="infoIcon">⛺</span>
        <div>
          <div class="subfolder-title" id="infoTitle">201 三元</div>
          <div class="subfolder-desc" id="infoDesc">201 班與隊輔三元哥哥的精彩生活日誌</div>
        </div>
      </div>
      <div class="stat-pill" id="infoCountPill">
        共 <strong id="infoCount">0</strong> 張照片
      </div>
    </div>

    <!-- Level 2 Sub-activity Pills -->
    <div class="filter-pills-wrapper">
      <div class="tabs-label">第二層分類 · 依活動項目篩選</div>
      <div class="filter-pills" id="activityPills">
        <!-- Generated by JS -->
      </div>
    </div>

    <!-- Filter Status -->
    <div class="filter-status">
      <div>目前顯示：<strong id="currentFilterLabel">全部</strong> (<span id="visibleCount">0</span> 張)</div>
      <div id="activeSubfolderLabel" style="font-weight: 600; color: var(--accent);"></div>
    </div>

    <!-- Photo Grid -->
    <div class="photo-grid" id="photoGrid">
      <!-- Generated by JS -->
    </div>

    <!-- Empty State -->
    <div class="empty-state" id="emptyState" style="display: none;">
      <div class="empty-state-icon">🔍</div>
      <h3>查無符合條件的照片或影音</h3>
      <p style="margin-top: 6px;">請嘗試更換搜尋關鍵字或切換其他活動標籤！</p>
    </div>

  </main>

  <!-- Lightbox Modal -->
  <div class="lightbox-modal" id="lightboxModal">
    <div class="lightbox-container">
      <div class="lightbox-header">
        <div class="lightbox-header-title">
          <span id="lbBadge" class="tag-act">活動</span>
          <span id="lbTitle">檔名</span>
          <span id="lbSeq" class="tag-seq">#01</span>
        </div>
        <button class="lightbox-close" id="lbClose">&times;</button>
      </div>

      <div class="lightbox-media-box">
        <img id="lbImg" class="lightbox-img" src="" alt="放大照片" style="display: none;">
        <video id="lbVideo" class="lightbox-video" controls style="display: none;"></video>
        <button class="lightbox-nav lightbox-prev" id="lbPrev">&#10094;</button>
        <button class="lightbox-nav lightbox-next" id="lbNext">&#10095;</button>
      </div>

      <div class="lightbox-footer">
        <div class="lightbox-caption" id="lbCaption">照片說明文字</div>
        <div class="lightbox-actions">
          <div><span id="lbTime">時間</span> · <span id="lbFolder">班級</span></div>
          <a id="lbDownload" href="#" class="btn-download" download>下載原圖 ⬇</a>
        </div>
      </div>
    </div>
  </div>

  <!-- Back to Top Button -->
  <button class="back-to-top" id="backToTop" title="回到頂部">↑</button>

  <!-- Footer -->
  <footer>
    <p>南投縣立南投國民中學 115學年度二年級隔宿露營精彩相片輯 · 尖山埤江南渡假村</p>
    <p style="font-size: 0.82rem; margin-top: 6px; opacity: 0.8;">兩天一夜童軍野營、山訓探索教育、BBQ烤肉與營火晚會全紀錄</p>
  </footer>

  <!-- Embedded Data Script -->
  <script>
    const GALLERY_DATA = {json_str};

    // State
    const subfolderKeys = Object.keys(GALLERY_DATA);
    let currentSubfolder = subfolderKeys[0] || '201 三元';
    let currentActivity = 'ALL';
    let searchQuery = '';
    let currentFilteredList = [];
    let currentLightboxIndex = 0;

    // DOM Elements
    const subfolderTabs = document.getElementById('subfolderTabs');
    const activityPills = document.getElementById('activityPills');
    const photoGrid = document.getElementById('photoGrid');
    const searchInput = document.getElementById('searchInput');
    const emptyState = document.getElementById('emptyState');
    const visibleCount = document.getElementById('visibleCount');
    const currentFilterLabel = document.getElementById('currentFilterLabel');
    const activeSubfolderLabel = document.getElementById('activeSubfolderLabel');

    // Info Bar Elements
    const infoIcon = document.getElementById('infoIcon');
    const infoTitle = document.getElementById('infoTitle');
    const infoDesc = document.getElementById('infoDesc');
    const infoCount = document.getElementById('infoCount');

    // Lightbox Elements
    const lightboxModal = document.getElementById('lightboxModal');
    const lbClose = document.getElementById('lbClose');
    const lbImg = document.getElementById('lbImg');
    const lbVideo = document.getElementById('lbVideo');
    const lbPrev = document.getElementById('lbPrev');
    const lbNext = document.getElementById('lbNext');
    const lbBadge = document.getElementById('lbBadge');
    const lbTitle = document.getElementById('lbTitle');
    const lbSeq = document.getElementById('lbSeq');
    const lbCaption = document.getElementById('lbCaption');
    const lbTime = document.getElementById('lbTime');
    const lbFolder = document.getElementById('lbFolder');
    const lbDownload = document.getElementById('lbDownload');
    const backToTop = document.getElementById('backToTop');

    // Initialize Level 1 Tabs
    function renderSubfolderTabs() {{
      subfolderTabs.innerHTML = '';
      subfolderKeys.forEach(sub => {{
        const meta = GALLERY_DATA[sub];
        const btn = document.createElement('button');
        btn.className = `tab-btn ${{sub === currentSubfolder ? 'active' : ''}}`;
        btn.innerHTML = `${{meta.info.icon}} ${{sub}} <span class="tab-badge">${{meta.count}}</span>`;
        btn.addEventListener('click', () => {{
          if (currentSubfolder !== sub) {{
            currentSubfolder = sub;
            currentActivity = 'ALL';
            searchQuery = '';
            searchInput.value = '';
            updateTabsActive();
            updateSubfolderInfo();
            renderActivityPills();
            renderPhotos();
          }}
        }});
        subfolderTabs.appendChild(btn);
      }});
    }}

    function updateTabsActive() {{
      const btns = subfolderTabs.querySelectorAll('.tab-btn');
      subfolderKeys.forEach((sub, i) => {{
        if (sub === currentSubfolder) {{
          btns[i].classList.add('active');
        }} else {{
          btns[i].classList.remove('active');
        }}
      }});
    }}

    function updateSubfolderInfo() {{
      const meta = GALLERY_DATA[currentSubfolder];
      infoIcon.textContent = meta.info.icon || '⛺';
      infoTitle.textContent = currentSubfolder;
      infoDesc.textContent = meta.info.desc || '';
      infoCount.textContent = meta.count;
      activeSubfolderLabel.textContent = `【${{currentSubfolder}}】`;
    }}

    // Initialize Level 2 Activity Pills
    function renderActivityPills() {{
      const meta = GALLERY_DATA[currentSubfolder];
      activityPills.innerHTML = '';

      // Count activities
      const actCounts = {{}};
      meta.items.forEach(item => {{
        actCounts[item.act] = (actCounts[item.act] || 0) + 1;
      }});

      // ALL Pill
      const allBtn = document.createElement('button');
      allBtn.className = `pill-btn ${{currentActivity === 'ALL' ? 'active' : ''}}`;
      allBtn.innerHTML = `全部 <span class="pill-count">${{meta.count}}</span>`;
      allBtn.addEventListener('click', () => {{
        currentActivity = 'ALL';
        updatePillsActive();
        renderPhotos();
      }});
      activityPills.appendChild(allBtn);

      // Other Activities
      meta.activities.forEach(act => {{
        const btn = document.createElement('button');
        btn.className = `pill-btn ${{currentActivity === act ? 'active' : ''}}`;
        btn.innerHTML = `${{act}} <span class="pill-count">${{actCounts[act] || 0}}</span>`;
        btn.addEventListener('click', () => {{
          currentActivity = act;
          updatePillsActive();
          renderPhotos();
        }});
        activityPills.appendChild(btn);
      }});
    }}

    function updatePillsActive() {{
      const pills = activityPills.querySelectorAll('.pill-btn');
      pills.forEach((p, idx) => {{
        if (idx === 0) {{
          if (currentActivity === 'ALL') p.classList.add('active');
          else p.classList.remove('active');
        }} else {{
          const meta = GALLERY_DATA[currentSubfolder];
          const act = meta.activities[idx - 1];
          if (currentActivity === act) p.classList.add('active');
          else p.classList.remove('active');
        }}
      }});
      currentFilterLabel.textContent = currentActivity === 'ALL' ? '全部活動' : currentActivity;
    }}

    // Render Photo Cards
    function renderPhotos() {{
      const meta = GALLERY_DATA[currentSubfolder];
      let items = meta.items;

      // Filter by Activity
      if (currentActivity !== 'ALL') {{
        items = items.filter(it => it.act === currentActivity);
      }}

      // Filter by Search Query
      if (searchQuery.trim() !== '') {{
        const q = searchQuery.toLowerCase().trim();
        items = items.filter(it => 
          it.filename.toLowerCase().includes(q) ||
          it.act.toLowerCase().includes(q) ||
          it.caption.toLowerCase().includes(q) ||
          it.disp_time.toLowerCase().includes(q)
        );
      }}

      currentFilteredList = items;
      visibleCount.textContent = items.length;

      if (items.length === 0) {{
        photoGrid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
      }}

      photoGrid.style.display = 'grid';
      emptyState.style.display = 'none';
      photoGrid.innerHTML = '';

      items.forEach((item, index) => {{
        const card = document.createElement('div');
        card.className = 'photo-card';

        // Media Thumbnail
        let thumbHtml = '';
        if (item.is_video) {{
          thumbHtml = `
            <div class="media-thumb-box" onclick="openLightbox(${{index}})">
              <div class="video-badge">▶ 影片</div>
              <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#1e1b4b;">
                <span style="font-size:3.5rem;">🎬</span>
              </div>
              <div class="zoom-overlay"><div class="zoom-btn-icon">▶</div></div>
            </div>`;
        }} else {{
          thumbHtml = `
            <div class="media-thumb-box" onclick="openLightbox(${{index}})">
              <img class="media-thumb" src="${{encodeURI(item.rel_path)}}" alt="${{item.caption}}" loading="lazy">
              <div class="zoom-overlay"><div class="zoom-btn-icon">🔍</div></div>
            </div>`;
        }}

        card.innerHTML = `
          ${{thumbHtml}}
          <div class="card-body">
            <div class="card-meta">
              <span class="tag-act">${{item.act}}</span>
              <span class="tag-time">🕒 ${{item.disp_time}}</span>
              <span class="tag-seq">${{item.seq}}</span>
            </div>
            <p class="card-caption">${{item.caption}}</p>
            <div class="card-footer">
              <span class="file-tag" title="${{item.filename}}">${{item.filename}}</span>
              <a class="btn-download" href="${{encodeURI(item.rel_path)}}" download="${{item.filename}}" title="下載檔案">下載 ⬇</a>
            </div>
          </div>
        `;
        photoGrid.appendChild(card);
      }});
    }}

    // Search Input Listener
    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      renderPhotos();
    }});

    // Lightbox Functions
    window.openLightbox = function(index) {{
      currentLightboxIndex = index;
      updateLightbox();
      lightboxModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }};

    function closeLightbox() {{
      lightboxModal.classList.remove('active');
      document.body.style.overflow = 'auto';
      if (lbVideo) {{
        lbVideo.pause();
        lbVideo.src = '';
      }}
    }}

    function updateLightbox() {{
      const item = currentFilteredList[currentLightboxIndex];
      if (!item) return;

      lbBadge.textContent = item.act;
      lbTitle.textContent = item.filename;
      lbSeq.textContent = item.seq;
      lbCaption.textContent = item.caption;
      lbTime.textContent = item.disp_time;
      lbFolder.textContent = currentSubfolder;
      lbDownload.href = encodeURI(item.rel_path);
      lbDownload.download = item.filename;

      if (item.is_video) {{
        lbImg.style.display = 'none';
        lbVideo.style.display = 'block';
        lbVideo.src = encodeURI(item.rel_path);
        lbVideo.play().catch(() => {{}});
      }} else {{
        if (lbVideo) {{
          lbVideo.pause();
          lbVideo.src = '';
        }}
        lbVideo.style.display = 'none';
        lbImg.style.display = 'block';
        lbImg.src = encodeURI(item.rel_path);
      }}

      // Nav buttons visibility
      lbPrev.style.display = currentLightboxIndex > 0 ? 'flex' : 'none';
      lbNext.style.display = currentLightboxIndex < currentFilteredList.length - 1 ? 'flex' : 'none';
    }}

    lbClose.addEventListener('click', closeLightbox);
    lightboxModal.addEventListener('click', (e) => {{
      if (e.target === lightboxModal) closeLightbox();
    }});

    lbPrev.addEventListener('click', (e) => {{
      e.stopPropagation();
      if (currentLightboxIndex > 0) {{
        currentLightboxIndex--;
        updateLightbox();
      }}
    }});

    lbNext.addEventListener('click', (e) => {{
      e.stopPropagation();
      if (currentLightboxIndex < currentFilteredList.length - 1) {{
        currentLightboxIndex++;
        updateLightbox();
      }}
    }});

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {{
      if (!lightboxModal.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      else if (e.key === 'ArrowLeft' && currentLightboxIndex > 0) {{
        currentLightboxIndex--;
        updateLightbox();
      }} else if (e.key === 'ArrowRight' && currentLightboxIndex < currentFilteredList.length - 1) {{
        currentLightboxIndex++;
        updateLightbox();
      }}
    }});

    // Back to top
    window.addEventListener('scroll', () => {{
      if (window.scrollY > 300) {{
        backToTop.classList.add('visible');
      }} else {{
        backToTop.classList.remove('visible');
      }}
    }});

    backToTop.addEventListener('click', () => {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }});

    // Initial setup
    renderSubfolderTabs();
    updateSubfolderInfo();
    renderActivityPills();
    renderPhotos();
  </script>
</body>
</html>
'''

index_html_path = os.path.join(target_dir, 'index.html')
with open(index_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated {index_html_path}")
print(f"File size: {os.path.getsize(index_html_path) / 1024:.2f} KB")
