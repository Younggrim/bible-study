#!/usr/bin/env python3
"""Interface wording (buttons and labels) in the languages of the other-language
Bibles, written to docs/site/i18n/<lang>.json, which docs/site/i18n.js loads
when a reader picks one of those Bibles.

    python3 i18n_strings.py          # write docs/site/i18n/*.json

Only buttons and labels are translated. Study notes, commentary and the other
tab contents stay in English (deliberately: see WORKFLOW.md).

These were written by Claude, not by native speakers. The major languages are
reliable; the ones marked REVIEW in LANGS below most deserve a check by a
fluent reader, and a correction is a one-line change here plus a re-run.
{n} and {book} are placeholders and must stay as they are.
"""
import json
import os

KEYS = [
    "tab.summary", "tab.authorship", "tab.mapgeo", "tab.commentary", "tab.videos", "tab.articles", "tab.reflection",
    "nav.go", "nav.ch", "nav.chapter", "home.choose", "home.goto",
    "bn.bible", "bn.topical", "bn.life", "bn.devotional", "bn.memory", "bn.notes",
    "sheet.bookmark", "sheet.bookmarked", "sheet.note", "sheet.clear",
    "home.resume", "home.continue", "home.lastread", "home.bookmarks", "home.highlights",
    "acct.signin", "acct.signout", "acct.signinbtn", "acct.mynotes", "acct.privacy", "acct.delete",
    "studied.mark", "studied.done", "streak.n", "home.daystreak", "home.chstudied",
    "notes.add", "notes.title", "notes.new", "notes.search", "notes.bullet", "notes.numbered", "notes.delete",
    "notes.all", "notes.titleph", "notes.bodyph", "notes.refph", "streak.risk", "notes.count",
]

EN = ["Summary", "Authorship & Background", "Map & Geography", "Commentary", "Videos", "Articles", "Reflection",
      "Go", "Ch {n}", "{book} — Chapter {n}", "Choose a Passage", "Go to Chapter",
      "Bible", "Topical", "Life", "Devotional", "Memory", "Notes",
      "Bookmark", "Bookmarked", "Note", "Clear",
      "Pick up where you left off", "Continue", "Last read", "Bookmarks", "Highlights",
      "Sign in", "Sign out", "Sign in to save your study", "My notes", "Privacy", "Delete my account",
      "Mark chapter studied", "Studied", "{n}-day streak", "day streak", "chapters studied",
      "Add a note", "My Notes", "New note", "Search notes", "Bullet point", "Numbered", "Delete note",
      "All notes", "Title", "Start writing…", "Passage, e.g. John 3:16",
      "Your {n}-day streak ends tonight. Study a chapter today to keep it going.", "Notes ({n})"]

T = {}

T["es"] = ["Resumen", "Autoría y contexto", "Mapa y geografía", "Comentario", "Videos", "Artículos", "Reflexión",
    "Ir", "Cap. {n}", "{book} — Capítulo {n}", "Elige un pasaje", "Ir al capítulo",
    "Biblia", "Temas", "Vida", "Devocional", "Memoria", "Notas",
    "Marcar", "Marcado", "Nota", "Borrar",
    "Continúa donde lo dejaste", "Continuar", "Última lectura", "Marcadores", "Resaltados",
    "Iniciar sesión", "Cerrar sesión", "Inicia sesión para guardar tu estudio", "Mis notas", "Privacidad", "Eliminar mi cuenta",
    "Marcar capítulo como estudiado", "Estudiado", "Racha de {n} días", "días de racha", "capítulos estudiados",
    "Añadir una nota", "Mis notas", "Nueva nota", "Buscar notas", "Viñeta", "Numerada", "Eliminar nota",
    "Todas las notas", "Título", "Empieza a escribir…", "Pasaje, p. ej. Juan 3:16",
    "Tu racha de {n} días termina esta noche. Estudia un capítulo hoy para mantenerla.", "Notas ({n})"]

T["fr"] = ["Résumé", "Auteur et contexte", "Carte et géographie", "Commentaire", "Vidéos", "Articles", "Réflexion",
    "Aller", "Ch. {n}", "{book} — Chapitre {n}", "Choisir un passage", "Aller au chapitre",
    "Bible", "Thèmes", "Vie", "Méditation", "Mémoire", "Notes",
    "Signet", "Signet ajouté", "Note", "Effacer",
    "Reprendre là où vous en étiez", "Continuer", "Dernière lecture", "Signets", "Surlignages",
    "Se connecter", "Se déconnecter", "Connectez-vous pour enregistrer votre étude", "Mes notes", "Confidentialité", "Supprimer mon compte",
    "Marquer le chapitre comme étudié", "Étudié", "{n} jours d’affilée", "jours d’affilée", "chapitres étudiés",
    "Ajouter une note", "Mes notes", "Nouvelle note", "Rechercher dans les notes", "Puce", "Numérotée", "Supprimer la note",
    "Toutes les notes", "Titre", "Commencez à écrire…", "Passage, ex. Jean 3:16",
    "Votre série de {n} jours se termine ce soir. Étudiez un chapitre aujourd’hui pour la poursuivre.", "Notes ({n})"]

T["pt"] = ["Resumo", "Autoria e contexto", "Mapa e geografia", "Comentário", "Vídeos", "Artigos", "Reflexão",
    "Ir", "Cap. {n}", "{book} — Capítulo {n}", "Escolha uma passagem", "Ir para o capítulo",
    "Bíblia", "Temas", "Vida", "Devocional", "Memória", "Notas",
    "Marcar", "Marcado", "Nota", "Limpar",
    "Continue de onde parou", "Continuar", "Última leitura", "Marcadores", "Destaques",
    "Entrar", "Sair", "Entre para salvar seu estudo", "Minhas notas", "Privacidade", "Excluir minha conta",
    "Marcar capítulo como estudado", "Estudado", "{n} dias seguidos", "dias seguidos", "capítulos estudados",
    "Adicionar uma nota", "Minhas notas", "Nova nota", "Buscar notas", "Marcador", "Numerada", "Excluir nota",
    "Todas as notas", "Título", "Comece a escrever…", "Passagem, ex.: João 3:16",
    "Sua sequência de {n} dias termina hoje à noite. Estude um capítulo hoje para mantê-la.", "Notas ({n})"]

T["ar"] = ["الملخص", "الكاتب والخلفية", "الخريطة والجغرافيا", "التفسير", "فيديوهات", "مقالات", "تأمل",
    "اذهب", "أصحاح {n}", "{book} — الأصحاح {n}", "اختر مقطعًا", "اذهب إلى الأصحاح",
    "الكتاب المقدس", "مواضيع", "الحياة", "التأمل اليومي", "الحفظ", "ملاحظات",
    "إشارة مرجعية", "تمت الإشارة", "ملاحظة", "مسح",
    "تابع من حيث توقفت", "متابعة", "آخر قراءة", "الإشارات المرجعية", "التظليلات",
    "تسجيل الدخول", "تسجيل الخروج", "سجّل الدخول لحفظ دراستك", "ملاحظاتي", "الخصوصية", "حذف حسابي",
    "تحديد الأصحاح كمدروس", "تمت الدراسة", "{n} أيام متتالية", "أيام متتالية", "أصحاحات مدروسة",
    "أضف ملاحظة", "ملاحظاتي", "ملاحظة جديدة", "ابحث في الملاحظات", "نقاط", "ترقيم", "حذف الملاحظة",
    "كل الملاحظات", "العنوان", "ابدأ الكتابة…", "المقطع، مثلاً يوحنا 3:16",
    "ستنتهي أيامك المتتالية ({n}) الليلة. ادرس أصحاحًا اليوم لتستمر.", "ملاحظات ({n})"]

