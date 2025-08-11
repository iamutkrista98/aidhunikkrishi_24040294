import streamlit as st
import os
import bcrypt
import requests
import json
import pandas as pd
import datetime

def import_data_from_api(update_session):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    st.subheader("🔗 Import Data from API Endpoints")
    
    # Instruction section
    with st.expander("📘 How to Use This Importer", expanded=True):
        st.markdown("""
        **Import data from any public API endpoint (JSON/CSV) in 3 simple steps:**

        1. **Provide Input**  
           → Enter the valid API endpoint URL   
           → Name your dataset (e.g., `crime_data_2024`)

        2. **Configure Settings**  
           → Select file type (Auto-detected by default)  
           → Adjust CSV parameters if needed

        3. **Process & Save**  
           → Click 'Process Data' to validate and convert  
           → Download or use dataset in analytics modules

        **Supported Formats:**  
        ✅ JSON (nested structures supported)  
        ✅ CSV (any delimiter, automatic encoding detection)  
        
        **Example Endpoints:**  
        ```
        https://raw.githubusercontent.com/iamutkrista98/pentasynergeticsproj/main/csvjson.json
        ```
        """)

    # Configuration columns
    col1, col2 = st.columns([3, 1])
    with col1:
        api_url = st.text_input(
            "Dataset Endpoint URL",
            value="https://raw.githubusercontent.com/iamutkrista98/pentasynergeticsproj/main/csvjson.json",
            help="Supports HTTP/HTTPS endpoints with public access"
        )
    with col2:
        file_type = st.selectbox(
            "File Type",
            ["Auto Detect", "JSON", "CSV"],
            help="Force specific format if auto-detection fails"
        )

    dataset_name = st.text_input(
        "Dataset Name",
        placeholder="crime_data_2024",
        help="Will be saved as [name].csv in project datasets"
    )

    # CSV configuration expander
    with st.expander("Advanced CSV Settings", expanded=False):
        csv_col1, csv_col2 = st.columns(2)
        with csv_col1:
            delimiter = st.text_input("Delimiter", ",", max_chars=2)
            encoding = st.selectbox("Encoding", ["utf-8", "latin-1", "iso-8859-1"])
        with csv_col2:
            decimal = st.text_input("Decimal", ".", max_chars=1)
            thousands = st.text_input("Thousands Separator", "", max_chars=1)

    if st.button("🚀 Process Data", use_container_width=True):
        if not api_url or not dataset_name:
            st.warning("Please provide both URL and dataset name")
            return

        try:
            # File type detection logic
            if file_type == "Auto Detect":
                if api_url.lower().endswith('.json'):
                    file_type = "JSON"
                elif api_url.lower().endswith('.csv'):
                    file_type = "CSV"
                else:
                    content_type = requests.head(api_url).headers.get('Content-Type', '')
                    if 'json' in content_type:
                        file_type = "JSON"
                    elif 'csv' in content_type or 'text/plain' in content_type:
                        file_type = "CSV"

            # Data processing workflow
            with st.spinner(f"🔍 Connecting to {api_url}"):
                response = requests.get(api_url)
                response.raise_for_status()

                if file_type == "JSON":
                    # JSON processing with enhanced error handling
                    try:
                        json_data = response.json()
                        st.success("✅ Valid JSON structure detected")
                        
                        # Flatten nested JSON
                        def flatten_json(nested_json, parent_key='', sep='_'):
                            items = {}
                            for k, v in nested_json.items():
                                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                                if isinstance(v, dict):
                                    items.update(flatten_json(v, new_key, sep))
                                elif isinstance(v, list):
                                    for i, item in enumerate(v):
                                        items.update(flatten_json({f"{k}_{i}": item}, new_key, sep))
                                else:
                                    items[new_key] = v
                            return items

                        if isinstance(json_data, list):
                            df = pd.DataFrame([flatten_json(item) for item in json_data])
                        elif isinstance(json_data, dict):
                            df = pd.DataFrame([flatten_json(json_data)])
                        else:
                            raise ValueError("Unsupported JSON structure")

                    except json.JSONDecodeError:
                        st.error("Failed to parse JSON - Invalid structure")
                        raise

                elif file_type == "CSV":
                    # CSV processing with encoding fallback
                    try:
                        df = pd.read_csv(
                            io.StringIO(response.text),
                            sep=delimiter,
                            decimal=decimal,
                            thousands=thousands,
                            encoding=encoding
                        )
                    except UnicodeDecodeError:
                        st.warning("Retrying with fallback encoding...")
                        df = pd.read_csv(
                            io.StringIO(response.text),
                            sep=delimiter,
                            decimal=decimal,
                            thousands=thousands,
                            encoding='latin-1'
                        )

                st.success(f"📦 Loaded {len(df)} records with {len(df.columns)} columns")

            # File saving section
            dataset_dir = os.path.join(root_dir, 'Component_datasets')
            os.makedirs(dataset_dir, exist_ok=True)
            csv_path = os.path.join(dataset_dir, f"{dataset_name}.csv")
            
            with st.spinner(f"💾 Saving to {csv_path}"):
                df.to_csv(csv_path, index=False, encoding='utf-8')

            # Results display
            st.success(f"✅ Dataset saved successfully")
            
            tab1, tab2, tab3 = st.tabs(["Preview", "Statistics", "Download"])
            
            with tab1:
                st.dataframe(df.head(10), use_container_width=True)

            with tab2:
                st.markdown("**Dataset Summary**")
                st.json({
                    "Total Records": len(df),
                    "Columns": list(df.columns),
                    "File Size": f"{os.path.getsize(csv_path)/1024:.1f} KB",
                    "Created At": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            with tab3:
                st.download_button(
                    label="⬇️ Download CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{dataset_name}.csv",
                    mime='text/csv',
                    use_container_width=True
                )

        except requests.exceptions.RequestException as e:
            st.error(f"🔌 Connection Error: {str(e)}")
        except pd.errors.ParserError as e:
            st.error(f"📊 Parsing Error: Check delimiter/encoding settings")
        except Exception as e:
            st.error(f"❌ Processing Failed: {str(e)}")
            with st.expander("Technical Details"):
                st.write(response.text[:500])
                st.write(f"Headers: {response.headers}")