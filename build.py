# -*- coding: utf-8 -*-
# تشغيل: python3 build.py  -> يولّد كل الصفحات (عربي + إنجليزي) + sitemap.xml
import os,json,html
from urllib.parse import quote
DOMAIN="https://shfaa.online"; PHONE="201098997347"
FB="https://www.facebook.com/share/1HTjj8ZCZ2/"; IG="https://www.instagram.com/shifacenter2025"; TT="https://www.tiktok.com/@shifa.home.care.c"
E_=html.escape
# ---- الآراء: استبدلها بالحقيقية (ar, en, الاسم, المدينة) ----
REVIEWS=[("التمريض كان محترم جدًا والمتابعة ماشية بدقة. حسّينا إن والدي في أمان.","The nursing was very respectful and follow-up was precise. We felt our father was safe.","أم محمد","طنطا","Um Mohamed","Tanta"),
("جهاز الفاكيوم فرق كتير في التئام الجرح، وفريق شفا متعاون جدًا.","The vacuum device made a big difference in wound healing, and the team is very cooperative.","أحمد س.","المحلة الكبرى","Ahmed S.","El Mahalla"),
("الإقامة المنزلية كانت راحة كبيرة لينا، والممرضة ملتزمة ومتابعة كل صغيرة.","Home residence care was a huge relief; the nurse was committed and tracked every detail.","هبة ع.","القاهرة","Heba A.","Cairo"),
("خدمة سريعة في الطوارئ ووصلوا في وقت قياسي. شكرًا لكم.","Fast emergency response; they arrived in record time. Thank you.","محمود","كفر الزيات","Mahmoud","Kafr El Zayat"),
("اهتمام حقيقي بمريضنا وتواصل مستمر معانا طول اليوم.","Genuine care for our patient and constant communication all day.","نادين ح.","الإسكندرية","Nadine H.","Alexandria"),
("من أحسن مراكز الرعاية المنزلية، ما شاء الله على مجهودهم.","One of the best home care centers. Great effort from the whole team.","أبو يوسف","المنصورة","Abu Yousef","Mansoura")]
CATS={
"quick":{"ic":"⚡","ar":("الخدمات السريعة","كانيولا، قياس العلامات الحيوية، غيارات، حقن، قسطرة، نقل دم وأكثر.","تصفح الخدمات","اضغط على أي خدمة وهتتحول مباشرة لواتساب لطلبها."),
"en":("Quick Services","Cannula, vital signs, dressings, injections, catheters, blood transfusion and more.","Browse services","Tap any service to request it instantly on WhatsApp."),
"items":[("🚑","طوارئ (حروق – جروح – إغماء)","Emergencies (burns, wounds, fainting)"),("🩸","قياس العلامات الحيوية والوظيفية","Vital & functional signs measurement"),("💉","تركيب الكانيولات","IV cannula insertion"),("🧴","تركيب القسطرة البولية","Urinary catheter insertion"),("🍼","تركيب الرايل NGT / أنبوب التغذية","NGT / feeding tube insertion"),("💉","إعطاء الحقن / اختبارات الحساسية","Injections / allergy tests"),("💧","تركيب المحاليل الوريدية","IV fluids administration"),("🩹","الغيار على الجروح / الحروق / القدم السكري / الالتهاب الخلوي","Dressing: wounds, burns, diabetic foot, cellulitis"),("🛏️","الغيار على قرح الفراش","Pressure ulcer dressing"),("🫁","جلسات الأكسجين وجلسات الاستنشاق","Oxygen & nebulizer sessions"),("🩸","نقل الدم – البلازما – الصفائح – الألبيومين – الأحماض الأمينية – التغذية الكاملة TPN","Blood, plasma, platelets, albumin, amino acids & TPN"),("🫀","تركيب أجهزة التنفس الصناعي","Ventilator setup"),("🩹","الغيار على الكولوستومي / غيار كيس التجميع","Colostomy care / bag change"),("💊","عمل الحقن الشرجية (Enema)","Enema administration"),("🧑‍⚕️","عمل كير كامل للمريض","Complete patient care"),("🩺","تركيب سنترال لاين","Central line insertion","بإشراف طبي","Under medical supervision"),("🩺","تركيب ماهوكر","Mahurkar catheter insertion","بإشراف طبي","Under medical supervision"),("🧪","البزل لحالات الفشل الكبدي","Paracentesis for liver failure","بإشراف طبي","Under medical supervision")]},
"stay":{"ic":"🏠","ar":("حالات الإقامة المنزلية","ممرض أو ممرضة مقيم مع المريض بنظام الشيفتات: صباحي، مسائي، سهر أو يوم كامل.","تصفح الحالات","اختر نظام الشيفت المناسب لحالة مريضك."),
"en":("Home Residence Care","A resident nurse with your patient in shifts: morning, evening, night or full day.","Browse options","Choose the shift that suits your patient."),
"items":[("🌅","شيفت صباحي","Morning shift","من 8 ص إلى 2 م","8 AM – 2 PM"),("🌇","شيفت مسائي","Evening shift","من 2 م إلى 8 م","2 PM – 8 PM"),("🌙","شيفت سهر","Night shift","من 8 م إلى 8 ص","8 PM – 8 AM"),("☀️","شيفت يوم كامل","Full-day shift","من 8 ص إلى 8 ص","8 AM – 8 AM")]},
"follow":{"ic":"❤️","ar":("حالات المتابعة","ما بعد العمليات، قرح الفراش، كبار السن، الغيبوبة والشلل والعناية المركزة.","تصفح الحالات","متابعة تمريضية وطبية منتظمة للحالات المستقرة والحرجة."),
"en":("Follow-up Care","Post-surgery, pressure ulcers, elderly care, coma, paralysis and intensive care.","Browse cases","Regular nursing and medical follow-up for stable and critical cases."),
"items":[("🏥","حالات الجراحة العامة وما بعد العمليات","General surgery & post-operative care"),("🛏️","قرح الفراش وجهاز الفاكيوم","Pressure ulcers & vacuum (VAC) therapy"),("👴","كبار السن (الزهايمر – الحالات النفسية – الضمور العضلي والعصبي – الأمراض المزمنة)","Elderly care (Alzheimer's, psychiatric cases, muscular/neural atrophy, chronic diseases)"),("🧠","حالات الغيبوبة والشلل والجلطات","Coma, paralysis & stroke cases"),("🫀","حالات العناية المركزة","Intensive care cases")]}}
WHY=[("🛡️","الحد من العدوى","رعاية في بيئة آمنة بعيدًا عن عدوى المستشفيات.","Infection control","Safe care away from hospital-acquired infections."),
("🫁","أجهزة عناية مركزة","أسرّة، مونيتور، تنفس صناعي، سرنجة كهربائية، شفاط وفاكيوم.","ICU equipment","Beds, monitors, ventilators, syringe pumps, suction and vacuum."),
("🧪","تحاليل وأشعة منزلية","الأشعات التشخيصية والمعملية في بيت المريض.","Home labs & imaging","Diagnostic imaging and lab tests at the patient's home."),
("🥗","تغذية وعلاج طبيعي","تغذية علاجية وجلسات علاج طبيعي ضمن خطة المتابعة.","Nutrition & physiotherapy","Therapeutic nutrition and physiotherapy within the care plan."),
("👩‍⚕️","استشارات وزيارات طبية","زيارات لجميع التخصصات ومتابعة الحالات طوال اليوم.","Medical visits","Visits from all specialties and round-the-clock follow-up."),
("💊","أدوية العناية المركزة","نوفر أدوية العناية المركزة للحالات الحرجة.","ICU medications","We provide ICU medications for critical cases."),
("🛏️","الوقاية من قرح الفراش","رعاية مكثفة تحمي من قرح الفراش والالتهاب الرئوي الاستنشاقي.","Pressure ulcer prevention","Intensive nursing that prevents bedsores and aspiration pneumonia."),
("👴","كبار السن وذوو الاحتياجات","عناية كاملة بمرضى الغيبوبة والجلطات وكبار السن.","Elderly & special needs","Complete care for coma, stroke and elderly patients.")]
FAQ=[("هل تغطون كل محافظات مصر؟","نعم، نقدم خدمات الإقامة المنزلية في جميع محافظات مصر، بينما تتوفر خدمات الطوارئ والخدمات السريعة في محافظة الغربية ونواحيها.","Do you cover all of Egypt?","Yes. Home residence care is available in all Egyptian governorates, while emergency and quick services are available in Gharbia and nearby areas."),
("ما هي أنظمة الإقامة المنزلية؟","شيفت صباحي (8 ص – 2 م)، مسائي (2 م – 8 م)، سهر (8 م – 8 ص) أو يوم كامل (8 ص – 8 ص).","What are the home residence shift options?","Morning (8 AM–2 PM), evening (2 PM–8 PM), night (8 PM–8 AM) or full day (8 AM–8 AM)."),
("هل توفرون أجهزة العناية المركزة في المنزل؟","نعم: أسرّة، مونيتور، مراتب هوائية، سرنجات كهربائية، أجهزة قياس الضغط والسكر والأكسجين، شفاط، فاكيوم للجروح وقرح الفراش، أجهزة تنفس صناعي وجهاز رسم القلب.","Do you provide ICU equipment at home?","Yes: beds, monitors, air mattresses, syringe pumps, BP/glucose/oxygen meters, suction, wound vacuum, ventilators and ECG."),
("كيف أطلب خدمة؟","اضغط على أي خدمة في الموقع وسيفتح واتساب برسالة جاهزة على الرقم 01098997347.","How do I request a service?","Tap any service on the site and WhatsApp opens with a ready message to 01098997347.")]
T={"ar":dict(dir="rtl",home="الرئيسية",about="من نحن",services="خدماتنا",why="لماذا شفا",gal="أعمالنا",rev="آراء العملاء",faq="أسئلة شائعة",contact="تواصل معنا",wabtn="تواصل واتساب",
title="شفا | رعاية منزلية وتمريض منزلي في مصر – عناية مركزة وإقامة 24 ساعة",desc="مركز شفا للرعاية الطبية والتمريضية المنزلية: تمريض منزلي، عناية مركزة بالمنزل، غيارات وقرح فراش، رعاية كبار السن وإقامة منزلية 24 ساعة في جميع محافظات مصر. اتصل 01098997347.",
pill="خدمة في جميع محافظات مصر · طوارئ سريعة بالغربية",h1a="شفا… ",h1b="رعاية كاملة",h1c=" في بيتك",lead="تمريض متخصص وعناية مركزة وأجهزة طبية ومتابعة على مدار اليوم، من غير ما مريضك يتحرك ولا يتعرض لعدوى المستشفيات.",
req="اطلب خدمة الآن",browse="تصفح الخدمات",waq="أريد طلب خدمة",waq2="أريد الاستفسار عن خدماتكم",chips=("🩺 فريق تمريض متخصص","🏠 رعاية في بيتك","⏱ متاحين 24/7"),
st=("نخدمك منذ عام","محافظة نغطيها","ساعة متابعة يوميًا","خدمة سريعة"),about_t="عن مركز شفا",
about_p="مركز شفا للرعاية الصحية الكاملة يقدم الرعاية والجودة الصحية بالمنزل مع توفير كل الخدمات دون تحريك المريض وتعريضه للعدوى أو مخاطر السقوط والمضاعفات. نعتمد على نخبة من أخصائيي التمريض في العناية المركزة والطوارئ والأطفال وحديثي الولادة والحالات الحرجة ورعاية كبار السن.",
ticks=("خبرة في الرعاية المنزلية من 2017","خدمات الإقامة المنزلية في جميع محافظات مصر","الطوارئ والخدمات السريعة في محافظة الغربية ونواحيها","رعاية خاصة لمرضى الأورام وتلف الكبد وضعف المناعة"),
svc_p="اختر القسم المناسب وهتلاقي كل الخدمات جواه، وبضغطة واحدة تطلبها على واتساب.",why_p="الرعاية الكاملة… طريقك للشفاء",why_cta="اسأل عن الأجهزة والخدمات الإضافية",wa_extra="أريد الاستفسار عن الأجهزة والخدمات الإضافية",
gal_p="تصميمات وخدمات من صفحاتنا.",rev_p="ثقة أسر كتير هي أكبر شهادة لينا.",map_t="نغطي مصر كلها",map_p="الإقامة المنزلية في كل المحافظات، والطوارئ السريعة بالغربية.",hot="الغربية (طوارئ وخدمات سريعة)",
cta_t="محتاج رعاية لمريضك؟",cta_p="كلمنا دلوقتي وفريقنا يرد عليك فورًا.",wa_l="واتساب",call="أو اتصل",hq="المقر الإداري: قحافة – طنطا – الغربية",fb="فيسبوك",ig="إنستجرام",tt="تيك توك",
back="→ الرجوع للرئيسية",other="خدمة أخرى غير مذكورة",other_s="اكتب لنا احتياجك",order="اطلب ←",waother="أريد طلب خدمة أخرى",foot="© 2026 مركز شفا للرعاية الطبية والتمريضية المنزلية",other_l="English",lcode="ar",locale="ar_EG"),
"en":dict(dir="ltr",home="Home",about="About",services="Services",why="Why Shifa",gal="Our Work",rev="Reviews",faq="FAQ",contact="Contact",wabtn="WhatsApp us",
title="Shifa Home Care | Home Nursing & ICU Care at Home in Egypt – 24/7",desc="Shifa Home Care Center: professional home nursing, ICU care at home, wound & pressure-ulcer dressing, elderly care and 24/7 residence nursing across all Egyptian governorates. Call 01098997347.",
pill="Serving all of Egypt · Fast emergency care in Gharbia",h1a="Shifa… ",h1b="Complete care",h1c=" at your home",lead="Specialized nursing, ICU care, medical equipment and round-the-clock follow-up, without moving your patient or exposing them to hospital infections.",
req="Request a service",browse="Browse services",waq="I would like to request:",waq2="I would like to ask about your services",chips=("🩺 Specialized nurses","🏠 Care at home","⏱ Available 24/7"),
st=("Serving since","Governorates covered","Hours of care daily","Quick services"),about_t="About Shifa",
about_p="Shifa delivers complete healthcare and quality at home, providing every service without moving the patient or exposing them to infection, falls and complications. Our team is built on elite nursing specialists in intensive care, emergency, pediatrics, neonatal, critical cases and elderly care.",
ticks=("Home care experience since 2017","Home residence care in all Egyptian governorates","Emergency & quick services in Gharbia and nearby areas","Special care for cancer, liver failure and low-immunity patients"),
svc_p="Pick a category to see every service, and request any of them on WhatsApp with one tap.",why_p="Complete care… your way to recovery",why_cta="Ask about equipment & extra services",wa_extra="I would like to ask about equipment and extra services",
gal_p="Designs and services from our pages.",rev_p="The trust of many families is our greatest testimony.",map_t="Covering all of Egypt",map_p="Residence care in every governorate, fast emergency care in Gharbia.",hot="Gharbia (emergency & quick services)",
cta_t="Need care for your patient?",cta_p="Message us now and our team replies right away.",wa_l="WhatsApp",call="or call",hq="HQ: Qahafa, Tanta, Gharbia",fb="Facebook",ig="Instagram",tt="TikTok",
back="← Back to home",other="Another service",other_s="Tell us what you need",order="Request →",waother="I would like to request another service",foot="© 2026 Shifa Home Care Center",other_l="العربية",lcode="en",locale="en_US")}
GOV={"ar":["القاهرة","الجيزة","الإسكندرية","مطروح","الساحل الشمالي","شرم الشيخ","المنوفية","الدقهلية","البحيرة","المنصورة","الإسماعيلية","السويس","وجميع محافظات مصر (إقامة منزلية)"],
"en":["Cairo","Giza","Alexandria","Matrouh","North Coast","Sharm El Sheikh","Monufia","Dakahlia","Beheira","Mansoura","Ismailia","Suez","and all Egyptian governorates (residence care)"]}
WAI='<svg viewBox="0 0 32 32"><path d="M16 3a13 13 0 0 0-11 19.8L3 29l6.4-2A13 13 0 1 0 16 3zm7.6 18.4c-.3.9-1.8 1.7-2.5 1.8-.6.1-1.4.1-2.3-.2-2.8-1-4.6-3.3-5.8-5.1-.8-1.2-1.4-2.6-1.2-4 .1-1 .6-1.7 1.1-2.2.3-.3.7-.3 1-.3h.7c.2 0 .5 0 .7.6l1 2.3c.1.2.1.4 0 .6l-.5.7c-.2.2-.3.4-.1.7.7 1.2 1.7 2.2 2.9 2.8.3.2.5.1.7-.1l.8-1c.2-.3.5-.3.8-.2l2.2 1c.3.2.5.2.6.4.1.2.1.8-.1 1.4z"/></svg>'
def wa(t):return f"https://wa.me/{PHONE}?text={quote(t)}"
def path(l,k=None):
    p=("/en" if l=="en" else "")+("/"+k if k else "")
    return (p+"/") if p else "/"