T["fa"] = ["خلاصه", "نویسنده و زمینه", "نقشه و جغرافیا", "تفسیر", "ویدیوها", "مقالات", "تأمل",
    "برو", "باب {n}", "{book} — باب {n}", "یک بخش را انتخاب کنید", "رفتن به باب",
    "کتاب مقدس", "موضوعات", "زندگی", "تأمل روزانه", "حفظ آیات", "یادداشت‌ها",
    "نشانک", "نشانک‌گذاری شد", "یادداشت", "پاک کردن",
    "از جایی که ماندید ادامه دهید", "ادامه", "آخرین مطالعه", "نشانک‌ها", "برجسته‌ها",
    "ورود", "خروج", "برای ذخیرهٔ مطالعه‌تان وارد شوید", "یادداشت‌های من", "حریم خصوصی", "حذف حساب من",
    "علامت‌گذاری باب به‌عنوان مطالعه‌شده", "مطالعه شد", "{n} روز پیاپی", "روز پیاپی", "باب مطالعه‌شده",
    "افزودن یادداشت", "یادداشت‌های من", "یادداشت جدید", "جستجوی یادداشت‌ها", "نقطه‌دار", "شماره‌دار", "حذف یادداشت",
    "همهٔ یادداشت‌ها", "عنوان", "شروع به نوشتن کنید…", "بخش، مثلاً یوحنا ۳:۱۶",
    "رشتهٔ {n} روزهٔ شما امشب تمام می‌شود. امروز یک باب مطالعه کنید تا ادامه یابد.", "یادداشت‌ها ({n})"]

T["zh-Hans"] = ["概要", "作者与背景", "地图与地理", "注释", "视频", "文章", "反思",
    "前往", "第{n}章", "{book} 第{n}章", "选择经文", "前往该章",
    "圣经", "主题", "生活", "灵修", "背经", "笔记",
    "书签", "已加书签", "笔记", "清除",
    "从上次停下的地方继续", "继续", "上次阅读", "书签", "标记",
    "登录", "退出登录", "登录以保存你的学习", "我的笔记", "隐私", "删除我的账户",
    "标记本章已学习", "已学习", "连续{n}天", "天连续", "章已学习",
    "添加笔记", "我的笔记", "新笔记", "搜索笔记", "项目符号", "编号", "删除笔记",
    "全部笔记", "标题", "开始书写…", "经文，例如 约翰福音 3:16",
    "你已连续学习{n}天，今晚将中断。今天学习一章即可保持。", "笔记（{n}）"]

T["zh-Hant"] = ["概要", "作者與背景", "地圖與地理", "註釋", "影片", "文章", "反思",
    "前往", "第{n}章", "{book} 第{n}章", "選擇經文", "前往該章",
    "聖經", "主題", "生活", "靈修", "背經", "筆記",
    "書籤", "已加書籤", "筆記", "清除",
    "從上次停下的地方繼續", "繼續", "上次閱讀", "書籤", "標記",
    "登入", "登出", "登入以儲存你的學習", "我的筆記", "隱私", "刪除我的帳戶",
    "標記本章已學習", "已學習", "連續{n}天", "天連續", "章已學習",
    "新增筆記", "我的筆記", "新筆記", "搜尋筆記", "項目符號", "編號", "刪除筆記",
    "全部筆記", "標題", "開始書寫…", "經文，例如 約翰福音 3:16",
    "你已連續學習{n}天，今晚將中斷。今天學習一章即可保持。", "筆記（{n}）"]

T["vi"] = ["Tóm tắt", "Tác giả và bối cảnh", "Bản đồ và địa lý", "Chú giải", "Video", "Bài viết", "Suy ngẫm",
    "Đi", "Ch. {n}", "{book} — Chương {n}", "Chọn một phân đoạn", "Đến chương",
    "Kinh Thánh", "Chủ đề", "Đời sống", "Tĩnh nguyện", "Ghi nhớ", "Ghi chú",
    "Đánh dấu", "Đã đánh dấu", "Ghi chú", "Xóa",
    "Tiếp tục từ chỗ bạn đã dừng", "Tiếp tục", "Đọc lần cuối", "Dấu trang", "Tô sáng",
    "Đăng nhập", "Đăng xuất", "Đăng nhập để lưu việc học của bạn", "Ghi chú của tôi", "Quyền riêng tư", "Xóa tài khoản của tôi",
    "Đánh dấu đã học chương này", "Đã học", "Chuỗi {n} ngày", "ngày liên tiếp", "chương đã học",
    "Thêm ghi chú", "Ghi chú của tôi", "Ghi chú mới", "Tìm ghi chú", "Gạch đầu dòng", "Đánh số", "Xóa ghi chú",
    "Tất cả ghi chú", "Tiêu đề", "Bắt đầu viết…", "Phân đoạn, vd. Giăng 3:16",
    "Chuỗi {n} ngày của bạn sẽ kết thúc tối nay. Hãy học một chương hôm nay để giữ chuỗi.", "Ghi chú ({n})"]

T["tl"] = ["Buod", "May-akda at Konteksto", "Mapa at Heograpiya", "Komentaryo", "Mga Video", "Mga Artikulo", "Pagninilay",
    "Pumunta", "Kab. {n}", "{book} — Kabanata {n}", "Pumili ng Talata", "Pumunta sa Kabanata",
    "Bibliya", "Paksa", "Buhay", "Debosyonal", "Pagsasaulo", "Mga Tala",
    "I-bookmark", "Naka-bookmark", "Tala", "Burahin",
    "Ituloy kung saan ka huminto", "Ituloy", "Huling nabasa", "Mga bookmark", "Mga highlight",
    "Mag-sign in", "Mag-sign out", "Mag-sign in para i-save ang iyong pag-aaral", "Aking mga tala", "Privacy", "Burahin ang aking account",
    "Markahang napag-aralan ang kabanata", "Napag-aralan", "{n} sunod-sunod na araw", "sunod-sunod na araw", "kabanatang napag-aralan",
    "Magdagdag ng tala", "Aking mga Tala", "Bagong tala", "Maghanap sa mga tala", "Bullet", "May numero", "Burahin ang tala",
    "Lahat ng tala", "Pamagat", "Magsimulang magsulat…", "Talata, hal. Juan 3:16",
    "Matatapos ngayong gabi ang iyong {n} sunod-sunod na araw. Mag-aral ng isang kabanata ngayon para magpatuloy.", "Mga tala ({n})"]

