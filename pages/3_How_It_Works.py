import pandas as pd
import streamlit as st

from webapp import story, ui

ui.setup("How It Works")
engine = ui.load_engine()
cfg = engine.cfg
stages = cfg.matching.stages

st.title("How it works")
st.write(
    "This page is for readers who want the technical detail. You do not need any of it to use the app."
)

st.header("The idea")
st.write(
    "Every manufacturer names spreadsheet columns differently. The app reads a file, decides which "
    "standard product field each column most likely holds, and lets a person confirm the result. "
    "Confirmed choices become a reusable template. A confirmed file can then be turned into a "
    "digital product passport: a structured, checked record with its own identifier."
)

st.header("The matching steps")
st.write(
    "Each column is tried against four steps, in order, and the first step that is confident enough "
    "decides. Later steps only run if earlier ones found nothing."
)
steps = pd.DataFrame(
    [
        {"Step": "1. Known names", "What it does": "Looks the column name up in a list of known synonyms (for example 'colour', 'shade').", "Setting": "Exact match"},
        {"Step": "2. Similar spelling", "What it does": "Compares the name to the standard field names, tolerating typos and abbreviations (fuzzy string matching).", "Setting": f"Score of at least {stages.fuzzy.threshold:g} out of 100"},
        {"Step": "3. Similar meaning", "What it does": "Compares the meaning of the name using a small language model (sentence embeddings).", "Setting": (f"Similarity of at least {stages.semantic.threshold:g}" if engine.semantic_on else "Switched off in this version")},
        {"Step": "4. Look at the values", "What it does": "Checks what the values look like (country codes, barcodes, customs codes) when the name tells us nothing.", "Setting": f"Score of at least {stages.value.threshold:g} out of 100"},
    ]
)
st.dataframe(steps, hide_index=True, **ui.stretch())
st.write(
    "If two columns compete for the same field, the one with stronger evidence wins and the other "
    "is flagged for review."
)

st.header("How sure is 'How sure'?")
st.write(
    "A raw similarity score is not a probability. For each step, the app learned from example files "
    "how often its answers were right at each score (a logistic calibration), and reports that "
    "as a percentage. Anything below "
    f"{cfg.confidence.bands.review:.0%} is marked for a person to check."
    if cfg.confidence.bands.review is not None
    else "Confidence values are learned from example files with known answers."
)

st.header("From columns to a passport")
st.markdown(
    "- **Standard fields.** Matches point at a fixed list of "
    f"{len(engine.field_names)} product fields, each defined in a JSON Schema.\n"
    "- **Product ID.** Each passport gets an identifier built from the company, the product family, "
    "and optionally its colour and size.\n"
    "- **Checks.** The record is validated against the schema and against lists of allowed values, "
    "and the share of required fields that are filled is reported.\n"
    "- **Output.** The passport is written as JSON-LD, a standard format for linked data."
)

st.header("Saved templates")
st.write(
    "A template stores only column names and the field each was matched to. Applying it to a new file "
    "reuses those choices for columns it recognises and sends new or renamed columns back through the "
    "matching steps. Templates are kept in a small SQLite database file."
)

st.header("The product ID (ADID)")
st.write(
    "A barcode (GTIN) identifies one colour and size of a product. A passport often has to talk about the "
    "whole design too, and a design has no barcode of its own. ADID supplies that missing level."
)
st.dataframe(
    pd.DataFrame(
        [
            {"Level": "Design (family)", "Meaning": "The style, whatever the colour or size", "Example": "/adid/ts-1000"},
            {"Level": "Variant", "Meaning": "One colour and size of the design", "Example": "/adid/ts-1000/navy_m"},
            {"Level": "Single item", "Meaning": "One physical unit of a variant (barcode plus serial number)", "Example": "/adid/ts-1000/navy_m/sn-1"},
        ]
    ),
    hide_index=True,
    **ui.stretch(),
)
st.markdown(
    "- **Identity is kept apart from data.** Only what identifies an item goes into the ID. A correction to fibre content or "
    "origin changes the record, never the ID, so printed labels and QR codes stay valid.\n"
    "- **One format for three levels.** The path gets longer as you go down: design, then colour and size, then serial number.\n"
    "- **It works with GS1, not against it.** The variant level lines up with the barcode. ADID is a research design from this "
    "project, not an official standard, and its conformance statement says so: it makes no claim to GS1 Digital Link "
    "compliance and no claim to any standard's identifier scheme.\n"
    "- **Resolvable by design.** The ID is meant to be a web address that returns the record. In this demonstration the "
    "addresses are examples and do not open live pages."
)

st.header("Technologies")
st.dataframe(
    pd.DataFrame(
        [
            {"Part": "Interface", "Technology": "Streamlit"},
            {"Part": "Reading files", "Technology": "Python and pandas (CSV, Excel, flat JSON)"},
            {"Part": "Similar spelling", "Technology": "RapidFuzz"},
            {"Part": "Similar meaning", "Technology": "Sentence-Transformers, model all-MiniLM-L6-v2"},
            {"Part": "Checking records", "Technology": "JSON Schema (jsonschema) and JSON-LD"},
            {"Part": "Saved templates", "Technology": "SQLite"},
            {"Part": "Settings", "Technology": "One YAML configuration file, fixed before testing"},
        ]
    ),
    hide_index=True,
    **ui.stretch(),
)

st.header("This installation")
st.dataframe(
    pd.DataFrame(
        [
            {"Item": "Standard fields", "Value": str(len(engine.field_names))},
            {"Item": "Meaning-based matching", "Value": "On" if engine.semantic_on else "Off"},
            {"Item": "Confidence available", "Value": "Yes" if engine.calibrator is not None else "No"},
            {"Item": "Settings file", "Value": str(cfg.source_path) if getattr(cfg, "source_path", None) else "config/default.yaml"},
        ]
    ),
    hide_index=True,
    **ui.stretch(),
)

st.header("The development story")
st.write("How the project was built, what went wrong, how it was tested and what it found.")
if st.button("Read the full development story" if not st.session_state.get("show_story") else "Hide the development story"):
    st.session_state["show_story"] = not st.session_state.get("show_story", False)
    st.rerun()
if st.session_state.get("show_story"):
    story.render()

st.header("Limits")
st.markdown(
    "- It is a research prototype, not a certified compliance tool.\n"
    "- It suggests matches; a person must confirm them.\n"
    "- A column that holds several things at once (for example colour and size together) is not split.\n"
    "- Results depend on the file: columns with clear names or recognisable values match best."
)
ui.footer()