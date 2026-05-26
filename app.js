document.body.innerHTML = '';

// ==========================================
// SEKCJA 1: Wpisanie funkcji ręcznie
// ==========================================
const sekcjaTekstowa = document.createElement('div');
sekcjaTekstowa.className = 'sekcja'; 

const tytul1 = document.createElement('h3');
tytul1.innerText = '1. Wpisz funkcję logiczną z klawiatury:';

const poleTekstowe = document.createElement('input');
poleTekstowe.type = 'text';
poleTekstowe.placeholder = 'np. A AND B';
poleTekstowe.style.marginRight = '10px';
poleTekstowe.style.padding = '5px';

const przyciskTekst = document.createElement('button');
przyciskTekst.innerText = 'Wyślij funkcję';

sekcjaTekstowa.appendChild(tytul1);
sekcjaTekstowa.appendChild(poleTekstowe);
sekcjaTekstowa.appendChild(przyciskTekst);
document.body.appendChild(sekcjaTekstowa);

przyciskTekst.addEventListener('click', () => {
    // Pobieramy tekst i automatycznie zamieniamy na WIELKIE LITERY
    const tekstFunkcji = poleTekstowe.value.trim().toUpperCase(); 
    
    if (!tekstFunkcji) {
        alert('Wpisz najpierw formułę logiczną!');
        return;
    }

    const payload = {
        plaintext: tekstFunkcji
    };

    fetch('http://127.0.0.1:8000/expression', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) throw new Error(`Błąd: ${response.status}`);
        return response.json();
    })
    .then(data => {
        alert(`Sukces (Sekcja Tekstowa)!\nFormuła: ${data.sympy_expr}\nZmienne: ${data.vars.join(', ')}`);
    })
    .catch(error => {
        console.error(error);
        alert('Błąd połączenia z backendem przy wysyłaniu tekstu!');
    });
});


// ==========================================
// SEKCJA 2: Generator Tabeli Prawdy
// ==========================================
const sekcjaTabeli = document.createElement('div');
sekcjaTabeli.className = 'sekcja';

const tytul2 = document.createElement('h3');
tytul2.innerText = '2. Lub wygeneruj tabelę prawdy:';

const etykieta = document.createElement('label');
etykieta.innerText = 'Liczba zmiennych (np. 3): ';

const poleIloscZmiennych = document.createElement('input');
poleIloscZmiennych.type = 'number';
poleIloscZmiennych.value = '3';
poleIloscZmiennych.min = '1';
poleIloscZmiennych.max = '5';
poleIloscZmiennych.style.width = '40px';
poleIloscZmiennych.style.marginRight = '10px';

const przyciskGeneruj = document.createElement('button');
przyciskGeneruj.innerText = 'Generuj tabelę';

const kontenerNaTabele = document.createElement('div'); 

sekcjaTabeli.appendChild(tytul2);
sekcjaTabeli.appendChild(etykieta);
sekcjaTabeli.appendChild(poleIloscZmiennych);
sekcjaTabeli.appendChild(przyciskGeneruj);
sekcjaTabeli.appendChild(kontenerNaTabele);
document.body.appendChild(sekcjaTabeli);


przyciskGeneruj.addEventListener('click', () => {
    kontenerNaTabele.innerHTML = ''; 
    
    const ileZmiennych = parseInt(poleIloscZmiennych.value);
    const tabela = document.createElement('table');
    
    const wierszNaglowkowy = document.createElement('tr');
    for (let i = 0; i < ileZmiennych; i++) {
        const th = document.createElement('th');
        th.innerText = `X${i + 1}`;
        wierszNaglowkowy.appendChild(th);
    }
    const thWynik = document.createElement('th');
    thWynik.innerText = "Wynik (Y)";
    wierszNaglowkowy.appendChild(thWynik);
    tabela.appendChild(wierszNaglowkowy);

    const liczbaWierszy = Math.pow(2, ileZmiennych);
    for (let i = 0; i < liczbaWierszy; i++) {
        const wiersz = document.createElement('tr');
        const binarnie = i.toString(2).padStart(ileZmiennych, '0');
        
        for (let bit of binarnie) {
            const komorka = document.createElement('td');
            komorka.innerText = bit;
            wiersz.appendChild(komorka);
        }

        const wynikTd = document.createElement('td');
        const poleWyniku = document.createElement('button');
        poleWyniku.innerText = '0'; 
        poleWyniku.className = 'wynik-btn'; 
        poleWyniku.style.width = '40px';
        poleWyniku.style.height = '30px';
        poleWyniku.style.cursor = 'pointer';
        poleWyniku.style.fontWeight = 'bold';
        
        poleWyniku.addEventListener('click', (event) => {
            if (event.target.innerText === '0') {
                event.target.innerText = '1';
            } else if (event.target.innerText === '1') {
                event.target.innerText = '-';
            } else {
                event.target.innerText = '0';
            }
        });

        wynikTd.appendChild(poleWyniku);
        wiersz.appendChild(wynikTd);
        tabela.appendChild(wiersz);
    }
    
    kontenerNaTabele.appendChild(tabela);

    const przyciskWyslijTabele = document.createElement('button');
    przyciskWyslijTabele.innerText = 'Wyślij wyniki z tabeli';
    przyciskWyslijTabele.style.marginTop = '15px';
    kontenerNaTabele.appendChild(przyciskWyslijTabele);

    przyciskWyslijTabele.addEventListener('click', () => {
        const wszystkiePola = kontenerNaTabele.querySelectorAll('.wynik-btn');
        const minterms = [];
        const dontcares = [];
        const naglowki = Array.from(tabela.querySelectorAll('th')).slice(0, ileZmiennych).map(th => th.innerText);

        wszystkiePola.forEach((pole, index) => {
            // Konwertujemy numer wiersza na tablicę intów, np. 3 -> [0, 1, 1]
            const kombinacjaBinarna = index.toString(2)
                .padStart(ileZmiennych, '0')
                .split('')
                .map(bit => parseInt(bit));

            if (pole.innerText === '1') {
                minterms.push(kombinacjaBinarna); 
            } else if (pole.innerText === '-') {
                dontcares.push(kombinacjaBinarna); 
            }
        });

        const payload = {
            vars: naglowki,
            ttable_readable: [minterms, dontcares]
        };

        fetch('http://127.0.0.1:8000/expression/nand', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) throw new Error(`Błąd: ${response.status}`);
            return response.json();
        })
        .then(data => {
            alert(`Sukces!\nFormuła: ${data.sympy_expr}\nPostać NAND: ${data.nand_sympy_expr || 'Brak'}`);
        })
        .catch(error => {
            console.error(error);
            alert('Nie udało się połączyć z backendem. Upewnij się, że serwer Pythona działa na porcie 8000!');
        });
    });
});

przyciskGeneruj.click();