T["ht"] = ["Rezime", "Otè ak kontèks", "Kat ak jewografi", "Kòmantè", "Videyo", "Atik", "Refleksyon",
    "Ale", "Chap. {n}", "{book} — Chapit {n}", "Chwazi yon pasaj", "Ale nan chapit la",
    "Bib", "Sijè", "Lavi", "Devosyon", "Memwa", "Nòt",
    "Make", "Make deja", "Nòt", "Efase",
    "Kontinye kote ou te rete a", "Kontinye", "Dènye lekti", "Mak", "Souliyaj",
    "Konekte", "Dekonekte", "Konekte pou anrejistre etid ou", "Nòt mwen yo", "Vi prive", "Efase kont mwen",
    "Make chapit la kòm etidye", "Etidye", "{n} jou youn apre lòt", "jou youn apre lòt", "chapit etidye",
    "Ajoute yon nòt", "Nòt mwen yo", "Nouvo nòt", "Chèche nan nòt yo", "Pwen", "Nimewote", "Efase nòt la",
    "Tout nòt yo", "Tit", "Kòmanse ekri…", "Pasaj, pa egzanp Jan 3:16",
    "Seri {n} jou ou a ap fini aswè a. Etidye yon chapit jodi a pou kontinye.", "Nòt ({n})"]

T["ha"] = ["Taƙaitawa", "Marubuci da Tarihi", "Taswira da Ƙasa", "Sharhi", "Bidiyo", "Labarai", "Tunani",
    "Je", "Babi {n}", "{book} — Babi {n}", "Zaɓi Nassi", "Je zuwa Babi",
    "Littafi Mai Tsarki", "Jigogi", "Rayuwa", "Ibada", "Haddace", "Bayanai",
    "Alama", "An yi alama", "Bayani", "Share",
    "Ci gaba daga inda ka tsaya", "Ci gaba", "Karatu na ƙarshe", "Alamomi", "Haskakawa",
    "Shiga", "Fita", "Shiga don adana karatunka", "Bayanaina", "Sirri", "Share asusuna",
    "Sa alama an karanta babin", "An karanta", "Kwanaki {n} a jere", "kwanaki a jere", "babobin da aka karanta",
    "Ƙara bayani", "Bayanaina", "Sabon bayani", "Nemo bayanai", "Ɗigo", "Lambobi", "Share bayani",
    "Duk bayanai", "Take", "Fara rubutu…", "Nassi, misali Yohanna 3:16",
    "Kwanakinka {n} a jere za su ƙare yau da dare. Karanta babi ɗaya yau don ci gaba.", "Bayanai ({n})"]

T["yo"] = ["Àkópọ̀", "Òǹkọ̀wé àti Ìtàn", "Máàpù àti Ilẹ̀", "Àlàyé", "Fídíò", "Àwọn àpilẹ̀kọ", "Àṣàrò",
    "Lọ", "Orí {n}", "{book} — Orí {n}", "Yan Ẹsẹ Bíbélì", "Lọ sí Orí",
    "Bíbélì", "Àwọn Kókó", "Ìgbésí ayé", "Ìfọkànsìn", "Àkọ́sórí", "Àkọsílẹ̀",
    "Sàmì sí", "A ti sàmì sí", "Àkọsílẹ̀", "Pa rẹ́",
    "Tẹ̀síwájú láti ibi tí o dúró", "Tẹ̀síwájú", "Kíkà tó kẹ́yìn", "Àwọn àmì", "Àwọn ìtànmọ́lẹ̀",
    "Wọlé", "Jáde", "Wọlé láti tọ́jú ẹ̀kọ́ rẹ", "Àwọn àkọsílẹ̀ mi", "Àṣírí", "Pa àkọọ́lẹ̀ mi rẹ́",
    "Sàmì pé o ti kọ́ orí yìí", "Ti kọ́", "Ọjọ́ {n} léraléra", "ọjọ́ léraléra", "orí tí o ti kọ́",
    "Fi àkọsílẹ̀ kún un", "Àwọn Àkọsílẹ̀ Mi", "Àkọsílẹ̀ tuntun", "Wá àkọsílẹ̀", "Àmì kékeré", "Nọ́ńbà", "Pa àkọsílẹ̀ rẹ́",
    "Gbogbo àkọsílẹ̀", "Àkọlé", "Bẹ̀rẹ̀ sí kọ…", "Ẹsẹ, fún àpẹẹrẹ Johanu 3:16",
    "Ọjọ́ {n} léraléra rẹ yóò parí lálẹ́ òní. Kọ́ orí kan lónìí láti máa bá a lọ.", "Àkọsílẹ̀ ({n})"]

T["ig"] = ["Nchịkọta", "Onye dere ya na Akụkọ ndabere", "Maapụ na Ọdịdị ala", "Nkọwa", "Vidiyo", "Edemede", "Ntụgharị uche",
    "Gaa", "Isi {n}", "{book} — Isi {n}", "Họrọ Akụkụ Akwụkwọ Nsọ", "Gaa n'Isi",
    "Baịbụl", "Isiokwu", "Ndụ", "Ofufe", "Iburu n'isi", "Ndetu",
    "Kaa akara", "Akaala akara", "Ndetu", "Hichapụ",
    "Gaa n'ihu ebe ị kwụsịrị", "Gaa n'ihu", "Ọgụgụ ikpeazụ", "Akara", "Ihe e mere ka o pụta ìhè",
    "Banye", "Pụọ", "Banye ka ịchekwaa ọmụmụ gị", "Ndetu m", "Nzuzo", "Hichapụ akaụntụ m",
    "Kaa isi a akara na amụchaala ya", "Amụchaala", "Ụbọchị {n} n'usoro", "ụbọchị n'usoro", "isi amụchaala",
    "Tinye ndetu", "Ndetu m", "Ndetu ọhụrụ", "Chọọ ndetu", "Ntụpọ", "Nọmba", "Hichapụ ndetu",
    "Ndetu niile", "Isiokwu", "Malite ide…", "Akụkụ, dịka Jọn 3:16",
    "Ụbọchị {n} gị n'usoro ga-akwụsị n'abalị a. Mụọ otu isi taa ka ọ gaa n'ihu.", "Ndetu ({n})"]

T["sw"] = ["Muhtasari", "Mwandishi na Mazingira", "Ramani na Jiografia", "Ufafanuzi", "Video", "Makala", "Tafakari",
    "Nenda", "Sura {n}", "{book} — Sura {n}", "Chagua Kifungu", "Nenda kwenye Sura",
    "Biblia", "Mada", "Maisha", "Ibada", "Kukariri", "Maandishi",
    "Alamisho", "Imewekwa alamisho", "Andiko", "Futa",
    "Endelea ulipoachia", "Endelea", "Ulisoma mwisho", "Alamisho", "Vionyeshi",
    "Ingia", "Toka", "Ingia ili kuhifadhi masomo yako", "Maandishi yangu", "Faragha", "Futa akaunti yangu",
    "Weka alama sura imesomwa", "Imesomwa", "Siku {n} mfululizo", "siku mfululizo", "sura zilizosomwa",
    "Ongeza andiko", "Maandishi Yangu", "Andiko jipya", "Tafuta maandishi", "Nukta", "Namba", "Futa andiko",
    "Maandishi yote", "Kichwa", "Anza kuandika…", "Kifungu, mf. Yohana 3:16",
    "Mfululizo wako wa siku {n} unaisha leo usiku. Soma sura moja leo ili kuuendeleza.", "Maandishi ({n})"]

