from pathlib import Path

import streamlit as st

from webapp import ui

ui.setup("Home")

st.markdown(
    """
    <div class="hero">
      <h1>Turn any product spreadsheet into a digital product passport</h1>
      <p>Upload the file you already have. The app works out what each column means,
      asks you to check its suggestions, and prepares a standard product record.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("How to get started")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="step">Step 1</div>', unsafe_allow_html=True)
    st.markdown("**Upload your file**  \nUse a spreadsheet exported from your own system (.csv, .xlsx or .json).")
with c2:
    st.markdown('<div class="step">Step 2</div>', unsafe_allow_html=True)
    st.markdown("**Check the suggestions**  \nThe app proposes what each column means. Change anything that looks wrong.")
with c3:
    st.markdown('<div class="step">Step 3</div>', unsafe_allow_html=True)
    st.markdown("**Save and create**  \nSave your choices as a template for next season, then create a product passport.")

st.write("")
st.subheader("Why the product ID matters")
st.write(
    "Every passport needs an ID that stays put. A barcode only identifies one colour and size, so a whole "
    "design has no ID of its own. The ADID gives every product one, at three levels."
)
d1, d2, d3 = st.columns(3)
for col, title, body, example in [
    (d1, "Design", "The style itself, whatever the colour or size.", "/adid/ts-1000"),
    (d2, "Variant", "One colour and size of the design.", "/adid/ts-1000/navy_m"),
    (d3, "Single item", "One physical unit, with its serial number.", "/adid/ts-1000/navy_m/sn-1"),
]:
    with col.container(border=True):
        st.markdown(f"**{title}**")
        st.write(body)
        st.code(example, language=None)
st.markdown(
    "- **It never changes by accident.** Fixing a typo in the fabric content updates the record, not the ID, "
    "so printed labels and QR codes stay valid.\n"
    "- **One simple pattern** for the design, the variant and the single item.\n"
    "- **It works alongside barcodes.** ADID is a research design from this project. It does not replace GS1 barcodes "
    "and is not an official standard. The example addresses here are illustrations and do not open live pages."
)

st.write("")
a, b, c = st.columns(3)
if a.button("Start with your file", type="primary"):
    st.switch_page("pages/1_Main_Tool.py")
if b.button("Open my saved templates"):
    st.switch_page("pages/2_Saved_Templates.py")
sample = Path("demo/demo_knitwear_export_spring.csv")
if sample.is_file():
    c.download_button(
        "Download a sample file to try",
        data=sample.read_bytes(),
        file_name=sample.name,
        mime="text/csv",
    )

st.write("")
st.info(
    "Your data stays in this session. Only column names and your choices are kept when you save a template. "
    "Want to know how it works? See the How It Works page."
)
ui.footer()