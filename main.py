import streamlit as app
from streamlit_option_menu import option_menu
import controllers as cont
import validators

app.write("---")

ph = """Phone: 0201112234\nText: Some text here""".strip()
get_qr_status: bool = True
download_status: bool = True
qrcodeimage: str = \
    app.session_state['qrcodename'] if 'qrcodename' in app.session_state else ''
color_setting: dict = {}
data: str = None
which_input: str = ""

theme_color = ('White', 'Black', 'Blue', 'Orange', 'Red')

with app.sidebar:
    app.subheader("QR Maker")
    app.write("---")
    bg_color = app.selectbox(
        'Background Color', theme_color, index=0)

    fill_color = app.selectbox(
        'Foreground Color', theme_color, index=1)

    logo = app.file_uploader(
        'Add logo to QR Code', ['jpg', 'png'], accept_multiple_files=False)

nav = option_menu(
    "", ["URL", 'TEXT', 'FILE'],
    icons=['globe', 'chat', 'file'],
    default_index=0,
    orientation="horizontal"
)

if nav == "URL":
    which_input = "url"
    data = app.text_input(
        'Webiste',
        placeholder='Enter your website data',
        label_visibility='hidden',
        key="url",
    )


if nav == "TEXT":
    which_input = "text"
    data = app.text_area('Text', placeholder=ph,
                         label_visibility="collapsed", key="text")


if nav == "FILE":
    which_input = "file"
    file = app.file_uploader("Upload a file to create a qr code", key="file")

col1, col2 = app.columns(2)

with col2:
    # checking to disable or enable button based on data input
    get_qr_status = False if data != "" else True

    # setting color for qr code
    color_setting["fillcolor"] = fill_color
    color_setting["background"] = bg_color

    # output image format
    output_format = option_menu(
        "", ("JPG", 'PNG'),
        default_index=0,
        key="format",
        orientation="horizontal"
    )

    # qr code generator button
    get_qrcode = \
        app.button('Generate QR Code', disabled=get_qr_status,
                   use_container_width=True)

    # button click event handler
    if get_qrcode:
        if (which_input == "url" and validators.url(data) == True) or which_input == "text":
            if data:
                if logo:
                    qrcodeimage = cont.makeqrcode(
                        data, output_format, color_setting, logo
                    )[1]
                else:
                    qrcodeimage = cont.makeqrcode(
                        data, output_format, color_setting
                    )[1]

                download_status = False if data != "" else True
                app.session_state["qrcodename"] = qrcodeimage
        else:
            app.warning("Enter a valid data to continue")

    download = \
        app.download_button(
            'Download',
            disabled=download_status,
            use_container_width=True,
            data=qrcodeimage,
            file_name=f"qrcode.{output_format.lower()}",
            mime=f"image/{output_format.lower()}",
        )

with col1:
    # check qrcode image generated and ouput to the page
    if qrcodeimage != "":
        app.image(cont.set_output(qrcodeimage))
    else:
        app.image(cont.set_output())
