"""CryptoBox - brique 1 : Cesar, Substitution, Transposition par colonnes.
Aucune bibliotheque de cryptographie. Lettres majuscules A-Z uniquement."""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def nettoyer(texte):
    """Met en majuscules et ne garde que A-Z."""
    return "".join(c for c in texte.upper() if c in ALPHABET)


# ---------- Cesar ----------
def cesar_chiffrer(msg, k):
    return "".join(ALPHABET[(ALPHABET.index(c) + k) % 26] for c in nettoyer(msg))


def cesar_dechiffrer(msg, k):
    return cesar_chiffrer(msg, -k)


def cesar_force_brute(msg):
    """Teste les 25 cles (1 a 25) et renvoie la liste (k, texte)."""
    return [(k, cesar_dechiffrer(msg, k)) for k in range(1, 26)]


# ---------- Substitution ----------
def verifier_cle_substitution(cle):
    cle = nettoyer(cle)
    if len(cle) != 26 or set(cle) != set(ALPHABET):
        raise ValueError("La cle doit contenir les 26 lettres, chacune une seule fois.")
    return cle


def substitution_chiffrer(msg, cle):
    cle = verifier_cle_substitution(cle)
    return "".join(cle[ALPHABET.index(c)] for c in nettoyer(msg))


def substitution_dechiffrer(msg, cle):
    cle = verifier_cle_substitution(cle)
    return "".join(ALPHABET[cle.index(c)] for c in nettoyer(msg))


# ---------- Transposition par colonnes ----------
def ordre_colonnes(mot):
    """Indices des colonnes dans l'ordre alphabetique du mot-cle
    (egalite : la lettre la plus a gauche passe en premier)."""
    return sorted(range(len(mot)), key=lambda i: (mot[i], i))


def transposition_chiffrer(msg, mot):
    msg, mot = nettoyer(msg), nettoyer(mot)
    n = len(mot)
    while len(msg) % n != 0:
        msg += "X"
    lignes = [msg[i:i + n] for i in range(0, len(msg), n)]
    return "".join("".join(ligne[c] for ligne in lignes) for c in ordre_colonnes(mot))


def transposition_dechiffrer(msg, mot):
    msg, mot = nettoyer(msg), nettoyer(mot)
    n = len(mot)
    nb_lignes = len(msg) // n
    colonnes = {}
    for pos, c in enumerate(ordre_colonnes(mot)):
        colonnes[c] = msg[pos * nb_lignes:(pos + 1) * nb_lignes]
    return "".join(colonnes[c][r] for r in range(nb_lignes) for c in range(n))


# ---------- Tests ----------
def tests():
    assert cesar_chiffrer("BONJOUR", 3) == "ERQMRXU"
    assert cesar_dechiffrer("ERQMRXU", 3) == "BONJOUR"
    cle = "QWERTYUIOPASDFGHJKLZXCVBNM"
    assert substitution_chiffrer("ATTAQUE", cle) == "QZZQJXT"
    assert substitution_dechiffrer("QZZQJXT", cle) == "ATTAQUE"
    assert transposition_chiffrer("RENDEZVOUSAMIDI", "PORTE") == "ESIEVMRZANOIDUD"
    assert transposition_dechiffrer("ESIEVMRZANOIDUD", "PORTE") == "RENDEZVOUSAMIDI"
    print("Tous les tests passent.")


# ---------- Challenge : binome 41 ----------
def challenge():
    intercepte = "MXJIWXSKSXBX"
    cle_sub = "IFZRYHDJUBQEPCKXGMANVLSTOW"
    mot_cle = "CHAISE"
    # Ordre de chiffrement : Cesar -> Substitution -> Transposition
    # On retire donc : Transposition, puis Substitution, puis Cesar.
    etape1 = transposition_dechiffrer(intercepte, mot_cle)
    etape2 = substitution_dechiffrer(etape1, cle_sub)
    print("Apres transposition :", etape1)
    print("Apres substitution  :", etape2)
    for k, texte in cesar_force_brute(etape2):
        print(f"k = {k:2d} : {texte}")


# ---------- Menu terminal ----------
def menu():
    while True:
        print("\n=== CryptoBox ===")
        print("1. Cesar chiffrer   2. Cesar dechiffrer   3. Cesar force brute")
        print("4. Substitution chiffrer   5. Substitution dechiffrer")
        print("6. Transposition chiffrer  7. Transposition dechiffrer")
        print("0. Quitter")
        choix = input("Choix : ").strip()
        try:
            if choix == "0":
                break
            msg = input("Message : ")
            if choix == "1":
                print(cesar_chiffrer(msg, int(input("Cle k : "))))
            elif choix == "2":
                print(cesar_dechiffrer(msg, int(input("Cle k : "))))
            elif choix == "3":
                for k, t in cesar_force_brute(msg):
                    print(f"k = {k:2d} : {t}")
            elif choix == "4":
                print(substitution_chiffrer(msg, input("Cle (26 lettres) : ")))
            elif choix == "5":
                print(substitution_dechiffrer(msg, input("Cle (26 lettres) : ")))
            elif choix == "6":
                print(transposition_chiffrer(msg, input("Mot-cle : ")))
            elif choix == "7":
                print(transposition_dechiffrer(msg, input("Mot-cle : ")))
            else:
                print("Choix invalide.")
        except ValueError as e:
            print("Erreur :", e)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "challenge":
        challenge()
    else:
        menu()
