import os
import sys
import json
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r'C:\antigravity\115-10-27-28back'
subdirs = ['201 三元', '202小郭', '203 阿犬', '204木木', '205+206+207 哈任', '207 五千', '獨木橋', '繩結 盲蛇取物', '跳繩+水彈']

# Subfolder metadata (counselor / activity intro)
subfolder_meta = {
    '201 三元': {'desc': '201 班與隊輔三元哥哥的精彩生活日誌', 'icon': '⛺', 'type': 'class'},
    '202小郭': {'desc': '202 班與隊輔小郭哥哥的熱血挑戰全紀錄', 'icon': '🔥', 'type': 'class'},
    '203 阿犬': {'desc': '203 班與隊輔阿犬哥哥的默契成長足跡', 'icon': '🌟', 'type': 'class'},
    '204木木': {'desc': '204 班與隊輔木木姐姐的歡樂野營日常', 'icon': '🌲', 'type': 'class'},
    '205+206+207 哈任': {'desc': '205+206+207 聯隊與隊輔哈任的精彩合影', 'icon': '🎉', 'type': 'class'},
    '207 五千': {'desc': '207 班與隊輔五千姐姐的青春探索之旅', 'icon': '✨', 'type': 'class'},
    '獨木橋': {'desc': '極限山訓探索——勇氣與平衡感大考驗', 'icon': '🧗', 'type': 'station'},
    '繩結 盲蛇取物': {'desc': '童軍核心技能與信任探索——八大繩結與盲蛇尋寶', 'icon': '🪢', 'type': 'station'},
    '跳繩+水彈': {'desc': '山訓探索專區——生存遊戲水彈射擊與團隊大跳繩默契', 'icon': '🎯', 'type': 'station'}
}

