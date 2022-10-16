import streamlit as st
from util.Illuminator import Illuminator
from PIL import Image
import os


def save_image(image_file):
    img = Image.open(image_file)
    img = img.save("util/input/in.png")

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>DARK PART ILLUMINATOR</h1>", unsafe_allow_html=True)

im = Illuminator()
base_path = os.path.dirname(os.path.abspath(__file__))
in_path = os.path.join(base_path,"util/input/in.png")
out_path = os.path.join(base_path,"util/output/out.png")

st.write("""
# Try Uploading an Image!
""")

footer="""<style>
a:link , a:visited{
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
color: gray;
text-align: center;
}
</style>
<div class="footer">
<p>Based on <i>M. Akai et. al. "A Single Backlit Image Enhancement Method For Improvement Of Visibility Of Dark Part"</i></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

image_file = st.file_uploader("Choose a file")

if image_file is not None:
   # print(image_file)
    
    try:
        save_image(image_file)
        out = im.illuminate(in_path)
        images = [in_path, out_path]
        # st.image(images, use_column_width=True, caption=["some generic text"] * len(images))

        n_rows = 1
        n_cols = 2
        captions = ["Original Image", "Illuminated Image"]
        rows = [st.columns(n_cols) for _ in range(n_rows)]
        cols = [column for row in rows for column in row]

        for col, img, caption in zip(cols, images, captions):
            col.image(img, caption = caption, width=700)

    except Exception as e:
        st.write("""
        # That isn't supposed to go there!
        """)
        raise(e)


