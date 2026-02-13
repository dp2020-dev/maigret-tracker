import sqlite3

def setup_db():
    conn = sqlite3.connect('maigret.db')
    cursor = conn.cursor()

    # Drop table if exists to start fresh
    cursor.execute('DROP TABLE IF EXISTS books')
    
    # Create the slimmed-down table
    cursor.execute('''
        CREATE TABLE books (
            title TEXT,
            alt_titles TEXT,
            original_title TEXT,
            pub_year INTEGER,
            read_status BOOLEAN
        )
    ''')

    # Data parsed from your notes
    # Format: (Title, Alt Titles, Original Title, Pub Year, Read Status)
    maigret_books = [
        ("Pietr the Latvian", "The Strange Case of Peter the Lett", "Pietr-le-Letton", 1931, True),
        ("The Carter of La Providence", "The Crime at Lock 14; Maigret Meets a Milord", "Le Charretier de la Providence", 1931, True),
        ("The Late Monsieur Gallet", "The Death of Monsieur Gallet; Maigret Stonewalled", "M. Gallet décédé", 1931, True),
        ("The Hanged Man of Saint-Pholien", "The Crime of Inspector Maigret; Maigret and the Hundred Gibbets", "Le Pendu de Saint-Pholien", 1931, True),
        ("A Man's Head", "A Battle of Nerves; Maigret's War of Nerves", "La Tête d'un homme", 1931, False),
        ("The Yellow Dog", "A Face for a Clue; Maigret and the Concarneau Murders", "Le Chien jaune", 1931, False),
        ("Night at the Crossroads", "Maigret at the Crossroads", "La Nuit du carrefour", 1931, False),
        ("A Crime in Holland", "Maigret in Holland", "Un Crime en Hollande", 1931, False),
        ("The Grand Banks Café", "The Sailors' Rendezvous; Maigret Answers a Plea", "Au Rendez-vous des Terre-Neuves", 1931, True),
        ("The Dancer at the Gai Moulin", "At the Gai Moulin; Maigret at the Gai Moulin", "La Danseuse du Gai-Moulin", 1931, False),
        ("The Two-Penny Bar", "Guinguette by the Seine; The Bar on the Seine", "La Guinguette à deux sous", 1932, False),
        ("The Shadow Puppet", "The Shadow in the Courtyard; Maigret Mystified", "L'Ombre chinoise", 1932, True),
        ("The Saint-Fiacre Affair", "Maigret and the Countess; Maigret Goes Home", "L'Affaire Saint-Fiacre", 1932, True),
        ("The Flemish House", "Maigret and the Flemish Shop", "Chez les Flamands", 1932, True),
        ("The Misty Harbour", "Death of a Harbour Master; Port of Shadows", "Le Port des brumes", 1932, False),
        ("The Madman of Bergerac", "", "Le Fou de Bergerac", 1932, False),
        ("Liberty Bar", "Maigret on the Riviera", "Liberty Bar", 1932, False),
        ("Lock No. 1", "The Lock at Charenton; Maigret Sits It Out", "L'Écluse nº 1", 1933, False),
        ("The Redhead", "", "La femme rousse", 1933, False),
        ("Maigret", "Maigret Returns", "Maigret", 1934, False),
        ("The Judge's House", "Maigret in Exile", "La Maison du juge", 1940, False),
        ("The Cellars of the Majestic", "The Hotel Majestic", "Les Caves du Majestic", 1942, False),
        ("Cecile is Dead", "Maigret and the Spinster", "Cécile est morte", 1942, False),
        ("Signed, Picpus", "Maigret and the Fortuneteller", "Signé Picpus", 1944, False),
        ("Félicie", "Maigret and the Toy Village", "Félicie est là", 1944, False),
        ("Inspector Cadaver", "Maigret's Rival", "L'Inspecteur Cadavre", 1944, False),
        ("Maigret Gets Angry", "Maigret in Retirement", "Maigret se fâche", 1947, False),
        ("Maigret in New York", "Inspector Maigret in New York's Underworld", "Maigret à New York", 1947, False),
        ("Maigret's Holiday", "A Summer Holiday; Maigret on Holiday", "Les Vacances de Maigret", 1947, False),
        ("Maigret's Dead Man", "Maigret's Special Murder", "Maigret et son mort", 1948, True),
        ("Maigret's First Case", "", "La Première enquête de Maigret, 1913", 1948, False),
        ("My Friend Maigret", "The Methods of Maigret", "Mon ami Maigret", 1949, False),
        ("Maigret at the Coroner's", "", "Maigret chez le coroner", 1949, False),
        ("Madame Maigret's Friend", "The Friend of Madame Maigret", "L'Amie de Mme Maigret", 1949, True),
        ("Maigret's Memoirs", "", "Les Mémoires de Maigret", 1950, False),
        ("Maigret and the Old Lady", "", "Maigret et la vieille dame", 1950, True),
        ("Maigret at Picratt's", "Maigret and the Strangled Stripper; Maigret in Montmartre", "Maigret au Picratt's", 1950, False),
        ("Maigret Takes a Room", "Maigret Rents a Room", "Maigret en meublé", 1951, False),
        ("Maigret and the Tall Woman", "Maigret and the Burglar's Wife", "Maigret et la grande perche", 1951, False),
        ("Maigret, Lognon and the Gangsters", "Inspector Maigret and the Killers", "Maigret, Lognon et les gangsters", 1951, False),
        ("Maigret's Revolver", "", "Le Revolver de Maigret", 1952, True),
        ("Maigret and the Man on the Bench", "The Man on the Boulevard", "Maigret et l'homme du banc", 1953, False),
        ("Maigret is Afraid", "Maigret Afraid", "Maigret a peur", 1953, False),
        ("Maigret's Mistake", "", "Maigret se trompe", 1953, False),
        ("Maigret Goes to School", "", "Maigret à l'école", 1953, True),
        ("Maigret and the Dead Girl", "Maigret and the Young Girl", "Maigret et la jeune morte", 1954, False),
        ("Maigret and the Minister", "Maigret and the Calame Report", "Maigret chez le ministre", 1954, False),
        ("Maigret and the Headless Corpse", "", "Maigret et le corps sans tête", 1955, False),
        ("Maigret Sets a Trap", "", "Maigret tend un piège", 1955, False),
        ("Maigret's Failure", "", "Un échec de Maigret", 1956, False),
        ("Maigret Enjoys Himself", "Maigret's Little Joke; None of Maigret's Business", "Maigret s'amuse", 1956, True),
        ("Maigret Travels", "Maigret and the Millionaires", "Maigret voyage", 1957, True),
        ("Maigret's Doubts", "Maigret Has Scruples", "Les scrupules de Maigret", 1957, False),
        ("Maigret and the Reluctant Witnesses", "", "Maigret et les témoins récalcitrants", 1958, False),
        ("Maigret's Secret", "Maigret Has Doubts", "Une confidence de Maigret", 1959, False),
        ("Maigret in Court", "", "Maigret aux assises", 1959, False),
        ("Maigret and the Old People", "Maigret in Society", "Maigret et les vieillards", 1960, False),
        ("Maigret and the Lazy Burglar", "Maigret and the Idle Burglar", "Maigret et le voleur paresseux", 1961, False),
        ("Maigret and the Good People of Montparnasse", "Maigret and the Black Sheep", "Maigret et les braves gens", 1961, False),
        ("Maigret and the Saturday Caller", "", "Maigret et le client du samedi", 1962, False),
        ("Maigret and the Tramp", "Maigret and the Dosser; Maigret and the Bum", "Maigret et le clochard", 1962, False),
        ("Maigret's Anger", "Maigret Loses His Temper", "La colère de Maigret", 1962, False),
        ("Maigret and the Ghost", "Maigret and the Apparition", "Maigret et le fantôme", 1963, False),
        ("Maigret Defends Himself", "Maigret on the Defensive", "Maigret se défend", 1964, False),
        ("Maigret's Patience", "The Patience of Maigret; Maigret Bides His Time", "La Patience de Maigret", 1965, False),
        ("Maigret and the Nahour Case", "", "Maigret et l'affaire Nahour", 1966, False),
        ("Maigret's Pickpocket", "Maigret and the Pickpocket", "Le voleur de Maigret", 1966, False),
        ("Maigret in Vichy", "Maigret Takes the Waters", "Maigret à Vichy", 1967, False),
        ("Maigret Hesitates", "", "Maigret hésite", 1968, False),
        ("Maigret's Childhood Friend", "Maigret's Boyhood Friend", "L'ami d'enfance de Maigret", 1968, True),
        ("Maigret and the Killer", "", "Maigret et le tueur", 1969, False),
        ("Maigret and the Wine Merchant", "", "Maigret et le marchand de vin", 1969, True),
        ("Maigret's Madwoman", "Maigret and the Madwoman", "La Folle de Maigret", 1970, False),
        ("Maigret and the Loner", "", "Maigret et l'homme tout seul", 1971, False),
        ("Maigret and the Informer", "Maigret and the Flea", "Maigret et l'indicateur", 1971, False),
        ("Maigret and Monsieur Charles", "", "Maigret et Monsieur Charles", 1972, False)
    ]

    cursor.executemany('INSERT INTO books VALUES (?,?,?,?,?)', maigret_books)
    conn.commit()
    conn.close()
    print("Database populated successfully with 75 Maigret novels!")

if __name__ == "__main__":
    setup_db()
