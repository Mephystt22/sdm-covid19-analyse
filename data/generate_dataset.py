"""
generate_dataset.py
--------------------
Genere un jeu de donnees clinique COVID-19 realiste et VOLONTAIREMENT "sale"
(valeurs manquantes, doublons, valeurs aberrantes, categories incoherentes)
afin de pouvoir demontrer toutes les fonctionnalites de nettoyage et de
preprocessing de l'application.

Auteur : Saad Elidrissi El Hassan
Usage  : python generate_dataset.py
Sortie : covid19_clinical_dataset.csv
"""

import numpy as np
import pandas as pd

# Graine fixe -> dataset reproductible
RNG = np.random.default_rng(42)
N = 1400  # nombre de patients


def main() -> None:
    pays = ["Morocco", "France", "Spain", "Italy", "Germany",
            "Egypt", "Tunisia", "USA", "Brazil", "India"]
    regions = ["Casablanca-Settat", "Rabat-Sale", "Marrakech", "Fes-Meknes",
               "Tanger", "Ile-de-France", "Lombardia", "Madrid", "Bavaria", "Cairo"]

    # --- Variables de base ---
    age = RNG.normal(54, 18, N).clip(1, 98).round(0)

    # Genre : uniquement Male / Female
    genre = RNG.choice(["Male", "Female"], size=N, p=[0.5, 0.5])

    pays_col = RNG.choice(pays, size=N)
    region_col = RNG.choice(regions, size=N)

    # Date d'admission -> sert pour l'analyse temporelle
    base = pd.Timestamp("2020-03-01")
    jours = RNG.integers(0, 760, size=N)  # ~2 ans
    date_admission = base + pd.to_timedelta(jours, unit="D")

    # --- Mesures cliniques ---
    temperature = RNG.normal(37.8, 0.9, N).round(1)
    spo2 = RNG.normal(94, 5, N).clip(60, 100).round(0)
    freq_cardiaque = RNG.normal(88, 15, N).clip(40, 180).round(0)
    pression_systolique = RNG.normal(128, 18, N).clip(80, 220).round(0)
    globules_blancs = RNG.normal(8.5, 3.2, N).clip(1, 30).round(1)   # 10^9/L
    crp = RNG.gamma(3.0, 18.0, N).round(1)                            # mg/L
    d_dimere = RNG.gamma(2.0, 0.5, N).round(2)                        # mg/L
    ct_pcr = RNG.normal(24, 6, N).clip(10, 40).round(1)              # valeur Ct

    # --- Comorbidites (0/1) ---
    diabete = RNG.choice([0, 1], size=N, p=[0.72, 0.28])
    hypertension = RNG.choice([0, 1], size=N, p=[0.62, 0.38])
    cardiaque = RNG.choice([0, 1], size=N, p=[0.80, 0.20])

    tabagisme = RNG.choice(["Never", "Former", "Current"],
                           size=N, p=[0.55, 0.28, 0.17])

    # --- Severite correlee a l'age et a la SpO2 ---
    score = (age / 30) + (95 - spo2) / 5 + diabete + hypertension + cardiaque
    severite = np.where(score < 3, "Mild",
                np.where(score < 5, "Moderate",
                np.where(score < 7, "Severe", "Critical")))

    hospitalise = (score > 3.5).astype(int)
    soins_intensifs = ((score > 6) & (RNG.random(N) > 0.3)).astype(int)
    ventilateur = ((soins_intensifs == 1) & (RNG.random(N) > 0.4)).astype(int)
    duree_sejour = (RNG.gamma(2.0, 3.0, N) * (1 + hospitalise)).round(0).clip(0, 60)

    vaccination = RNG.choice(["Unvaccinated", "Partial", "Full", "Booster"],
                             size=N, p=[0.35, 0.20, 0.30, 0.15])

    # Issue correlee a la severite
    p_deces = np.clip((score - 4) / 12, 0.01, 0.6)
    issue = np.where(RNG.random(N) < p_deces, "Deceased", "Recovered")

    df = pd.DataFrame({
        "patient_id": np.arange(1, N + 1),
        "age": age,
        "gender": genre,
        "country": pays_col,
        "region": region_col,
        "admission_date": date_admission,
        "body_temperature": temperature,
        "oxygen_saturation": spo2,
        "heart_rate": freq_cardiaque,
        "systolic_bp": pression_systolique,
        "wbc_count": globules_blancs,
        "crp_level": crp,
        "d_dimer": d_dimere,
        "pcr_ct_value": ct_pcr,
        "diabetes": diabete,
        "hypertension": hypertension,
        "cardiac_disease": cardiaque,
        "smoking_status": tabagisme,
        "symptom_severity": severite,
        "hospitalized": hospitalise,
        "icu_admission": soins_intensifs,
        "ventilator_support": ventilateur,
        "length_of_stay": duree_sejour,
        "vaccination_status": vaccination,
        "outcome": issue,
    })

    # =========================================================
    #  ON "SALIT" LE DATASET POUR LA DEMONSTRATION
    # =========================================================

    # 1) Valeurs manquantes dans plusieurs colonnes
    for col, frac in {
        "oxygen_saturation": 0.06,
        "crp_level": 0.10,
        "d_dimer": 0.12,
        "smoking_status": 0.05,
        "body_temperature": 0.04,
        "vaccination_status": 0.03,
    }.items():
        idx = RNG.choice(N, size=int(N * frac), replace=False)
        df.loc[idx, col] = np.nan

    # 2) Valeurs aberrantes (outliers) evidentes
    out_idx = RNG.choice(N, size=12, replace=False)
    df.loc[out_idx[:4], "age"] = [210, 255, 0, 199]
    df.loc[out_idx[4:8], "body_temperature"] = [50.0, 12.0, 47.5, 5.0]
    df.loc[out_idx[8:], "heart_rate"] = [400, 5, 350, 2]

    # 3) Doublons (on duplique ~25 lignes)
    dup = df.sample(25, random_state=7)
    df = pd.concat([df, dup], ignore_index=True)

    # 4) Melange final
    df = df.sample(frac=1.0, random_state=11).reset_index(drop=True)

    out = "covid19_clinical_dataset.csv"
    df.to_csv(out, index=False)
    print(f"OK -> {out}  ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
    print(f"Valeurs manquantes totales : {int(df.isna().sum().sum())}")
    print(f"Doublons               : {int(df.duplicated().sum())}")


if __name__ == "__main__":
    main()