T["tw"] = ["Nsɛm tiawa", "Ɔkyerɛwfo ne Abakɔsɛm", "Asase mfonini", "Nkyerɛkyerɛmu", "Video", "Nsɛm a wɔakyerɛw", "Adwendwene",
    "Kɔ", "Ti {n}", "{book} — Ti {n}", "Paw Kyerɛwsɛm", "Kɔ Ti no so",
    "Bible", "Asɛmti", "Asetena", "Anɔpa som", "Ti mu sua", "Nsɛm a wɔakyerɛw",
    "Hyɛ agyiraeɛ", "Wɔahyɛ agyiraeɛ", "Kyerɛw", "Pepa",
    "Toa so firi baabi a wogyae", "Toa so", "Nea wokenkanee akyire", "Agyiraeɛ", "Nea wɔahyɛn so",
    "Kɔ mu", "Fi mu", "Kɔ mu na kora wo adesua", "Me nsɛm a makyerɛw", "Kokoam", "Pepa me akontaabu",
    "Hyɛ agyiraeɛ sɛ masua ti yi", "Wɔasua", "Nnafua {n} toatoa so", "nnafua toatoa so", "ti a wɔasua",
    "Kyerɛw biribi", "Me Nsɛm", "Asɛm foforɔ", "Hwehwɛ nsɛm", "Nsensaneɛ", "Nɔma", "Pepa asɛm no",
    "Nsɛm nyinaa", "Asɛmti", "Fi ase kyerɛw…", "Kyerɛwsɛm, sɛ Yohane 3:16",
    "Wo nnafua {n} a atoatoa so no bɛba awieeɛ anadwo yi. Sua ti baako ɛnnɛ na ɛnkɔ so.", "Nsɛm ({n})"]

T["ur"] = ["خلاصہ", "مصنف اور پس منظر", "نقشہ اور جغرافیہ", "تفسیر", "ویڈیوز", "مضامین", "غور و فکر",
    "جائیں", "باب {n}", "{book} — باب {n}", "حوالہ منتخب کریں", "باب پر جائیں",
    "بائبل", "موضوعات", "زندگی", "روزانہ عبادت", "حفظ", "نوٹس",
    "بُک مارک", "بُک مارک ہو گیا", "نوٹ", "مٹائیں",
    "جہاں چھوڑا تھا وہیں سے جاری رکھیں", "جاری رکھیں", "آخری مطالعہ", "بُک مارکس", "نمایاں آیات",
    "سائن ان", "سائن آؤٹ", "اپنا مطالعہ محفوظ کرنے کے لیے سائن ان کریں", "میرے نوٹس", "رازداری", "میرا اکاؤنٹ حذف کریں",
    "باب کو پڑھا ہوا نشان زد کریں", "پڑھ لیا", "{n} دن مسلسل", "دن مسلسل", "پڑھے گئے ابواب",
    "نوٹ لکھیں", "میرے نوٹس", "نیا نوٹ", "نوٹس تلاش کریں", "نقطے", "نمبر", "نوٹ حذف کریں",
    "تمام نوٹس", "عنوان", "لکھنا شروع کریں…", "حوالہ، مثلاً یوحنا 3:16",
    "آپ کا {n} دن کا سلسلہ آج رات ختم ہو جائے گا۔ اسے جاری رکھنے کے لیے آج ایک باب پڑھیں۔", "نوٹس ({n})"]

T["hi"] = ["सारांश", "लेखक और पृष्ठभूमि", "मानचित्र और भूगोल", "टीका", "वीडियो", "लेख", "मनन",
    "जाएँ", "अध्याय {n}", "{book} — अध्याय {n}", "वचन चुनें", "अध्याय पर जाएँ",
    "बाइबल", "विषय", "जीवन", "भक्ति", "कंठस्थ", "नोट्स",
    "बुकमार्क", "बुकमार्क किया", "नोट", "हटाएँ",
    "जहाँ छोड़ा था वहीं से पढ़ें", "जारी रखें", "पिछली बार पढ़ा", "बुकमार्क", "हाइलाइट",
    "साइन इन", "साइन आउट", "अपना अध्ययन सहेजने के लिए साइन इन करें", "मेरे नोट्स", "गोपनीयता", "मेरा खाता हटाएँ",
    "अध्याय को पढ़ा हुआ चिह्नित करें", "पढ़ लिया", "लगातार {n} दिन", "दिन लगातार", "अध्याय पढ़े",
    "नोट जोड़ें", "मेरे नोट्स", "नया नोट", "नोट्स खोजें", "बुलेट", "क्रमांकित", "नोट हटाएँ",
    "सभी नोट्स", "शीर्षक", "लिखना शुरू करें…", "वचन, जैसे यूहन्ना 3:16",
    "आपका {n} दिन का सिलसिला आज रात खत्म हो जाएगा। इसे जारी रखने के लिए आज एक अध्याय पढ़ें।", "नोट्स ({n})"]

T["bn"] = ["সারসংক্ষেপ", "লেখক ও পটভূমি", "মানচিত্র ও ভূগোল", "ব্যাখ্যা", "ভিডিও", "প্রবন্ধ", "ধ্যান",
    "যান", "অধ্যায় {n}", "{book} — অধ্যায় {n}", "অংশ বেছে নিন", "অধ্যায়ে যান",
    "বাইবেল", "বিষয়", "জীবন", "ধ্যান-প্রার্থনা", "মুখস্থ", "নোট",
    "বুকমার্ক", "বুকমার্ক করা হয়েছে", "নোট", "মুছুন",
    "যেখানে থেমেছিলেন সেখান থেকে শুরু করুন", "চালিয়ে যান", "শেষবার পড়েছেন", "বুকমার্ক", "হাইলাইট",
    "সাইন ইন", "সাইন আউট", "আপনার অধ্যয়ন সংরক্ষণ করতে সাইন ইন করুন", "আমার নোট", "গোপনীয়তা", "আমার অ্যাকাউন্ট মুছুন",
    "অধ্যায়টি পড়া হয়েছে চিহ্নিত করুন", "পড়া হয়েছে", "টানা {n} দিন", "দিন টানা", "অধ্যায় পড়া হয়েছে",
    "নোট যোগ করুন", "আমার নোট", "নতুন নোট", "নোট খুঁজুন", "বুলেট", "নম্বরযুক্ত", "নোট মুছুন",
    "সব নোট", "শিরোনাম", "লিখতে শুরু করুন…", "অংশ, যেমন যোহন 3:16",
    "আপনার টানা {n} দিনের ধারা আজ রাতে শেষ হবে। ধরে রাখতে আজ একটি অধ্যায় পড়ুন।", "নোট ({n})"]

