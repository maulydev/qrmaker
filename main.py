import streamlit as app
from streamlit_option_menu import option_menu
import controllers as cont


get_qr_status: bool = True
download_status: bool = True
qrcodeimage: str = \
    app.session_state['qrcodename'] if 'qrcodename' in app.session_state else ''
color_setting: dict = {}

theme_color = ('White', 'Black', 'Blue', 'Orange', 'Red')

with app.sidebar:
    app.header = "Quickres"
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
    url = app.text_input(
        'Webiste',
        placeholder='Enter your website url',
        label_visibility='hidden',
    )

    col1, col2 = app.columns(2)

    with col2:
        # checking to disable or enable button based on url input
        get_qr_status = False if url != "" else True

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
            if url:
                if logo:
                    qrcodeimage = cont.makeqrcode(
                        url, output_format, color_setting, logo
                    )[1]
                else:
                    qrcodeimage = cont.makeqrcode(
                        url, output_format, color_setting
                    )[1]

                download_status = False if url != "" else True
                app.session_state["qrcodename"] = qrcodeimage
            else:
                app.warning("Enter url to continue")

        # qr code image downloader button
            # with open(qrcodeimage, "rb") as file:
            #     download = \
            #         app.download_button(
            #             'Download',
            #             disabled=download_status,
            #             use_container_width=True,
            #             data=file,
            #             file_name=f"qrcode.{qrcodeimage.split('.')[1]}",
            #             mime=f"image/{qrcodeimage.split('.')[1]}",
            #             on_click=lambda: os.remove(qrcodeimage)
            #         )
            download = \
                app.download_button(
                    'Download',
                    disabled=download_status,
                    use_container_width=True,
                    data=qrcodeimage,
                    file_name=f"qrcode.{output_format}",
                    mime=f"image/{output_format}",
                )

    with col1:
        if qrcodeimage != "":
            app.image(cont.set_output(qrcodeimage))
        else:
            app.image(cont.set_output())