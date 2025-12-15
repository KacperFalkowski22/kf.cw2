import streamlit as st
import pandas as pd

# Używamy st.session_state do przechowywania danych
# To symuluje prostą pamięć bez zapisu do pliku.
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = [] # Inicjalizacja pustej listy towarów

def dodaj_towar(nazwa_towaru):
    """Dodaje towar do listy magazynu."""
    if nazwa_towaru:
        # Dodajemy nowy towar do listy
        st.session_state.magazyn.append(nazwa_towaru.strip())
        st.success(f"Dodano towar: **{nazwa_towaru.strip()}**")
    else:
        st.warning("Nazwa towaru nie może być pusta.")

def usun_towar(indeks_towaru):
    """Usuwa towar z listy magazynu na podstawie indeksu."""
    try:
        nazwa_usunietego = st.session_state.magazyn.pop(indeks_towaru)
        st.success(f"Usunięto towar: **{nazwa_usunietego}**")
    except IndexError:
        st.error("Błąd: Nieprawidłowy indeks towaru do usunięcia.")

# --- Interfejs Streamlit ---

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("Dane są przechowywane tylko w pamięci sesji i znikną po odświeżeniu.")

## 1. Dodawanie Towaru
st.header("➕ Dodaj Nowy Towar")
nowy_towar_nazwa = st.text_input("Nazwa Towaru", key="input_dodaj")

if st.button("Dodaj do Magazynu"):
    dodaj_towar(nowy_towar_nazwa)
    # Wyczyszczenie pola wejściowego po dodaniu, dla lepszego UX
    st.session_state.input_dodaj = ""

st.markdown("---")

## 2. Stan Magazynu
st.header("📋 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Tworzymy DataFrame dla lepszej wizualizacji w Streamlit
    # Kolumna 'Indeks' jest potrzebna do łatwego usuwania
    dane = {
        'Indeks': list(range(len(st.session_state.magazyn))),
        'Nazwa Towaru': st.session_state.magazyn
    }
    df = pd.DataFrame(dane)
    
    # Wyświetlamy tabelę
    st.dataframe(df, hide_index=True)
    
    st.subheader("🗑️ Usuń Towar")
    # Pole do wprowadzenia indeksu towaru do usunięcia
    indeks_do_usuniecia = st.number_input(
        "Wprowadź Indeks Towaru do usunięcia", 
        min_value=0, 
        max_value=len(st.session_state.magazyn) - 1, 
        step=1,
        key="input_usun",
        format="%d"
    )
    
    if st.button("Usuń z Magazynu"):
        usun_towar(indeks_do_usuniecia)
        # Ponowne wyświetlenie stanu magazynu po usunięciu
        st.experimental_rerun()
        
else:
    st.info("Magazyn jest obecnie pusty.")
