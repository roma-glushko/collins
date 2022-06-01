from typing import Final

from livearea.services.documents import Document

DOCUMENT_MAP: Final[dict[int, Document]] = {
    0: Document(
        id=0,
        title="About Australia 🇦🇺",
        body="Australia, officially the Commonwealth of Australia, "
             "is a sovereign country comprising the mainland of the Australian continent, "
             "the island of Tasmania, and numerous smaller islands. "
             "With an area of 7,617,930 square kilometres (2,941,300 sq mi), "
             "Australia is the largest country by area in Oceania and the world's sixth-largest country. "
             "Australia is the oldest,[15] flattest,[16] and driest inhabited continent, with the least fertile soils. "
             "It is a megadiverse country, and its size gives it a wide variety of landscapes and climates, "
             "with deserts in the centre, "
             "tropical rainforests in the north-east, and mountain ranges in the south-east."
    ),
    1: Document(
        id=1,
        title="About Japan 🇯🇵",
        body="Japan is an island country in East Asia. "
             "It is situated in the northwest Pacific Ocean, and is bordered on the west by the Sea of Japan, "
             "while extending from the Sea of Okhotsk in the north toward the East China Sea and Taiwan in the south. "
             "Japan is a part of the Ring of Fire, and spans an archipelago of 6852 islands covering "
             "377,975 square kilometers (145,937 sq mi); the five main islands are "
             "Hokkaido, Honshu (the \"mainland\"), Shikoku, Kyushu, and Okinawa. "
             "Tokyo is the nation's capital and largest city; "
             "other major cities include Yokohama, Osaka, Nagoya, Sapporo, Fukuoka, Kobe, and Kyoto."
    ),
    2: Document(
        id=2,
        title="About Ukraine 🇺🇦",
        body="Ukraine is a country in Eastern Europe. "
             "It is the second largest country in Europe after Russia, "
             "which borders it to the east and north-east. "
             "Ukraine also shares borders with Belarus to the north; "
             "Poland, Slovakia, and Hungary to the west; "
             "Romania and Moldova to the south; and has a coastline along the Sea of Azov and the Black Sea. "
             "It covers about 600,000 km2 (230,000 sq mi), with a population of about 40 million."
             " The nation's capital and largest city is Kyiv. "
             "The official and national language is Ukrainian, and most people are also fluent in Russian."
    ),
}

__all__ = ("DOCUMENT_MAP", )
