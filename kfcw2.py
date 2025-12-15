import streamlit as st
import pandas as pd
from collections import Counter

# --- Inicjalizacja Stanu Magazynu ---
# Używamy st.session_state do przechowywania listy wszystkich towarów.
# Towary są po prostu przechowywane jako lista nazw.
if 'magazyn' not in st.session_state:
    # Inicjalizacja z podanymi towarami
    initial_items = ["chleb", "bułka", "kiełbasa", "ketchup"]
    st.session_state.magazyn = initial_items
    st.session_state.last_action = "" # Do wyświetlania ostatniej operacji

def dodaj_towar(nazwa_towaru):
    """Dodaje towar do listy magazynu."""
    nazwa_towaru = nazwa_towaru.strip()
    if nazwa_towaru:
        st.session_state.magazyn.append(nazwa_towaru)
        st.session_state.last_action = f"✅ Dodano: **{nazwa_towaru}**"
    else:
        st.session_state.last_action = "⚠️ Nazwa towaru nie może być pusta."

def usun_towar(nazwa_towaru):
    """Usuwa JEDNĄ instancję towaru z listy magazynu."""
    nazwa_towaru = nazwa_towaru.strip()
    if nazwa_towaru in st.session_state.magazyn:
        st.session_state.magazyn.remove(nazwa_towaru)
        st.session_state.last_action = f"❌ Usunięto jedną sztukę: **{nazwa_towaru}**"
    else:
        st.session_state.last_action = f"🚫 Towar **{nazwa_towaru}** nie znajduje się w magazynie."

def przelicz_stan_magazynu():
    """Zlicza ilości poszczególnych towarów w magazynie."""
    # Używamy Counter do szybkiego zliczenia wystąpień każdej nazwy na liście
    stan_count = Counter(st.session_state.magazyn)
    
    # Przekształcamy to na listę słowników lub DataFrame dla lepszego wyświetlania
    dane_magazynu = [{
        'Nazwa Towaru': nazwa,
        'Ilość w Magazynie': ilosc
    } for nazwa, ilosc in stan_count.items()]
    
    return pd.DataFrame(dane_magazynu)

# --- Interfejs Streamlit ---

st.title("📦 Prosty Magazyn (Towary i Ilości)")
st.caption("Dane są przechowywane tylko w pamięci sesji i znikną po odświeżeniu.")

st.subheader("Aktualna Lista Operacji:")
st.markdown(st.session_state.last_action if st.session_state.last_action else "Brak ostatniej operacji.")

st.markdown("---")

## 1. Dodawanie i Usuwanie Towaru

col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ Dodaj Towar")
    nazwa_dodaj = st.text_input("Nazwa do Dodania", key="input_dodaj")
    if st.button("Dodaj do Magazynu"):
        dodaj_towar(nazwa_dodaj)
        st.session_state.input_dodaj = "" # Wyczyszczenie pola
        st.rerun()

with col2:
    st.subheader("🗑️ Usuń Towar (Jedna Sztuka)")
    nazwa_usun = st.text_input("Nazwa do Usunięcia", key="input_usun")
    if st.button("Usuń z Magazynu"):
        usun_towar(nazwa_usun)
        st.session_state.input_usun = "" # Wyczyszczenie pola
        st.rerun()

st.markdown("---")

## 2. Stan Magazynu (Nazwa i Ilość)

st.header("📋 Zestawienie Magazynowe")

if st.session_state.magazyn:
    df_magazyn = przelicz_stan_magazynu()
    
    # Wyświetlamy tabelę z nazwami i zliczonymi ilościami
    st.dataframe(
        df_magazyn, 
        hide_index=True,
        # Opcjonalne formatowanie szerokości kolumn dla lepszej czytelności
        column_config={
            "Nazwa Towaru": st.column_config.TextColumn(width="large"),
            "Ilość w Magazynie": st.column_config.NumberColumn(format="%d")
        }
    )
    st.write(f"**Łączna liczba wszystkich pozycji w magazynie:** {len(st.session_state.magazyn)}")
else:
    st.info("Magazyn jest obecnie pusty.")
