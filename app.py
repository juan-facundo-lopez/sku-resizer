import io
import os
import zipfile

import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="SKU Resizer — Image Operations",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600&display=swap');

    :root {
        --ink: #f7f9ff;
        --muted: #8d97ba;
        --line: rgba(130, 154, 255, 0.14);
        --panel: rgba(17, 25, 54, 0.76);
        --blue: #4b7cff;
        --navy: #070b18;
    }

    * { box-sizing: border-box; }

    html, body, [class*="css"] { font-family: "DM Sans", sans-serif; }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 9% 8%, rgba(74, 113, 224, 0.29), transparent 27%),
            radial-gradient(circle at 86% 16%, rgba(53, 86, 190, 0.18), transparent 29%),
            linear-gradient(145deg, #111a35 0%, #090e20 48%, #060915 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: .18;
        background-image:
            linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
        background-size: 52px 52px;
        mask-image: linear-gradient(to bottom, black, transparent 82%);
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { right: 1rem; }

    .block-container {
        max-width: 1420px;
        padding: 2rem 3rem 4rem;
        animation: rise .65s cubic-bezier(.22,.8,.28,1) both;
    }

    @keyframes rise {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: .25rem 0 2.6rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: .8rem;
        font-family: "Manrope", sans-serif;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: -.01em;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        font-size: 1.05rem;
        background: linear-gradient(145deg, #79a0ff, #3768ef);
        box-shadow: 0 10px 30px rgba(69, 112, 255, .38), inset 0 1px rgba(255,255,255,.35);
    }

    .top-status {
        display: inline-flex;
        align-items: center;
        gap: .55rem;
        padding: .55rem .85rem;
        border: 1px solid var(--line);
        border-radius: 999px;
        color: #b8c3e9;
        background: rgba(14, 21, 45, .58);
        font-size: .78rem;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 99px;
        background: #78e6b0;
        box-shadow: 0 0 14px #54d89a;
    }

    .hero { max-width: 960px; margin-bottom: 2.2rem; }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: .5rem;
        color: #96adff;
        text-transform: uppercase;
        letter-spacing: .15em;
        font-size: .69rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .eyebrow::before {
        content: "";
        width: 22px;
        height: 1px;
        background: #6f92ff;
    }

    .hero h1 {
        max-width: 900px;
        margin: 0;
        font-family: "Manrope", sans-serif;
        font-size: clamp(3rem, 6vw, 6.4rem);
        font-weight: 400;
        line-height: .96;
        letter-spacing: -.065em;
        color: #f9fbff;
    }

    .hero h1 span { color: #829cf1; }

    .hero p {
        max-width: 650px;
        margin: 1.35rem 0 0;
        color: #9aa4c6;
        font-size: 1.03rem;
        line-height: 1.7;
    }

    .section-kicker {
        margin: .1rem 0 .75rem;
        color: #7784ad;
        font-size: .68rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
    }

    .section-title {
        margin: 0 0 .25rem;
        color: #f5f7ff;
        font-family: "Manrope", sans-serif;
        font-size: 1.55rem;
        font-weight: 500;
        letter-spacing: -.035em;
    }

    .section-copy {
        margin: 0 0 1.1rem;
        color: #828daf;
        font-size: .88rem;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: .8rem;
        margin-bottom: .8rem;
    }

    .metric-card, .workflow-card {
        position: relative;
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 22px;
        background: linear-gradient(145deg, rgba(26, 38, 78, .86), rgba(13, 20, 43, .82));
        box-shadow: 0 20px 60px rgba(0,0,0,.2), inset 0 1px rgba(255,255,255,.035);
    }

    .metric-card { min-height: 164px; padding: 1.2rem; }

    .metric-card::after {
        content: "";
        position: absolute;
        width: 120px;
        height: 120px;
        right: -48px;
        top: -48px;
        border-radius: 50%;
        background: rgba(77, 121, 255, .12);
        filter: blur(2px);
    }

    .metric-label { color: #8894ba; font-size: .72rem; }

    .metric-value {
        margin-top: .7rem;
        color: #f7f9ff;
        font-family: "Manrope", sans-serif;
        font-size: 2.15rem;
        font-weight: 400;
        letter-spacing: -.055em;
    }

    .metric-value small { color: #7181b0; font-size: .82rem; letter-spacing: 0; }
    .metric-foot { position: absolute; bottom: 1rem; color: #7785ae; font-size: .68rem; }

    .quality-bars {
        display: flex;
        align-items: end;
        gap: 4px;
        height: 38px;
        margin-top: .95rem;
    }

    .quality-bars i {
        display: block;
        width: 7px;
        border-radius: 4px;
        background: linear-gradient(to top, #376ef3, #86a5ff);
        box-shadow: 0 0 13px rgba(70,111,255,.24);
    }

    .workflow-card { padding: 1.2rem 1.25rem; }

    .workflow-step {
        display: flex;
        align-items: center;
        gap: .8rem;
        padding: .72rem 0;
        border-bottom: 1px solid rgba(123, 145, 224, .1);
        color: #c5ccec;
        font-size: .82rem;
    }

    .workflow-step:last-child { border-bottom: 0; }

    .step-number {
        display: grid;
        place-items: center;
        width: 27px;
        height: 27px;
        flex: 0 0 27px;
        border-radius: 9px;
        color: #abc0ff;
        background: rgba(73, 113, 244, .16);
        border: 1px solid rgba(100, 136, 255, .22);
        font-size: .68rem;
    }

    [data-testid="stFileUploader"] {
        padding: 1rem;
        border: 1px solid var(--line);
        border-radius: 24px;
        background: linear-gradient(145deg, rgba(20, 30, 63, .92), rgba(10, 16, 35, .88));
        box-shadow: 0 26px 70px rgba(0,0,0,.26), inset 0 1px rgba(255,255,255,.04);
    }

    [data-testid="stFileUploader"] > label { display: none; }

    [data-testid="stFileUploadDropzone"] {
        min-height: 235px;
        border: 1px dashed rgba(111, 143, 255, .48);
        border-radius: 18px;
        background:
            radial-gradient(circle at 50% 15%, rgba(68, 109, 255, .15), transparent 55%),
            rgba(17, 25, 53, .58);
        transition: .25s ease;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #769aff;
        background-color: rgba(33, 49, 95, .68);
        transform: translateY(-1px);
    }

    [data-testid="stFileUploadDropzone"] svg { color: #7397ff; width: 42px; height: 42px; }

    [data-testid="stFileUploadDropzone"] button {
        color: #eaf0ff !important;
        border: 1px solid rgba(121, 151, 255, .3) !important;
        border-radius: 12px !important;
        background: rgba(72, 109, 226, .16) !important;
    }

    [data-testid="stFileUploadDropzoneInstructions"] > div > span { color: #f1f4ff; font-size: .95rem; }
    [data-testid="stFileUploadDropzoneInstructions"] small { color: #7783a7 !important; }

    .stButton > button[kind="primary"], .stDownloadButton > button {
        min-height: 3.45rem;
        border: 0 !important;
        border-radius: 15px !important;
        color: #fff !important;
        font-weight: 700 !important;
        letter-spacing: -.01em;
        background: linear-gradient(110deg, #346bf3, #5986ff) !important;
        box-shadow: 0 14px 34px rgba(50, 101, 246, .3) !important;
        transition: .22s ease !important;
    }

    .stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.09);
        box-shadow: 0 18px 42px rgba(50, 101, 246, .42) !important;
    }

    .stButton > button:not([kind="primary"]) {
        border: 1px solid rgba(124, 148, 234, .18) !important;
        border-radius: 13px !important;
        color: #aeb9de !important;
        background: rgba(30, 42, 82, .42) !important;
    }

    [data-testid="stSidebar"] {
        width: 330px !important;
        border-right: 1px solid rgba(129, 150, 231, .12);
        background:
            radial-gradient(circle at 10% 0%, rgba(68, 104, 213, .24), transparent 28%),
            rgba(8, 13, 29, .94);
    }

    [data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }

    .side-brand {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin-bottom: 2.6rem;
        color: #f5f7ff;
        font-family: "Manrope", sans-serif;
        font-weight: 600;
    }

    .side-icon {
        display: grid;
        place-items: center;
        width: 35px;
        height: 35px;
        border-radius: 11px;
        background: linear-gradient(145deg, #769aff, #3a6df3);
        box-shadow: 0 10px 28px rgba(62, 105, 238, .32);
    }

    .side-label {
        color: #63709a;
        font-size: .65rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: .2rem;
    }

    [data-testid="stSidebar"] h2 {
        color: #f7f9ff;
        font-family: "Manrope", sans-serif;
        font-size: 1.55rem;
        font-weight: 500;
        letter-spacing: -.035em;
    }

    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #98a3c8; }
    [data-testid="stNumberInput"] input { color: #f5f7ff; background: rgba(28, 39, 76, .7); }

    [data-testid="stNumberInput"] > div,
    [data-testid="stNumberInput"] div[data-baseweb="input"] {
        border-color: rgba(124, 148, 234, .16) !important;
        border-radius: 12px !important;
        background: rgba(28, 39, 76, .7) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: #6e94ff;
        box-shadow: 0 0 18px rgba(72, 114, 255, .6);
    }

    [data-testid="stAlert"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        background: rgba(21, 31, 63, .88);
    }

    [data-testid="stProgress"] > div > div { background: linear-gradient(90deg, #3d72f4, #7a9dff); }
    hr { border-color: rgba(130, 150, 224, .1) !important; }

    .tiny-note { margin-top: .8rem; color: #596587; font-size: .7rem; text-align: center; }

    @media (max-width: 900px) {
        .block-container { padding: 1.2rem 1rem 3rem; }
        .topbar { padding-bottom: 2rem; }
        .top-status { display: none; }
        .hero h1 { font-size: 3.2rem; }
        .metric-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


def clear_all():
    st.session_state["uploader_key"] += 1
    st.rerun()


with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <span class="side-icon">◈</span>
            <span>SKU Resizer</span>
        </div>
        <div class="side-label">Workspace</div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Output settings")
    target_w = st.number_input("Width", min_value=1, value=500, step=10, help="Final width in pixels")
    target_h = st.number_input("Height", min_value=1, value=375, step=10, help="Final height in pixels")
    quality = st.slider("JPG quality", 10, 100, 90)

    st.markdown("---")
    st.caption("Images are centered automatically. PNG and WEBP transparency is preserved.")
    if st.button("Clear workspace", use_container_width=True):
        clear_all()
    st.markdown('<div class="tiny-note">VERSION 2.0 · IMAGE OPERATIONS</div>', unsafe_allow_html=True)


st.markdown(
    """
    <div class="topbar">
        <div class="brand"><span class="brand-mark">◈</span> SKU Resizer</div>
        <div class="top-status"><span class="status-dot"></span> System ready</div>
    </div>
    <section class="hero">
        <div class="eyebrow">Image operations</div>
        <h1>Every SKU.<br><span>Perfectly framed.</span></h1>
        <p>Resize, center and package product imagery in one clean workflow. Built for fast, consistent e-commerce uploads.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


upload_col, info_col = st.columns([1.7, 1], gap="large")

with upload_col:
    st.markdown(
        """
        <div class="section-kicker">01 · Input</div>
        <div class="section-title">Drop your product images</div>
        <div class="section-copy">PNG, JPG, JPEG or WEBP · Multiple files supported</div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Upload product images",
        accept_multiple_files=True,
        type=["png", "jpg", "jpeg", "webp"],
        key=f"uploader_{st.session_state['uploader_key']}",
    )

    button_label = (
        f"Process {len(uploaded_files)} image{'s' if len(uploaded_files) != 1 else ''}"
        if uploaded_files
        else "Process images"
    )
    process_clicked = st.button(button_label, use_container_width=True, type="primary")

with info_col:
    st.markdown(
        f"""
        <div class="section-kicker">02 · Live profile</div>
        <div class="section-title">Output overview</div>
        <div class="section-copy">Your current export configuration</div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Canvas size</div>
                <div class="metric-value">{target_w} <small>×</small> {target_h}</div>
                <div class="metric-foot">PX · CENTERED FIT</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">JPG quality</div>
                <div class="metric-value">{quality}<small>%</small></div>
                <div class="quality-bars">
                    <i style="height:13px"></i><i style="height:19px"></i>
                    <i style="height:27px"></i><i style="height:21px"></i>
                    <i style="height:34px"></i><i style="height:29px"></i>
                    <i style="height:38px"></i><i style="height:32px"></i>
                </div>
            </div>
        </div>
        <div class="workflow-card">
            <div class="workflow-step"><span class="step-number">01</span> Upload your source images</div>
            <div class="workflow-step"><span class="step-number">02</span> Automatic resize + center</div>
            <div class="workflow-step"><span class="step-number">03</span> Download one clean ZIP</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if process_clicked:
    if not uploaded_files:
        st.warning("Add at least one image to start processing.")
    else:
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for index, file in enumerate(uploaded_files):
                    status_text.caption(f"Processing {file.name}")
                    image = Image.open(file)
                    original_format = image.format

                    if image.mode in ("RGBA", "LA") or original_format in ("PNG", "WEBP"):
                        mode = "RGBA"
                        background_color = (0, 0, 0, 0)
                    else:
                        mode = "RGB"
                        background_color = (255, 255, 255)

                    image = image.convert(mode)
                    width, height = image.size
                    scale = min(target_w / width, target_h / height)
                    new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
                    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

                    final_image = Image.new(mode, (target_w, target_h), background_color)
                    offset = ((target_w - new_size[0]) // 2, (target_h - new_size[1]) // 2)
                    mask = resized_image if mode == "RGBA" else None
                    final_image.paste(resized_image, offset, mask)

                    image_buffer = io.BytesIO()
                    if mode == "RGBA":
                        final_image.save(image_buffer, "PNG", optimize=True)
                        extension = ".png"
                    else:
                        final_image.save(image_buffer, "JPEG", quality=quality, optimize=True)
                        extension = ".jpg"

                    clean_name = os.path.splitext(file.name)[0] + extension
                    zip_file.writestr(clean_name, image_buffer.getvalue())
                    progress_bar.progress((index + 1) / len(uploaded_files))

            status_text.empty()
            st.success(f"{len(uploaded_files)} images are ready to download.")
            st.download_button(
                label="Download processed images (.ZIP)",
                data=zip_buffer.getvalue(),
                file_name="sku_images_ready.zip",
                mime="application/zip",
                use_container_width=True,
            )
        except Exception as error:
            status_text.empty()
            st.error(f"Something went wrong while processing the images: {error}")