def head(l,k,title,desc,ld):
    t=T[l];other="en" if l=="ar" else "ar"
    return f'''<!DOCTYPE html><html lang="{l}" dir="{t["dir"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E_(title)}</title><meta name="description" content="{E_(desc)}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{DOMAIN}{path(l,k)}"><link rel="alternate" hreflang="ar" href="{DOMAIN}{path('ar',k)}"><link rel="alternate" hreflang="en" href="{DOMAIN}{path('en',k)}"><link rel="alternate" hreflang="x-default" href="{DOMAIN}{path('ar',k)}">
<meta name="theme-color" content="#0b2a5b"><meta name="geo.region" content="EG"><meta name="geo.placename" content="Tanta, Gharbia">
<meta property="og:type" content="website"><meta property="og:site_name" content="Shifa Home Care"><meta property="og:locale" content="{t["locale"]}"><meta property="og:title" content="{E_(title)}"><meta property="og:description" content="{E_(desc)}"><meta property="og:url" content="{DOMAIN}{path(l,k)}"><meta property="og:image" content="{DOMAIN}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E_(title)}"><meta name="twitter:description" content="{E_(desc)}"><meta name="twitter:image" content="{DOMAIN}/assets/og.jpg">
<link rel="icon" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/icon-192.png"><link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
<script>try{{var s=localStorage.getItem('theme');document.documentElement.dataset.theme=s||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{document.documentElement.dataset.theme='light'}}</script>
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script></head><body><div id="bar"></div>'''
def header(l,k):
    t=T[l];o="en" if l=="ar" else "ar";b=path(l)
    return f'''<header><div class="wrap nav"><a class="brand" href="{b}" aria-label="Shifa"><img class="ll" src="/assets/logo-light.png" alt="{E_("شعار شفا" if l=="ar" else "Shifa logo")}" width="58" height="58"><img class="ld" src="/assets/logo-dark.png" alt="" width="58" height="58"></a>
<nav class="links" id="links"><a href="{b}">{t["home"]}</a><a href="{b}#about">{t["about"]}</a><a href="{b}#services">{t["services"]}</a><a href="{b}#why">{t["why"]}</a><a href="{b}#gallery">{t["gal"]}</a><a href="{b}#reviews">{t["rev"]}</a><a href="{b}#faq">{t["faq"]}</a><a href="{b}#contact">{t["contact"]}</a></nav>
<div class="tools"><a class="btn g" href="{wa(t["waq2"])}" target="_blank" rel="noopener">{t["wabtn"]}</a><a class="ib" href="{path(o,k)}" hreflang="{o}" lang="{o}" aria-label="{t["other_l"]}">{"EN" if l=="ar" else "ع"}</a><button class="ib" id="tg" aria-label="Theme">🌙</button><button class="ib burger" id="bg" aria-label="Menu">☰</button></div></div></header>'''
def foot(l):
    t=T[l];return f'<a class="fab" href="{wa(t["waq2"])}" target="_blank" rel="noopener" aria-label="WhatsApp">{WAI}</a><script src="/app.js" defer></script></body></html>'