T["ta"] = ["சுருக்கம்", "ஆசிரியர் மற்றும் பின்னணி", "வரைபடம் மற்றும் புவியியல்", "விளக்கவுரை", "வீடியோக்கள்", "கட்டுரைகள்", "தியானம்",
    "செல்", "அதி. {n}", "{book} — அதிகாரம் {n}", "வேதப்பகுதியைத் தேர்ந்தெடுங்கள்", "அதிகாரத்திற்குச் செல்",
    "வேதாகமம்", "தலைப்புகள்", "வாழ்க்கை", "தியானம்", "மனப்பாடம்", "குறிப்புகள்",
    "புத்தகக்குறி", "குறிக்கப்பட்டது", "குறிப்பு", "அழி",
    "விட்ட இடத்திலிருந்து தொடருங்கள்", "தொடர்", "கடைசியாக வாசித்தது", "புத்தகக்குறிகள்", "சிறப்பித்தவை",
    "உள்நுழை", "வெளியேறு", "உங்கள் படிப்பைச் சேமிக்க உள்நுழையுங்கள்", "என் குறிப்புகள்", "தனியுரிமை", "என் கணக்கை நீக்கு",
    "அதிகாரத்தைப் படித்ததாகக் குறி", "படித்தது", "தொடர்ந்து {n} நாட்கள்", "நாட்கள் தொடர்ச்சி", "படித்த அதிகாரங்கள்",
    "குறிப்பு சேர்", "என் குறிப்புகள்", "புதிய குறிப்பு", "குறிப்புகளைத் தேடு", "புள்ளி", "எண்ணிட்டது", "குறிப்பை நீக்கு",
    "எல்லா குறிப்புகளும்", "தலைப்பு", "எழுதத் தொடங்குங்கள்…", "வேதப்பகுதி, எ.கா. யோவான் 3:16",
    "உங்கள் {n} நாள் தொடர்ச்சி இன்றிரவு முடிகிறது. தொடர இன்று ஒரு அதிகாரம் படியுங்கள்.", "குறிப்புகள் ({n})"]

T["te"] = ["సారాంశం", "రచయిత మరియు నేపథ్యం", "పటం మరియు భూగోళం", "వ్యాఖ్యానం", "వీడియోలు", "వ్యాసాలు", "ధ్యానం",
    "వెళ్ళు", "అధ్యా. {n}", "{book} — అధ్యాయం {n}", "వాక్యభాగాన్ని ఎంచుకోండి", "అధ్యాయానికి వెళ్ళండి",
    "బైబిల్", "అంశాలు", "జీవితం", "ధ్యానం", "కంఠస్థం", "నోట్స్",
    "బుక్‌మార్క్", "బుక్‌మార్క్ చేయబడింది", "నోట్", "తొలగించు",
    "ఆపిన చోటు నుండి కొనసాగించండి", "కొనసాగించు", "చివరిగా చదివింది", "బుక్‌మార్క్‌లు", "హైలైట్‌లు",
    "సైన్ ఇన్", "సైన్ అవుట్", "మీ అధ్యయనాన్ని సేవ్ చేయడానికి సైన్ ఇన్ చేయండి", "నా నోట్స్", "గోప్యత", "నా ఖాతాను తొలగించు",
    "అధ్యాయం చదివినట్లు గుర్తించు", "చదివాను", "వరుసగా {n} రోజులు", "రోజులు వరుసగా", "చదివిన అధ్యాయాలు",
    "నోట్ జోడించు", "నా నోట్స్", "కొత్త నోట్", "నోట్స్ వెతకండి", "బుల్లెట్", "సంఖ్యలు", "నోట్ తొలగించు",
    "అన్ని నోట్స్", "శీర్షిక", "రాయడం ప్రారంభించండి…", "వాక్యభాగం, ఉదా. యోహాను 3:16",
    "మీ {n} రోజుల వరుస ఈ రాత్రి ముగుస్తుంది. కొనసాగించడానికి ఈ రోజు ఒక అధ్యాయం చదవండి.", "నోట్స్ ({n})"]

T["ml"] = ["സംഗ്രഹം", "ഗ്രന്ഥകർത്താവും പശ്ചാത്തലവും", "ഭൂപടവും ഭൂമിശാസ്ത്രവും", "വ്യാഖ്യാനം", "വീഡിയോകൾ", "ലേഖനങ്ങൾ", "ധ്യാനം",
    "പോകുക", "അധ്യാ. {n}", "{book} — അധ്യായം {n}", "വേദഭാഗം തിരഞ്ഞെടുക്കുക", "അധ്യായത്തിലേക്ക് പോകുക",
    "ബൈബിൾ", "വിഷയങ്ങൾ", "ജീവിതം", "ധ്യാനം", "മനഃപാഠം", "കുറിപ്പുകൾ",
    "ബുക്ക്മാർക്ക്", "ബുക്ക്മാർക്ക് ചെയ്തു", "കുറിപ്പ്", "മായ്ക്കുക",
    "നിർത്തിയിടത്തുനിന്ന് തുടരുക", "തുടരുക", "അവസാനം വായിച്ചത്", "ബുക്ക്മാർക്കുകൾ", "ഹൈലൈറ്റുകൾ",
    "സൈൻ ഇൻ", "സൈൻ ഔട്ട്", "നിങ്ങളുടെ പഠനം സംരക്ഷിക്കാൻ സൈൻ ഇൻ ചെയ്യുക", "എന്റെ കുറിപ്പുകൾ", "സ്വകാര്യത", "എന്റെ അക്കൗണ്ട് ഇല്ലാതാക്കുക",
    "അധ്യായം പഠിച്ചതായി അടയാളപ്പെടുത്തുക", "പഠിച്ചു", "തുടർച്ചയായി {n} ദിവസം", "ദിവസം തുടർച്ച", "പഠിച്ച അധ്യായങ്ങൾ",
    "കുറിപ്പ് ചേർക്കുക", "എന്റെ കുറിപ്പുകൾ", "പുതിയ കുറിപ്പ്", "കുറിപ്പുകൾ തിരയുക", "ബുള്ളറ്റ്", "നമ്പറിട്ടത്", "കുറിപ്പ് ഇല്ലാതാക്കുക",
    "എല്ലാ കുറിപ്പുകളും", "തലക്കെട്ട്", "എഴുതിത്തുടങ്ങുക…", "വേദഭാഗം, ഉദാ. യോഹന്നാൻ 3:16",
    "നിങ്ങളുടെ {n} ദിവസത്തെ തുടർച്ച ഇന്നു രാത്രി അവസാനിക്കും. തുടരാൻ ഇന്ന് ഒരു അധ്യായം പഠിക്കുക.", "കുറിപ്പുകൾ ({n})"]

