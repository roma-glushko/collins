
from pydantic import BaseModel


class RawDocument(BaseModel):
    title: str
    text: str


SAMPLE_DOCUMENTS: tuple[RawDocument, ...] = (
    RawDocument(
        title="About Australia 🇦🇺",
        text="Australia, officially the Commonwealth of Australia, "
             "is a sovereign country comprising the mainland of the Australian continent, "
             "the island of Tasmania, and numerous smaller islands. "
             "With an area of 7,617,930 square kilometres (2,941,300 sq mi), "
             "Australia is the largest country by area in Oceania and the world's sixth-largest country. "
             "Australia is the oldest, flattest, and driest inhabited continent, with the least fertile soils. "
             "It is a megadiverse country, and its size gives it a wide variety of landscapes and climates, "
             "with deserts in the centre, "
             "tropical rainforests in the north-east, and mountain ranges in the south-east."
    ),
    RawDocument(
        title="About Japan 🇯🇵",
        text="Japan is an island country in East Asia. "
             "It is situated in the northwest Pacific Ocean, and is bordered on the west by the Sea of Japan, "
             "while extending from the Sea of Okhotsk in the north toward the East China Sea and Taiwan in the south. "
             "Japan is a part of the Ring of Fire, and spans an archipelago of 6852 islands covering "
             "377,975 square kilometers (145,937 sq mi); the five main islands are "
             "Hokkaido, Honshu (the \"mainland\"), Shikoku, Kyushu, and Okinawa. "
             "Tokyo is the nation's capital and largest city; "
             "other major cities include Yokohama, Osaka, Nagoya, Sapporo, Fukuoka, Kobe, and Kyoto."
    ),
    RawDocument(
        title="About Ukraine 🇺🇦",
        text="Ukraine is a country in Eastern Europe. "
             "It is the second largest country in Europe after Russia, "
             "which borders it to the east and north-east. "
             "Ukraine also shares borders with Belarus to the north; "
             "Poland, Slovakia, and Hungary to the west; "
             "Romania and Moldova to the south; and has a coastline along the Sea of Azov and the Black Sea. "
             "It covers about 600,000 km2 (230,000 sq mi), with a population of about 40 million."
             " The nation's capital and largest city is Kyiv. "
             "The official and national language is Ukrainian, and most people are also fluent in Russian."
    ),
)

__all__ = ("SAMPLE_DOCUMENTS", "RawDocument", )
