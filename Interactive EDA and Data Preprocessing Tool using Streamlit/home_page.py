
import streamlit as st
import base64

def set_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def show_home_page():

        # Set background image
        set_bg_from_local("assets/bg6.jpg")  # <-- Update this to match your image path

        # Key Features Section
        st.header("Key Highlights")
        st.markdown("""
        🔍 **Interactive Data Insights:** Dive deeper into your datasets with interactive and dynamic visualizations. 
 
        📊 **Engaging Visuals:** Create visually appealing and informative charts to effectively represent your data.  

        ⚙️ **Simplified Data Processing:** Easily clean, preprocess, and transform your data with minimal effort.  
        """)

        # Description Section
        st.header("Get Started")
        st.markdown("""
        Our app offers an intuitive and seamless experience for analyzing and preparing your datasets. Whether you're a beginner or an expert, the process is simplified to maximize your efficiency.
        """)

        # Creating a container for the roles
# Inject custom CSS to style the boxes
        st.markdown(
            """
            <style>
            .box {
                background-color: #F0F0F0;  /* Sky Blue color */
                padding: 20px;  /* Add padding to make it look spacious */
                border-radius: 10px;  /* Rounded corners for the boxes */
                height: 250px;  /* Set a fixed height for consistency */
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            .column {
                margin-bottom: 20px;  /* Space between rows */
            }

            h3 {
                font-size: 1.5rem;
                margin-top: 10px;
            }

            p {
                font-size: 1rem;
                color: #333;
            }
            </style>
            """, unsafe_allow_html=True
        )

        # Creating the main container for the roles
        with st.container():
            

            # Create 2 rows and 2 columns
            col1, col2 = st.columns(2)

            col3, col4 = st.columns(2)

            # First Row
            with col1:
                st.markdown('<div class="box"><h3>📊</h3><h4>Data Analysts</h4><p>Discover patterns and trends effortlessly with automated data exploration tools.</p></div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="box"><h3>🔬</h3><h4>Data Scientists</h4><p>Focus on deeper insights and model-building by streamlining your exploratory analysis process.</p></div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)  # Add a line break between rows

            # Second Row
            with col3:
                st.markdown('<div class="box"><h3>💼</h3><h4>Business Professionals</h4><p>Make data-driven decisions faster with easy-to-interpret visualizations.</p></div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)  # Add a line break between rows
            with col4:
                st.markdown('<div class="box"><h3>📚</h3><h4>Educators & Students</h4><p>Learn and teach data science with a simplified approach to data exploration.</p></div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)  # Add a line break between rows
    # Example Dataset
        st.subheader("Try it Out!")
        st.write('''Simply upload your dataset, or use our example data from the sidebar. Choose a dataset, and let the app take care of the rest!

            ''')


    # Final Message
        st.write('<div class="thank-you">Start making data-driven decisions with ease!  </div>', unsafe_allow_html=True)

    # Add Custom CSS
st.write('<style>'
            '.target-audience {display: flex; justify-content: space-between; flex-wrap: wrap;}'
            '.audience {flex: 0 1 calc(50% - 10px); background-color: #f6f6f6; border-radius: 10px; margin: 5px; padding: 10px; text-align: center;}'
            '.audience-icon {font-size: 2em;}'
            '.start-button {display: inline-block; margin-top: 20px; background-color: #1E90FF; color: #FFF; padding: 10px 20px; text-align: center; border-radius: 5px; text-decoration: none;}'
            '.thank-you {font-size: 1.5em; margin-top: 20px; text-align: center; color: #555;}'
            '</style>', unsafe_allow_html=True)


def custom_css():
    # Define custom CSS styles
    custom_css = """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Lora', serif; /* Elegant, stylish font */
                 /* Slightly italicized text */
        margin: 0;
        padding: 0;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        padding: 40px;
    }

    .header {
        font-size: 48px;
        font-weight: bold;
        color: #333;
        margin-bottom: 16px;
    }

    .tagline {
        font-size: 24px;
        color: #666;
        margin-bottom: 32px;
    }

    .features {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-bottom: 40px;
    }

    .feature {
        flex: 1;
        text-align: center;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 8px;
        transition: transform 0.3s ease-in-out;
    }

    .feature:hover {
        transform: scale(1.05);
    }

    .feature-icon {
        font-size: 36px;
        color: #4CAF50;
    }

    .feature-title {
        font-size: 18px;
        font-weight: bold;
        margin-top: 16px;
    }

    .action-button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 16px 32px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .action-button:hover {
        background-color: #45a049;
    }

    </style>
    """

    return custom_css