T["mr"] = ["सारांश", "लेखक आणि पार्श्वभूमी", "नकाशा आणि भूगोल", "भाष्य", "व्हिडिओ", "लेख", "मनन",
    "जा", "अध्याय {n}", "{book} — अध्याय {n}", "उतारा निवडा", "अध्यायावर जा",
    "बायबल", "विषय", "जीवन", "भक्ती", "पाठांतर", "नोंदी",
    "बुकमार्क", "बुकमार्क केले", "नोंद", "काढा",
    "जिथे थांबलात तिथून पुढे वाचा", "पुढे चला", "शेवटचे वाचन", "बुकमार्क", "हायलाइट",
    "साइन इन", "साइन आउट", "तुमचा अभ्यास जतन करण्यासाठी साइन इन करा", "माझ्या नोंदी", "गोपनीयता", "माझे खाते हटवा",
    "अध्याय वाचला असे चिन्हांकित करा", "वाचला", "सलग {n} दिवस", "दिवस सलग", "वाचलेले अध्याय",
    "नोंद जोडा", "माझ्या नोंदी", "नवी नोंद", "नोंदी शोधा", "बुलेट", "क्रमांकित", "नोंद हटवा",
    "सर्व नोंदी", "शीर्षक", "लिहायला सुरुवात करा…", "उतारा, उदा. योहान 3:16",
    "तुमची सलग {n} दिवसांची मालिका आज रात्री संपेल. ती टिकवण्यासाठी आज एक अध्याय वाचा.", "नोंदी ({n})"]

T["gu"] = ["સારાંશ", "લેખક અને પૃષ્ઠભૂમિ", "નકશો અને ભૂગોળ", "ભાષ્ય", "વીડિયો", "લેખો", "મનન",
    "જાઓ", "અધ્યાય {n}", "{book} — અધ્યાય {n}", "વચનભાગ પસંદ કરો", "અધ્યાય પર જાઓ",
    "બાઇબલ", "વિષયો", "જીવન", "ભક્તિ", "કંઠસ્થ", "નોંધો",
    "બુકમાર્ક", "બુકમાર્ક કર્યું", "નોંધ", "દૂર કરો",
    "જ્યાં અટક્યા હતા ત્યાંથી આગળ વાંચો", "ચાલુ રાખો", "છેલ્લે વાંચ્યું", "બુકમાર્ક", "હાઇલાઇટ",
    "સાઇન ઇન", "સાઇન આઉટ", "તમારો અભ્યાસ સાચવવા સાઇન ઇન કરો", "મારી નોંધો", "ગોપનીયતા", "મારું ખાતું કાઢી નાખો",
    "અધ્યાય વાંચ્યો તરીકે ચિહ્નિત કરો", "વાંચ્યો", "સતત {n} દિવસ", "દિવસ સતત", "વાંચેલા અધ્યાય",
    "નોંધ ઉમેરો", "મારી નોંધો", "નવી નોંધ", "નોંધો શોધો", "બુલેટ", "ક્રમાંકિત", "નોંધ કાઢી નાખો",
    "બધી નોંધો", "શીર્ષક", "લખવાનું શરૂ કરો…", "વચનભાગ, દા.ત. યોહાન 3:16",
    "તમારી સતત {n} દિવસની શ્રેણી આજે રાત્રે પૂરી થશે. ચાલુ રાખવા આજે એક અધ્યાય વાંચો.", "નોંધો ({n})"]

T["kn"] = ["ಸಾರಾಂಶ", "ಲೇಖಕ ಮತ್ತು ಹಿನ್ನೆಲೆ", "ನಕ್ಷೆ ಮತ್ತು ಭೂಗೋಳ", "ವ್ಯಾಖ್ಯಾನ", "ವೀಡಿಯೊಗಳು", "ಲೇಖನಗಳು", "ಧ್ಯಾನ",
    "ಹೋಗಿ", "ಅಧ್ಯಾ. {n}", "{book} — ಅಧ್ಯಾಯ {n}", "ವಾಕ್ಯಭಾಗ ಆರಿಸಿ", "ಅಧ್ಯಾಯಕ್ಕೆ ಹೋಗಿ",
    "ಬೈಬಲ್", "ವಿಷಯಗಳು", "ಜೀವನ", "ಧ್ಯಾನ", "ಕಂಠಪಾಠ", "ಟಿಪ್ಪಣಿಗಳು",
    "ಬುಕ್‌ಮಾರ್ಕ್", "ಬುಕ್‌ಮಾರ್ಕ್ ಮಾಡಲಾಗಿದೆ", "ಟಿಪ್ಪಣಿ", "ತೆರವುಗೊಳಿಸಿ",
    "ನಿಲ್ಲಿಸಿದಲ್ಲಿಂದ ಮುಂದುವರಿಸಿ", "ಮುಂದುವರಿಸಿ", "ಕೊನೆಯ ಓದು", "ಬುಕ್‌ಮಾರ್ಕ್‌ಗಳು", "ಹೈಲೈಟ್‌ಗಳು",
    "ಸೈನ್ ಇನ್", "ಸೈನ್ ಔಟ್", "ನಿಮ್ಮ ಅಧ್ಯಯನ ಉಳಿಸಲು ಸೈನ್ ಇನ್ ಮಾಡಿ", "ನನ್ನ ಟಿಪ್ಪಣಿಗಳು", "ಗೌಪ್ಯತೆ", "ನನ್ನ ಖಾತೆ ಅಳಿಸಿ",
    "ಅಧ್ಯಾಯ ಓದಿದೆ ಎಂದು ಗುರುತಿಸಿ", "ಓದಿದೆ", "ಸತತ {n} ದಿನಗಳು", "ದಿನಗಳ ಸರಣಿ", "ಓದಿದ ಅಧ್ಯಾಯಗಳು",
    "ಟಿಪ್ಪಣಿ ಸೇರಿಸಿ", "ನನ್ನ ಟಿಪ್ಪಣಿಗಳು", "ಹೊಸ ಟಿಪ್ಪಣಿ", "ಟಿಪ್ಪಣಿಗಳನ್ನು ಹುಡುಕಿ", "ಬುಲೆಟ್", "ಸಂಖ್ಯೆಯುಳ್ಳ", "ಟಿಪ್ಪಣಿ ಅಳಿಸಿ",
    "ಎಲ್ಲಾ ಟಿಪ್ಪಣಿಗಳು", "ಶೀರ್ಷಿಕೆ", "ಬರೆಯಲು ಪ್ರಾರಂಭಿಸಿ…", "ವಾಕ್ಯಭಾಗ, ಉದಾ. ಯೋಹಾನ 3:16",
    "ನಿಮ್ಮ {n} ದಿನಗಳ ಸರಣಿ ಇಂದು ರಾತ್ರಿ ಮುಗಿಯುತ್ತದೆ. ಮುಂದುವರಿಸಲು ಇಂದು ಒಂದು ಅಧ್ಯಾಯ ಓದಿ.", "ಟಿಪ್ಪಣಿಗಳು ({n})"]