# Rich contextual caption generator
def generate_caption(sub, act, time_str, seq, filename):
    is_video = filename.lower().endswith(('.mov', '.mp4'))
    if is_video:
        if '營火' in act:
            return f"【現場實況錄影】{sub} 於營火晚會舞台前熱力四射勁歌熱舞，全場歡聲雷動！"
        elif '山訓' in act or '繩結' in sub or '盲蛇' in sub:
            return f"【闖關實況錄影】{sub} 山訓分站闖關精準捕捉隊員默契配合與熱血突破時刻！"
        return f"【活動影音紀錄】{sub} {act} 精彩動態紀錄短片。"

    if act == '快樂啟程':
        captions = [
            f"{sub} 同學們精神抖擻搭上專車啟程，隨車隊輔熱情破冰帶動，開啟期待已久的露營旅程！",
            f"專車行駛國道南下，同學們興奮佩戴安全帶並開心向鏡頭比耶，留下青春出發的燦爛合影。",
            f"隊輔進行行車安全與逃生避難宣導，同學們彼此互動寒暄，車廂內充滿歡笑與出發期待。",
            f"啟程南下途中大家活力充沛，滿心期待即將抵達的台南尖山埤營地！"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '環境認識安全檢查':
        captions = [
            f"抵達尖山埤露營區！{sub} 同學們迅速整隊集合，隊輔進行生活常規宣導與個人隨身安檢。",
            f"各小隊整齊列隊聆聽營地公約，熟悉營本部、緊急救護站與洗滌衛浴動線，落實團隊紀律。",
            f"隨隊導師與隊輔仔細檢查各項器材，同學們展現高度自律，為兩天一夜活動打下安全基石。"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '開訓始業式':
        captions = [
            f"開訓始業式隆重展開！校長與師長致詞勉勵同學團結合作，隨隊隊輔群登台熱情熱舞亮相！",
            f"值星官正式接掌值星營旗並宣誓開訓，{sub} 全體成員齊聲呼號宣告露營挑戰正式啟動！",
            f"師長與全體師生齊聚大集會場，宣誓遵守童軍守則，展現朝氣蓬勃的南投國中團隊精神！"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '午餐饗宴':
        return f"{sub} 於開訓後領取中式美味便當，大夥圍坐稍作歇息，互相分享水分與補充體力。"

    elif act == '帳棚搭設示範':
        captions = [
            f"童軍野營核心技能！教官親自解析屋式帳結構與搭帳五步驟，解說 45 度倒勾營釘入土力學。",
            f"{sub} 小隊夥伴合力拉平地布、穿入鋁合金支架，同心協力頂起主桿撐開帳篷大骨架！",
            f"組員分工拉緊四角防風營繩並牢固敲入營釘，確保帳篷平整穩固、防風避雨。",
            f"鋪設外帳並固定防雨遮陽篷，小隊分工合作井然有序，親手打造今晚甜蜜溫馨的野營小窩！",
            f"帳篷搭建圓滿完工！{sub} 同學們在親手完成的整齊營帳前驕傲比讚合影，展現滿滿成就感！"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '童軍核心技能':
        captions = [
            f"童軍核心技能闖關！{sub} 同學專心聆聽教官解說，學習炭火引燃技巧與戶外野外炊具運用。",
            f"夥伴們親手練習生活實用八大繩結操作（平結、接繩結、稱人結等），手眼協調迅速上手！",
            f"實務演練戶外急救防護、台灣六大毒蛇辨識與五要五不常識，建立紮實戶外自保能力。",
            f"{sub} 同學們在草地上練習營火晚會動感律動舞步，歡笑聲不斷，兼具知識性與趣味性！"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '野炊廚藝競賽':
        captions = [
            f"野炊廚藝大比拚登場！{sub} 各組分工生火起灶、洗菜切肉，炊事專區炊煙裊裊熱鬧非凡！",
            f"小小大廚親自掌勺翻炒，大火快炒時蔬與肉片，火候拿捏精準，陣陣菜香撲鼻而來！",
            f"組員們各司其職默契十足，添柴掌控火勢、調配醬料擺盤，同心合力爭取班級炊事總錦標！",
            f"熱騰騰的現炒佳餚美味出鍋，金黃煎蛋與香炒時蔬盛盤上桌，等待評審老師的嚴謹評分！",
            f"全組同學圍坐大快朵頤，品嚐親手用柴火烹煮的豐盛晚餐，每一口都凝聚著深厚的團隊合作滋味！"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '營火晚會':
        captions = [
            f"營火晚會高潮引爆！熊熊烈焰點亮尖山埤夜空，全場師生高舉螢光棒齊聲吶喊歡呼！",
            f"{sub} 登台帶來熱力四射的才藝動感舞蹈，節奏明快動作整齊，瞬間點燃全場狂熱氣氛！",
            f"隨隊隊輔帶領全體學生熱情飆舞、齊聲合唱，全場圍繞營火盡情跳躍，釋放青春熱血！",
            f"晚會尾聲溫馨柔美的燭光夜語時刻，微光搖曳中師生圍圈真情對話，薪火相傳真情流露。",
            f"在柔和燭光與溫馨音樂圍繞下，師長給予深情叮嚀，全體師生相擁合影，留下難以忘懷的感動回憶。"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '早餐合菜':
        captions = [
            f"第二天晨光初現！{sub} 同學們早起整隊入座，在清晨微風中享用熱騰騰的營養中式早餐。",
            f"大鍋熱白粥搭配香酥肉鬆、水煮蛋、豆腐乳與鮮脆時蔬，同桌互盛熱粥，補充整日體能！",
            f"吃得津津有味、元氣滿分！同學們臉上洋溢著精神奕奕的笑容，儲備好上午山訓極限挑戰的能量。"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '山訓與探索教育':
        if '跳繩' in sub or '水彈' in sub:
            captions = [
                f"【生存遊戲水彈射擊】隊員全副武裝佩戴護目鏡，手持水彈槍於掩體間穿梭索敵、精準射擊！",
                f"【水彈對戰戰術掩護】小隊成員分工警戒、前後掩護壓制，在緊張刺激的對抗賽中培養高度信任！",
                f"【團隊解手結挑戰】全組雙手交錯互牽，透過冷靜觀察與默契走位解開繁複手結，展現解難智慧！",
                f"【小隊團體大跳繩】長繩規律甩動，全隊同學伴隨口號步伐一致騰空躍起，挑戰團隊最高默契！"
            ]
            return captions[(seq - 1) % len(captions)]
        elif '獨木橋' in sub:
            captions = [
                f"【極限獨木橋考驗】同學深呼吸踏上高空獨木橋，張開雙手維持平衡，勇敢邁出自我突破第一步！",
                f"【專注無懼邁向終點】面對懸空晃動的橋身，夥伴目光堅定、步伐沉穩，下方全體同學熱烈歡呼加油！",
                f"【克服恐懼超越自我】順利跨越獨木橋抵達對岸！隊員展現無比勇氣與自信微笑，收穫全場掌聲！"
            ]
            return captions[(seq - 1) % len(captions)]
        elif '繩結' in sub or '盲蛇' in sub:
            captions = [
                f"【童軍生活繩結實作】教官細部指導繩結打法，同學專注穿引繩索，掌握牢固耐用的打結技巧。",
                f"【盲蛇取物信任考驗】矇上雙眼的同學全心信賴身後隊友的口令指引，步步為營避開障礙尋獲寶物！",
                f"【考驗團隊默契與聆聽】場邊隊友精準給出方位指示，矇眼探員沉著執行，展現無可取代的隊友情誼。"
            ]
            return captions[(seq - 1) % len(captions)]
        else:
            captions = [
                f"山訓與探索教育極限闖關！{sub} 同學勇於跨越舒適圈，在垂降、攀岩與平衡關卡中大顯身手！",
                f"小隊夥伴彼此打氣加油，攜手完成高難度探索挑戰，在汗水與笑聲中建立堅不可摧的互信情誼！",
                f"面對極限關卡無所畏懼，{sub} 同學們展現團結互助與堅韌毅力，成功拿下探索教育榮譽積分！"
            ]
            return captions[(seq - 1) % len(captions)]

    elif act == 'BBQ烤肉饗宴':
        captions = [
            f"充實山訓後迎接歡樂炭火 BBQ 烤肉饗宴！{sub} 各組點燃炭火，肉片、香腸在鐵網上滋滋作響！",
            f"刷上香濃特調烤肉醬，肉汁四溢香氣誘人，同學們興高采烈夾起現烤肉片夾入吐司享用！",
            f"同桌夥伴互相盛裝烤肉、遞水夾菜，共享豐盛BBQ美食，洋溢著溫馨無比的同儕深厚情誼！"
        ]
        return captions[(seq - 1) % len(captions)]

    elif act == '結訓典禮':
        captions = [
            f"榮耀時刻！結訓典禮隆重登場，校長與師長頒發炊事錦標、晚會優勝與全校精神總錦標錦旗！",
            f"{sub} 優秀代表自信上台領取榮譽錦旗，全班同學振臂歡呼熱烈喝采，共享最高團隊榮耀！",
            f"校長發表深情結訓勉勵，期許同學們將這兩天學到的獨立自律與團結互助精神延續到未來日常！",
            f"全體師生高唱營火回憶之歌，在感恩與惜別聲中圓滿劃下兩天一夜隔宿露營的完美句點。"
        ]
        return captions[(seq - 1) % len(captions)]

    return f"{sub} 同學於尖山埤露營區參與 {act} 精彩紀實。"

# Collect all data
gallery_data = {}
all_activities_global = set()
total_images_count = 0

for sub in subdirs:
    subpath = os.path.join(target_dir, sub)
    # Ignore .HEIC for web display (use .jpg instead)
    files = sorted([f for f in os.listdir(subpath) if not f.lower().endswith('.heic')])
    
    sub_items = []
    sub_acts = set()
    
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        is_video = ext in ['.mov', '.mp4']
        
        # parse filename: 115-10-27-0812_201 三元_01-快樂啟程.JPG
        m = re.match(r'^(\d{3}-\d{2}-\d{2}-\d{4})_(.+?)_(\d+)-(.*?)\.(.+)$', f)
        if m:
            time_raw = m.group(1) # 115-10-27-0812
            seq = int(m.group(3))
            act = m.group(4)
        else:
            time_raw = '115-10-27-0800'
            seq = 1
            act = f.split('-')[-1].split('.')[0] if '-' in f else '活動紀錄'

        sub_acts.add(act)
        all_activities_global.add(act)
        
        # Format display time: e.g. 10/27 08:12
        parts = time_raw.split('-')
        if len(parts) == 4:
            disp_time = f"{parts[1]}/{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
        else:
            disp_time = time_raw

        caption = generate_caption(sub, act, disp_time, seq, f)
        
        # Relative URL for web
        rel_path = f"{sub}/{f}"

        sub_items.append({
            'filename': f,
            'rel_path': rel_path,
            'time_raw': time_raw,
            'disp_time': disp_time,
            'seq': f"#{seq:02d}",
            'act': act,
            'caption': caption,
            'is_video': is_video
        })
        total_images_count += 1

    gallery_data[sub] = {
        'info': subfolder_meta.get(sub, {'desc': f'{sub} 隔宿露營精彩回顧', 'icon': '📷', 'type': 'class'}),
        'count': len(sub_items),
        'activities': sorted(list(sub_acts)),
        'items': sub_items
    }

print(f"Total classified items for web: {total_images_count}")
print(f"9 Subfolders processed.")

# Save gallery_data to a json file
json_path = os.path.join(target_dir, 'gallery_data.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(gallery_data, f, ensure_ascii=False, indent=2)

print(f"Saved {json_path}")
