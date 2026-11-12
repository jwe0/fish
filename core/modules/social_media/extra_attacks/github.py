from bs4 import BeautifulSoup

def github(url, session):
    extra = {}
    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    extra_info = {
        "fullname" : soup.find("span", class_="p-name vcard-fullname d-block overflow-hidden"),
        "username" : soup.find("span", class_="p-nickname vcard-username d-block"),
    }
    details  = soup.find("ul", class_="vcard-details")

    for info in extra_info:
        detail_info = extra_info[info]

        if detail_info:
            extra[info] = detail_info.text.strip()
    if details:
        for li in details.find_all("li"):
            prop = li.get("itemprop").strip()
            data = li.find("span", class_="p-label")

            if not data:
                data = li.find("a")

            data = data.text.strip().replace("\n", "\\n")

            extra[prop] = data
    return extra