T["or"] = ["ସାରାଂଶ", "ଲେଖକ ଓ ପୃଷ୍ଠଭୂମି", "ମାନଚିତ୍ର ଓ ଭୂଗୋଳ", "ବ୍ୟାଖ୍ୟା", "ଭିଡିଓ", "ପ୍ରବନ୍ଧ", "ଧ୍ୟାନ",
    "ଯାଆନ୍ତୁ", "ଅଧ୍ୟାୟ {n}", "{book} — ଅଧ୍ୟାୟ {n}", "ଶାସ୍ତ୍ରାଂଶ ବାଛନ୍ତୁ", "ଅଧ୍ୟାୟକୁ ଯାଆନ୍ତୁ",
    "ବାଇବଲ", "ବିଷୟ", "ଜୀବନ", "ଭକ୍ତି", "କଣ୍ଠସ୍ଥ", "ଟିପ୍ପଣୀ",
    "ବୁକମାର୍କ", "ବୁକମାର୍କ ହେଲା", "ଟିପ୍ପଣୀ", "ହଟାନ୍ତୁ",
    "ଯେଉଁଠି ଛାଡ଼ିଥିଲେ ସେଠାରୁ ଆରମ୍ଭ କରନ୍ତୁ", "ଜାରି ରଖନ୍ତୁ", "ଶେଷଥର ପଢ଼ିଥିଲେ", "ବୁକମାର୍କ", "ହାଇଲାଇଟ",
    "ସାଇନ ଇନ", "ସାଇନ ଆଉଟ", "ଆପଣଙ୍କ ଅଧ୍ୟୟନ ସଞ୍ଚୟ କରିବାକୁ ସାଇନ ଇନ କରନ୍ତୁ", "ମୋର ଟିପ୍ପଣୀ", "ଗୋପନୀୟତା", "ମୋ ଆକାଉଣ୍ଟ ବିଲୋପ କରନ୍ତୁ",
    "ଅଧ୍ୟାୟ ପଢ଼ାଗଲା ବୋଲି ଚିହ୍ନିତ କରନ୍ତୁ", "ପଢ଼ାଗଲା", "କ୍ରମାଗତ {n} ଦିନ", "ଦିନ କ୍ରମାଗତ", "ପଢ଼ା ଅଧ୍ୟାୟ",
    "ଟିପ୍ପଣୀ ଯୋଡ଼ନ୍ତୁ", "ମୋର ଟିପ୍ପଣୀ", "ନୂଆ ଟିପ୍ପଣୀ", "ଟିପ୍ପଣୀ ଖୋଜନ୍ତୁ", "ବୁଲେଟ", "ସଂଖ୍ୟାଯୁକ୍ତ", "ଟିପ୍ପଣୀ ବିଲୋପ କରନ୍ତୁ",
    "ସମସ୍ତ ଟିପ୍ପଣୀ", "ଶୀର୍ଷକ", "ଲେଖିବା ଆରମ୍ଭ କରନ୍ତୁ…", "ଶାସ୍ତ୍ରାଂଶ, ଯେପରି ଯୋହନ 3:16",
    "ଆପଣଙ୍କ କ୍ରମାଗତ {n} ଦିନ ଆଜି ରାତିରେ ଶେଷ ହେବ। ଜାରି ରଖିବାକୁ ଆଜି ଗୋଟିଏ ଅଧ୍ୟାୟ ପଢ଼ନ୍ତୁ।", "ଟିପ୍ପଣୀ ({n})"]

T["as"] = ["সাৰাংশ", "লেখক আৰু পটভূমি", "মানচিত্ৰ আৰু ভূগোল", "ব্যাখ্যা", "ভিডিঅ'", "প্ৰবন্ধ", "ধ্যান",
    "যাওক", "অধ্যায় {n}", "{book} — অধ্যায় {n}", "শাস্ত্ৰাংশ বাছক", "অধ্যায়লৈ যাওক",
    "বাইবেল", "বিষয়", "জীৱন", "ভক্তি", "মুখস্থ", "টোকা",
    "বুকমাৰ্ক", "বুকমাৰ্ক কৰা হ'ল", "টোকা", "আঁতৰাওক",
    "য'ত এৰিছিল তাৰ পৰা আৰম্ভ কৰক", "অব্যাহত ৰাখক", "শেষবাৰ পঢ়া", "বুকমাৰ্ক", "হাইলাইট",
    "ছাইন ইন", "ছাইন আউট", "আপোনাৰ অধ্যয়ন সংৰক্ষণ কৰিবলৈ ছাইন ইন কৰক", "মোৰ টোকা", "গোপনীয়তা", "মোৰ একাউণ্ট মচক",
    "অধ্যায় পঢ়া হ'ল বুলি চিহ্নিত কৰক", "পঢ়া হ'ল", "একেৰাহে {n} দিন", "দিন একেৰাহে", "পঢ়া অধ্যায়",
    "টোকা যোগ কৰক", "মোৰ টোকা", "নতুন টোকা", "টোকা বিচাৰক", "বুলেট", "সংখ্যাযুক্ত", "টোকা মচক",
    "সকলো টোকা", "শিৰোনাম", "লিখিবলৈ আৰম্ভ কৰক…", "শাস্ত্ৰাংশ, যেনে যোহন 3:16",
    "আপোনাৰ একেৰাহে {n} দিন আজি ৰাতি শেষ হ'ব। অব্যাহত ৰাখিবলৈ আজি এটা অধ্যায় পঢ়ক।", "টোকা ({n})"]

T["pa"] = ["ਸਾਰ", "ਲੇਖਕ ਅਤੇ ਪਿਛੋਕੜ", "ਨਕਸ਼ਾ ਅਤੇ ਭੂਗੋਲ", "ਟੀਕਾ", "ਵੀਡੀਓ", "ਲੇਖ", "ਮਨਨ",
    "ਜਾਓ", "ਅਧਿਆਇ {n}", "{book} — ਅਧਿਆਇ {n}", "ਹਵਾਲਾ ਚੁਣੋ", "ਅਧਿਆਇ 'ਤੇ ਜਾਓ",
    "ਬਾਈਬਲ", "ਵਿਸ਼ੇ", "ਜੀਵਨ", "ਭਗਤੀ", "ਕੰਠ", "ਨੋਟਸ",
    "ਬੁੱਕਮਾਰਕ", "ਬੁੱਕਮਾਰਕ ਕੀਤਾ", "ਨੋਟ", "ਹਟਾਓ",
    "ਜਿੱਥੇ ਛੱਡਿਆ ਸੀ ਉੱਥੋਂ ਜਾਰੀ ਰੱਖੋ", "ਜਾਰੀ ਰੱਖੋ", "ਪਿਛਲੀ ਵਾਰ ਪੜ੍ਹਿਆ", "ਬੁੱਕਮਾਰਕ", "ਹਾਈਲਾਈਟ",
    "ਸਾਈਨ ਇਨ", "ਸਾਈਨ ਆਉਟ", "ਆਪਣਾ ਅਧਿਐਨ ਸੰਭਾਲਣ ਲਈ ਸਾਈਨ ਇਨ ਕਰੋ", "ਮੇਰੇ ਨੋਟਸ", "ਪਰਦੇਦਾਰੀ", "ਮੇਰਾ ਖਾਤਾ ਮਿਟਾਓ",
    "ਅਧਿਆਇ ਪੜ੍ਹਿਆ ਹੋਇਆ ਨਿਸ਼ਾਨ ਲਗਾਓ", "ਪੜ੍ਹ ਲਿਆ", "ਲਗਾਤਾਰ {n} ਦਿਨ", "ਦਿਨ ਲਗਾਤਾਰ", "ਪੜ੍ਹੇ ਅਧਿਆਇ",
    "ਨੋਟ ਜੋੜੋ", "ਮੇਰੇ ਨੋਟਸ", "ਨਵਾਂ ਨੋਟ", "ਨੋਟਸ ਖੋਜੋ", "ਬੁਲੇਟ", "ਨੰਬਰ ਵਾਲਾ", "ਨੋਟ ਮਿਟਾਓ",
    "ਸਾਰੇ ਨੋਟਸ", "ਸਿਰਲੇਖ", "ਲਿਖਣਾ ਸ਼ੁਰੂ ਕਰੋ…", "ਹਵਾਲਾ, ਜਿਵੇਂ ਯੂਹੰਨਾ 3:16",
    "ਤੁਹਾਡਾ ਲਗਾਤਾਰ {n} ਦਿਨਾਂ ਦਾ ਸਿਲਸਿਲਾ ਅੱਜ ਰਾਤ ਖਤਮ ਹੋ ਜਾਵੇਗਾ। ਇਸਨੂੰ ਜਾਰੀ ਰੱਖਣ ਲਈ ਅੱਜ ਇੱਕ ਅਧਿਆਇ ਪੜ੍ਹੋ।", "ਨੋਟਸ ({n})"]

