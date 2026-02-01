def format_anime_post(anime):
    title = anime["title"]["romaji"]
    year = anime["startDate"]["year"]
    desc = anime["description"] or "Sem descrição."
    desc = desc.replace("<br>", "").replace("</br>", "")[:700]

    text = (
        f"🎬 *Anime*\n\n"
        f"📌 *Título:* {title}\n"
        f"📅 *Ano:* {year}\n\n"
        f"📖 *Sinopse:*\n{desc}\n\n"
        f"#anime #otaku"
    )
    return text, anime["coverImage"]["large"]
