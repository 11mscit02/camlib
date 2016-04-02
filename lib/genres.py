# Copied from http://cambridgeshire.libraryebooks.co.uk/site/EB/ebooks/genre.asp
# It's not safe to scrape it every time, since the genre indicies MUST be immutable.

GENRE_TREE = [
    {"section": "Biography & True Stories",
     "genres": ["Biography & True Stories",
                "Biography: general",
                "Diaries, letters & journals",
                "Memoirs",
                "True stories",
                ]},

    {"section": "Children's, young adult & educational",
     "genres": ["Children's & young adult fiction & true stories",
                "Children's & young adult poetry, anthologies, annuals",
                "Children's & young adult: general non-fiction",
                "Children's, young adult & educational",
                "Educational material",
                "Personal & social issues",
                "Picture books, activity books & early learning material",
                ]},

    {"section": "Computing & information technology",
     "genres": ["Business applications",
                "Computer hardware",
                "Computer networking & communications",
                "Computer programming / software development",
                "Computing & information technology",
                "Computing: general",
                "Digital lifestyle",
                "Operating systems",
                ]},

    {"section": "Earth sciences, geography, environment, planning",
     "genres": ["Earth sciences",
                "Geography",
                "The environment",
                "Business & management",
                ]},

    {"section": "Economics, finance, business & management",
     "genres": ["Economics",
                "Economics, finance, business & management",
                "Finance & accounting",
                "Industry & industrial studies",
                ]},

    {"section": "English language teaching (ELT)",
     "genres": ["ELT: learning material & coursework",
                "English language teaching (ELT)",
                ]},

    {"section": "Fiction & related items",
     "genres": ["Adventure",
                "Classic fiction (pre c 1945)",
                "Crime & mystery",
                "Erotic fiction",
                "Fantasy",
                "Fiction & related items",
                "Fiction: special features",
                "Fiction-related items",
                "Graphic novels",
                "Historical fiction",
                "Horror & ghost stories",
                "Modern & contemporary fiction (post c 1945)",
                "Myth & legend told as fiction",
                "Religious & spiritual fiction",
                "Romance",
                "Sagas",
                "Science fiction",
                "Thriller / suspense",
                ]},

    {"section": "Health & personal development",
     "genres": ["Family & health",
                "Health & personal development",
                "Mind, Body, Spirit",
                "Self-help & personal development",
                ]},

    {"section": "Humanities",
     "genres": ["History",
                "Humanities",
                "Philosophy",
                "Religion & beliefs",
                ]},

    {"section": "Language",
     "genres": ["Language teaching & learning (other than ELT)",
                "Language: reference & general",
                "linguistics",
                ]},

    {"section": "Law",
     "genres": ["Jurisprudence & general issues",
                "Laws of Specific jurisdictions",
                ]},

    {"section": "Lifestyle, sport & leisure",
     "genres": ["Antiques & collectables",
                "Cookery / food & drink etc",
                "Gardening",
                "Handicrafts, decorative arts & crafts",
                "Hobbies, quizzes & games",
                "Home & house maintenance",
                "Humour",
                "Lifetyle & personal style guides",
                "Local interest, family history & nostalgia",
                "Sports & outdoor recreation",
                "The natural world, country life & pets",
                "Transport: general interest",
                "Travel & holiday",
                ]},

    {"section": "Literature & literary studies",
     "genres": ["Anthologies (non-poetry)",
                "Literature & literary studies",
                "Literature: history & criticism",
                "Plays, playscripts",
                "Poetry",
                "Prose: non-fiction",
                ]},

    {"section": "Mathematics & science",
     "genres": ["Astronomy, space & time",
                "Mathematics",
                "Physics",
                "Science: general issues",
                ]},

    {"section": "Medicine",
     "genres": ["Clinical & internal medicine",
                "Medicine: general issues",
                "Nursing & ancillary services",
                "Other branches of medicine",
                ]},

    {"section": "Reference, information & interdisciplinary subjects",
     "genres": ["Encyclopaedias & reference works",
                ]},

    {"section": "Society & social sciences",
     "genres": ["Education",
                "Politics & government",
                "Psychology",
                "Social services & welfare, criminology",
                "Society & culture: general",
                "Sociology & anthropology",
                "Warfare & defence",
                ]},

    {"section": "Technology, engineering, agriculture",
     "genres": ["Agriculture & farming",
                "Civil engineering, surveying & building",
                "Electronics & communications engineering",
                "Energy technology & engineering",
                "Other technologies & applied sciences",
                "Technology: general issues",
                ]},

    {"section": "The arts",
     "genres": ["Architecture",
                "Art forms",
                "Film, TV & radio",
                "Music",
                "Photography & photographs",
                "The arts: general issues",
                "Theatre studies",
                ]},

    {"section": "Unclassified",
     "genres": ["Unclassified",
                ]},
]

FULL_GENRE_LIST = [genre for section in GENRE_TREE for genre in section["genres"]]

def get_genre_tree(books):
    tree = []
    for section in GENRE_TREE:
        branch = {"section": section["section"],
                  "genres": []}
        for genre_name in section["genres"]:
            books_in_genre = [book for book in books if book["genre"] == genre_name]
            if books_in_genre:
                genre = {"name": genre_name,
                         "index": FULL_GENRE_LIST.index(genre_name),
                         "book_count": len(books_in_genre)}
                branch["genres"].append(genre)
        if branch["genres"]:
            tree.append(branch)
    return tree