T["ne"] = ["सारांश", "लेखक र पृष्ठभूमि", "नक्सा र भूगोल", "व्याख्या", "भिडियोहरू", "लेखहरू", "मनन",
    "जानुहोस्", "अध्याय {n}", "{book} — अध्याय {n}", "खण्ड छान्नुहोस्", "अध्यायमा जानुहोस्",
    "बाइबल", "विषयहरू", "जीवन", "भक्ति", "कण्ठ", "टिपोटहरू",
    "बुकमार्क", "बुकमार्क गरियो", "टिपोट", "हटाउनुहोस्",
    "जहाँ छोड्नुभएको थियो त्यहीँबाट जारी राख्नुहोस्", "जारी राख्नुहोस्", "पछिल्लो पटक पढेको", "बुकमार्कहरू", "हाइलाइटहरू",
    "साइन इन", "साइन आउट", "आफ्नो अध्ययन सुरक्षित गर्न साइन इन गर्नुहोस्", "मेरा टिपोटहरू", "गोपनीयता", "मेरो खाता मेटाउनुहोस्",
    "अध्याय पढेको भनी चिन्ह लगाउनुहोस्", "पढियो", "लगातार {n} दिन", "दिन लगातार", "पढिएका अध्याय",
    "टिपोट थप्नुहोस्", "मेरा टिपोटहरू", "नयाँ टिपोट", "टिपोट खोज्नुहोस्", "बुलेट", "क्रमाङ्कित", "टिपोट मेटाउनुहोस्",
    "सबै टिपोटहरू", "शीर्षक", "लेख्न सुरु गर्नुहोस्…", "खण्ड, जस्तै यूहन्ना 3:16",
    "तपाईंको लगातार {n} दिनको क्रम आज राति टुट्नेछ। जारी राख्न आज एउटा अध्याय पढ्नुहोस्।", "टिपोटहरू ({n})"]

# Which Bible picks which wording. REVIEW = worth a fluent reader's check.
LANGS = {
    "RV09": "es", "FRA": "fr", "POR": "pt", "ARA": "ar", "FAS": "fa", "ZHS": "zh-Hans", "ZHT": "zh-Hant",
    "VIE": "vi", "TGL": "tl", "HAT": "ht",          # REVIEW: ht
    "HAU": "ha", "YOR": "yo", "IBO": "ig", "SWA": "sw", "TWI": "tw", "TWA": "tw",   # REVIEW: ha, yo, ig, tw
    "URD": "ur", "HIN": "hi", "BEN": "bn", "TAM": "ta", "TEL": "te", "MAL": "ml", "MAR": "mr",
    "GUJ": "gu", "KAN": "kn", "ORI": "or", "ASM": "as", "PAN": "pa", "NEP": "ne",   # REVIEW: or, as
}


# Added with the Plans tab (Oct 2026): the tab label and the plans page title.
KEYS += ["bn.plans", "plans.title"]
EN += ["Plans", "Reading Plans"]
_PLANS = {
    "es": ["Planes", "Planes de lectura"], "fr": ["Plans", "Plans de lecture"], "pt": ["Planos", "Planos de leitura"],
    "ar": ["الخطط", "خطط القراءة"], "fa": ["برنامه‌ها", "برنامه‌های مطالعه"], "zh-Hans": ["计划", "读经计划"],
    "zh-Hant": ["計劃", "讀經計劃"], "vi": ["Kế hoạch", "Kế hoạch đọc Kinh Thánh"], "tl": ["Plano", "Mga Plano sa Pagbasa"],
    "ht": ["Plan", "Plan lekti"], "ha": ["Tsare-tsare", "Tsare-tsaren karatu"], "yo": ["Ètò", "Ètò kíkà"],
    "ig": ["Atụmatụ", "Atụmatụ ọgụgụ"], "sw": ["Mipango", "Mipango ya kusoma"], "tw": ["Nhyehyɛe", "Akenkan nhyehyɛe"],
    "ur": ["منصوبے", "مطالعہ کے منصوبے"], "hi": ["योजनाएँ", "पठन योजनाएँ"], "bn": ["পরিকল্পনা", "পাঠ পরিকল্পনা"],
    "ta": ["திட்டங்கள்", "வாசிப்புத் திட்டங்கள்"], "te": ["ప్రణాళికలు", "పఠన ప్రణాళికలు"], "ml": ["പദ്ധതികൾ", "വായനാ പദ്ധതികൾ"],
    "mr": ["योजना", "वाचन योजना"], "gu": ["યોજનાઓ", "વાંચન યોજનાઓ"], "kn": ["ಯೋಜನೆಗಳು", "ಓದುವ ಯೋಜನೆಗಳು"],
    "or": ["ଯୋଜନା", "ପଠନ ଯୋଜନା"], "as": ["পৰিকল্পনা", "পঠন পৰিকল্পনা"], "pa": ["ਯੋਜਨਾਵਾਂ", "ਪੜ੍ਹਨ ਦੀਆਂ ਯੋਜਨਾਵਾਂ"],
    "ne": ["योजनाहरू", "पठन योजनाहरू"],
}
for _l, _w in _PLANS.items():
    T[_l] += _w


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "site", "i18n")
    os.makedirs(out, exist_ok=True)
    assert len(EN) == len(KEYS)
    for lang, words in T.items():
        assert len(words) == len(KEYS), (lang, len(words))
        for k, en, w in zip(KEYS, EN, words):
            for ph in ("{n}", "{book}"):
                assert (ph in en) == (ph in w), (lang, k, ph)
        with open(os.path.join(out, lang + ".json"), "w", encoding="utf-8") as f:
            json.dump(dict(zip(KEYS, words)), f, ensure_ascii=False, indent=0, sort_keys=True)
    with open(os.path.join(out, "en.json"), "w", encoding="utf-8") as f:
        json.dump(dict(zip(KEYS, EN)), f, ensure_ascii=False, indent=0, sort_keys=True)
    print(f"wrote {len(T) + 1} languages, {len(KEYS)} labels each")


if __name__ == "__main__":
    main()