def biz(l):
    t=T[l];return {"@context":"https://schema.org","@type":["MedicalBusiness","HomeAndConstructionBusiness"][0],"name":"Shifa Home Care Center | مركز شفا للرعاية الطبية والتمريضية المنزلية","alternateName":["شفا","Shfaa","Shifa Home Care"],"url":DOMAIN+"/","logo":DOMAIN+"/assets/icon-512.png","image":DOMAIN+"/assets/og.jpg","description":t["desc"],"telephone":["+201098997347","+201027760827"],"foundingDate":"2017","address":{"@type":"PostalAddress","streetAddress":"Qahafa","addressLocality":"Tanta","addressRegion":"Gharbia","addressCountry":"EG"},"areaServed":{"@type":"Country","name":"Egypt"},"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"},"sameAs":[FB,IG,TT],"availableLanguage":["Arabic","English"]}
def home(l):
    t=T[l];i=0 if l=="ar" else 1;b=path(l)
    ld=[biz(l),{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f[0+2*i],"acceptedAnswer":{"@type":"Answer","text":f[1+2*i]}} for f in FAQ]}]
    cats="".join(f'<a class="cat rv" href="{path(l,k)}"><div class="ic">{c["ic"]}</div><h3>{c[l][0]}</h3><p>{c[l][1]}</p><span class="more">{c[l][2]} {"←" if l=="ar" else "→"}</span></a>' for k,c in CATS.items())
    why="".join(f'<div class="card rv"><div class="ic">{w[0]}</div><h4>{w[1] if l=="ar" else w[3]}</h4><p>{w[2] if l=="ar" else w[4]}</p></div>' for w in WHY)
    r="".join(f'<div class="rev"><div class="st">★★★★★</div><p>{E_(x[0+i])}</p><small>{E_(x[2+2*i])} · {E_(x[3+2*i])}</small></div>' for x in REVIEWS);r*=2
    g="".join(f'<img class="work" src="/assets/work{n}.webp" alt="{"تصميم خدمات شفا للرعاية المنزلية" if l=="ar" else "Shifa home care services design"} {n}" loading="lazy" height="420">' for n in (1,2,3,4,1,2,3,4))
    gov="".join(f'<span>{x}</span>' for x in GOV[l])
    faq="".join(f'<details class="rv"><summary>{f[0+2*i]}</summary><p>{f[1+2*i]}</p></details>' for f in FAQ)
    return head(l,None,t["title"],t["desc"],ld)+header(l,None)+f'''<main><section class="hero"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="dots"></div><div class="wrap">
<div><span class="pill"><i></i>{t["pill"]}</span><h1>{t["h1a"]}<span>{t["h1b"]}</span>{t["h1c"]}</h1><p class="lead">{t["lead"]}</p>
<div class="cta"><a class="btn g" href="{wa(t["waq"])}" target="_blank" rel="noopener">{t["req"]}</a><a class="btn o" href="#services">{t["browse"]}</a></div></div>
<div class="visual"><div class="ring"></div><div class="ring r2"></div><div class="orb"><img class="ll" src="/assets/logo-light.png" alt="Shifa" width="250" height="250"><img class="ld" src="/assets/logo-dark.png" alt="" width="250" height="250"></div>
<div class="chip a">{t["chips"][0]}</div><div class="chip b">{t["chips"][1]}</div><div class="chip c">{t["chips"][2]}</div></div></div>
<svg class="ecg" viewBox="0 0 1200 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40H300l20-28 22 56 20-46 14 18H640l20-28 22 56 20-46 14 18H1200"/></svg></section>
<div class="stats"><div class="wrap"><div><b data-n="2017">2017</b>{t["st"][0]}</div><div><b data-n="27">27</b>{t["st"][1]}</div><div><b data-n="24">24</b>{t["st"][2]}</div><div><b data-n="18" data-s="+">18+</b>{t["st"][3]}</div></div></div>
<section id="about" class="about"><div class="wrap"><div class="rv"><div class="box"><img class="ll" src="/assets/logo-light.png" alt="Shifa" loading="lazy"><img class="ld" src="/assets/logo-dark.png" alt="" loading="lazy"></div></div>
<div class="rv"><h2 style="font-size:2.2rem;font-weight:900;color:var(--navy)">{t["about_t"]}</h2><p style="color:var(--mut);margin-top:10px">{t["about_p"]}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in t["ticks"])}</ul></div></div></section>
<section id="services" class="alt"><div class="wrap"><div class="head rv"><h2>{t["services"]}</h2><p>{t["svc_p"]}</p></div><div class="cats">{cats}</div></div></section>
<section id="why"><div class="wrap"><div class="head rv"><h2>{t["why"]}</h2><p>{t["why_p"]}</p></div><div class="grid4">{why}</div><div style="text-align:center;margin-top:32px"><a class="btn g" href="{wa(t["wa_extra"])}" target="_blank" rel="noopener">{t["why_cta"]}</a></div></div></section>
<section id="gallery" class="alt"><div class="wrap"><div class="head rv"><h2>{t["gal"]}</h2><p>{t["gal_p"]}</p></div></div><div class="slider"><div class="track w">{g}</div></div></section>
<section id="coverage"><div class="wrap"><div class="head rv"><h2>{t["map_t"]}</h2><p>{t["map_p"]}</p></div><div class="map rv"><span class="hot">{t["hot"]}</span>{gov}</div></div></section>
<section id="reviews" class="alt"><div class="wrap"><div class="head rv"><h2>{t["rev"]}</h2><p>{t["rev_p"]}</p></div></div><div class="slider"><div class="track">{r}</div></div></section>
<section id="faq"><div class="wrap"><div class="head rv"><h2>{t["faq"]}</h2></div><div class="faq">{faq}</div></div></section>
<section id="contact"><div class="wrap"><div class="contact rv"><h2>{t["cta_t"]}</h2><p>{t["cta_p"]}</p><a class="btn g" href="{wa(t["waq"])}" target="_blank" rel="noopener" style="font-size:1.15rem"><span dir="ltr">01098997347</span> · {t["wa_l"]}</a>
<p style="margin:18px 0 0;font-size:.95rem">{t["call"]}: <a href="tel:+201027760827" dir="ltr">01027760827</a> · {t["hq"]}</p>
<div class="soc"><a href="{FB}" target="_blank" rel="noopener">{t["fb"]}</a><a href="{IG}" target="_blank" rel="noopener">{t["ig"]}</a><a href="{TT}" target="_blank" rel="noopener">{t["tt"]}</a></div></div></div></section></main><footer>{t["foot"]}</footer>'''+foot(l)
def sub(l,k):
    t=T[l];c=CATS[k];i=0 if l=="ar" else 1;n=c[l][0]
    title=f"{n} | {'شفا للرعاية المنزلية' if l=='ar' else 'Shifa Home Care'}";desc=c[l][1]+" "+("اطلب عبر واتساب 01098997347." if l=="ar" else "Request via WhatsApp 01098997347.")
    ld=[biz(l),{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":t["home"],"item":DOMAIN+path(l)},{"@type":"ListItem","position":2,"name":n,"item":DOMAIN+path(l,k)}]}]
    items=""
    for it in c["items"]:
        nm=it[1+i];note=(it[3+i] if len(it)>3 else "")
        items+=f'<a href="{wa(t["waq"]+" "+nm)}" target="_blank" rel="noopener"><i>{it[0]}</i><span>{E_(nm)}{f"<small>{note}</small>" if note else ""}</span><em>{t["order"]}</em></a>'
    items+=f'<a href="{wa(t["waother"])}" target="_blank" rel="noopener"><i>➕</i><span>{t["other"]}<small>{t["other_s"]}</small></span><em>{t["order"]}</em></a>'
    return head(l,k,title,desc,ld)+header(l,k)+f'<main class="page"><div class="wrap"><a class="crumb" href="{path(l)}">{t["back"]}</a><div class="head" style="text-align:start;margin:0"><h1 style="font-size:2.4rem">{c["ic"]} {n}</h1><p>{c[l][3]}</p></div><div class="svc">{items}</div></div></main><footer>{t["foot"]}</footer>'+foot(l)
urls=[]
for l in("ar","en"):
    for k in [None]+list(CATS):
        p=path(l,k);d=("."+p);os.makedirs(d,exist_ok=True)
        open(d+"index.html","w",encoding="utf-8").write(home(l) if k is None else sub(l,k));urls.append(k)
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
for k in [None]+list(CATS):
    for l in("ar","en"):
        sm+=f'<url><loc>{DOMAIN}{path(l,k)}</loc><changefreq>weekly</changefreq><priority>{"1.0" if k is None else "0.8"}</priority>'+"".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{DOMAIN}{path(x,k)}"/>' for x in("ar","en"))+'</url>'
open("sitemap.xml","w").write(sm+"</urlset>")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
open("manifest.webmanifest","w",encoding="utf-8").write(json.dumps({"name":"شفا للرعاية المنزلية","short_name":"شفا","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#0b2a5b","lang":"ar","dir":"rtl","icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},ensure_ascii=False))
open("vercel.json","w").write(json.dumps({"cleanUrls":False,"trailingSlash":True,"headers":[{"source":"/assets/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=31536000, immutable"}]},{"source":"/(.*)","headers":[{"key":"X-Content-Type-Options","value":"nosniff"},{"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"}]}]}))
print("built",len(urls),"pages")
