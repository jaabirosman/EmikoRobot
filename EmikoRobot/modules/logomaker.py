@register(pattern="^/wlogo ?(.*)")
async def logo_(event):
    xx = await event.reply("Preparing your logo...")
    name = event.pattern_match.group(1)
    if not name:
        await xx.edit("Provide some text to draw!\nExample: /wlogo <your name>!")
        return
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in ubot2.iter_messages(
            "@osmanilogo", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob.glob("./EmikoRobot/resources/fonts/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in ubot2.iter_messages(
            "@osmanilogo", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("./EmikoRobot/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 105
        strke = 8
    elif len(name) >= 9:
        fnt_size = 50
        strke = 4
    else:
        fnt_size = 95
        strke = 13
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text((x, y), name, font=font, fill="white",
              stroke_width=strke, stroke_fill="black")
    flnme = f"logo.png"
    img.save(flnme, "png")
    await xx.edit("Uploading")
    if os.path.exists(flnme):
        await tbot.send_file(
            event.chat_id,
            file=flnme,
            caption="Logo Designed by [Osmani Logo Maker](https://t.me/osmanilogo)",
            force_document=False,
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_) 
    if os.path.exists(font_):
        if not font_.startswith("./EmikoRobot/resources/fonts"):
            os.remove(font_)


mod_name = "Logomaker"

help = """ This is help menu for logomaker

❂ /logo <text/name> - Create a logo with random view.
❂ /wlogo <text/name> - Create a logo with wide view only.

 Image Editor By @osmanilogo :

❂  /edit <reply photo> - to edit image.
"""
