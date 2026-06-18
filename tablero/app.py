import random

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Taller - Subsidios Educativos", layout="centered")

st.title("Taller: Programa de subsidios educativos")
st.markdown(
    "Sube el archivo CSV y responde las preguntas "
    "para desbloquear cada sección del análisis."
)

# ── Session state ──────────────────────────────────────────────────

if "seccion_maxima" not in st.session_state:
    st.session_state.seccion_maxima = 1

# ── Sidebar ────────────────────────────────────────────────────────

with st.sidebar:
    progreso = (st.session_state.seccion_maxima - 1) / 6
    st.markdown("**Progreso**")
    st.progress(
        progreso,
        text=f"Sección {min(st.session_state.seccion_maxima, 7)} de 7",
    )
    if st.button("Reiniciar taller"):
        st.session_state.seccion_maxima = 1
        st.rerun()

# ── Upload ─────────────────────────────────────────────────────────

uploaded = st.file_uploader(
    "Sube tu archivo **subsidios_educativos.csv**", type="csv"
)

if uploaded is None:
    st.info("Esperando archivo...")
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# ANÁLISIS COMPLETO
# ═══════════════════════════════════════════════════════════════════

df = pd.read_csv(uploaded)
total_solicitudes = len(df)

# Calidad
dep_antes = df["departamento"].value_counts()
df["departamento"] = df["departamento"].str.lower().str.strip()
dep_despues = df["departamento"].value_counts()
dep_unicos = df["departamento"].nunique()

# KPIs
aprobados = df[df["estado_solicitud"] == "Aprobada"]
rechazados = df[df["estado_solicitud"] == "Rechazada"]
tasa_aprob = (df["estado_solicitud"] == "Aprobada").mean()
costo_total = df["costo_atencion"].sum() + df["costo_beneficio"].sum()
costo_por_benef = costo_total / len(aprobados)

# Impacto
perm_aprob = aprobados["permanencia_escolar"].mean()
perm_rech = rechazados["permanencia_escolar"].mean()
if pd.isna(perm_aprob):
    perm_aprob = 0.0
if pd.isna(perm_rech):
    perm_rech = 0.0

# SROI
inversion = costo_total
if inversion == 0:
    inversion = 1
est_add = (perm_aprob - perm_rech) * len(aprobados)
VALOR_SOCIAL = 5_000_000
valor_social_total = est_add * VALOR_SOCIAL
sroi_bruto = valor_social_total / inversion
sroi_ajustado = (valor_social_total * 0.85) / inversion

# Segmentación
vars_cluster = df[
    ["ingreso_hogar", "puntaje_focalizacion", "num_personas_hogar"]
]
scaler = StandardScaler()
vars_scaled = scaler.fit_transform(vars_cluster)
kmeans = KMeans(n_clusters=3, random_state=42)
df["segmento"] = kmeans.fit_predict(vars_scaled)

# ── Helpers ────────────────────────────────────────────────────────


def fmt_pct(val):
    return f"{val:.1%}"


def fmt_pesos(val):
    return f"${val:,.0f}"


# ═══════════════════════════════════════════════════════════════════
# SECCIONES
# ═══════════════════════════════════════════════════════════════════

secciones = [
    (1, "Carga y exploración inicial", "📂"),
    (2, "Calidad de datos", "🧹"),
    (3, "KPIs del programa", "📊"),
    (4, "Evaluación de impacto", "🎯"),
    (5, "SROI simplificado", "💰"),
    (6, "Segmentación", "🔍"),
    (7, "Conclusiones", "✅"),
]

for num, titulo, icono in secciones:
    desbloqueada = num <= st.session_state.seccion_maxima
    completada = num < st.session_state.seccion_maxima

    if not desbloqueada:
        st.markdown(f"**🔒 Sección {num}: {titulo}**")
        st.divider()
        continue

    st.markdown(f"## {icono} Sección {num}: {titulo}")

    # ── CONTENIDO ──────────────────────────────────────────────

    if num == 1:
        st.dataframe(df.head(10), use_container_width=True)

    elif num == 2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Antes de limpiar** (top 10)")
            st.dataframe(dep_antes.head(10))
        with col2:
            st.markdown("**Después de limpiar** (top 10)")
            st.dataframe(dep_despues.head(10))
        st.markdown(
            f"Se identificaron **? departamentos únicos** "
            "tras la limpieza."
        )

    elif num == 3:
        st.markdown(f"- **Tasa de aprobación:** {fmt_pct(tasa_aprob)}")
        st.markdown(f"- **Costo total:** {fmt_pesos(costo_total)}")
        st.markdown(
            f"- **Costo por beneficiario:** {fmt_pesos(costo_por_benef)}"
        )
        fig1, ax1 = plt.subplots()
        df["tipo_beneficio"].value_counts().plot(kind="bar", ax=ax1)
        ax1.set_title("Solicitudes por tipo de beneficio")
        ax1.set_ylabel("Cantidad")
        st.pyplot(fig1)
        plt.close(fig1)

    elif num == 4:
        st.markdown(
            f"- **Permanencia escolar — Aprobados:** {perm_aprob:.3f}"
        )
        st.markdown(
            f"- **Permanencia escolar — Rechazados:** {perm_rech:.3f}"
        )
        st.markdown(f"- **Diferencia:** {perm_aprob - perm_rech:+.3f}")
        fig2, ax2 = plt.subplots()
        pd.Series(
            {"Aprobados": perm_aprob, "Rechazados": perm_rech}
        ).plot(kind="bar", ax=ax2)
        ax2.set_title("Permanencia escolar por estado")
        ax2.set_ylabel("Promedio")
        st.pyplot(fig2)
        plt.close(fig2)

    elif num == 5:
        st.markdown(f"- **Inversión total:** {fmt_pesos(inversion)}")
        st.markdown(
            f"- **Estudiantes retenidos adicionales:** {est_add:.1f}"
        )
        st.markdown(
            f"- **Valor social por estudiante:** "
            f"{fmt_pesos(VALOR_SOCIAL)}"
        )
        st.markdown(
            f"- **Valor social total:** {fmt_pesos(valor_social_total)}"
        )
        st.markdown(
            f"- **SROI bruto:** {sroi_bruto:.2f} "
            f"(por cada $1 se generan ${sroi_bruto:.2f} en valor social)"
        )
        st.markdown(
            f"- **SROI ajustado (15% deadweight):** {sroi_ajustado:.2f}"
        )

    elif num == 6:
        st.markdown("**Perfil promedio por segmento:**")
        perfiles = (
            df.groupby("segmento")[
                ["ingreso_hogar", "puntaje_focalizacion",
                 "num_personas_hogar"]
            ]
            .mean()
        )
        st.dataframe(
            perfiles.style.format(
                {
                    "ingreso_hogar": "${:,.0f}",
                    "puntaje_focalizacion": "{:.1f}",
                    "num_personas_hogar": "{:.1f}",
                }
            )
        )
        fig3, ax3 = plt.subplots()
        ax3.scatter(
            df["puntaje_focalizacion"],
            df["ingreso_hogar"],
            c=df["segmento"],
            cmap="viridis",
            alpha=0.6,
        )
        ax3.set_xlabel("Puntaje de focalización")
        ax3.set_ylabel("Ingreso del hogar")
        ax3.set_title("Segmentación de solicitantes")
        st.pyplot(fig3)
        plt.close(fig3)

    elif num == 7:
        st.markdown("### Taller completado")
        st.balloons()
        st.markdown(
            """
**Conclusiones del análisis:**

1. Antes de analizar es necesario revisar la calidad de los datos.
2. La tasa de aprobación permite evaluar la cobertura del programa.
3. El costo por beneficiario ayuda a evaluar eficiencia financiera.
4. Los beneficiarios muestran una permanencia escolar diferente
   a los no beneficiarios.
5. El SROI muestra el retorno social generado por cada peso invertido
   en el programa.
6. La segmentación permite identificar grupos prioritarios para
   futuras asignaciones.
"""
        )

    # ── PREGUNTA ───────────────────────────────────────────────

    if num < 7 and not completada:
        st.divider()
        st.markdown(
            "**Responde correctamente para desbloquear "
            "la siguiente sección:**"
        )

        if num == 1:
            opciones = sorted(
                [
                    f"{total_solicitudes:,}",
                    f"{total_solicitudes + 250:,}",
                    f"{total_solicitudes - 250:,}",
                    f"{total_solicitudes + 500:,}",
                ],
                key=lambda x: int(x.replace(",", "")),
            )
            correcta = f"{total_solicitudes:,}"
            pregunta = "¿Cuántas solicitudes hay en el dataset?"

        elif num == 2:
            opciones = sorted(
                [
                    str(dep_unicos),
                    str(dep_unicos + 3),
                    str(dep_unicos - 3),
                    str(dep_unicos + 8),
                ],
                key=int,
            )
            correcta = str(dep_unicos)
            pregunta = (
                "Después de limpiar, "
                "¿cuántos departamentos distintos hay?"
            )

        elif num == 3:
            opciones = [
                fmt_pct(tasa_aprob),
                fmt_pct(tasa_aprob + 0.05),
                fmt_pct(tasa_aprob - 0.05),
                fmt_pct(tasa_aprob + 0.10),
            ]
            opciones.sort(key=lambda x: float(x.strip("%")))
            correcta = fmt_pct(tasa_aprob)
            pregunta = "¿Cuál es la tasa de aprobación del programa?"

        elif num == 4:
            if perm_aprob > perm_rech:
                correcta = "Mayor"
            elif perm_aprob < perm_rech:
                correcta = "Menor"
            else:
                correcta = "Igual"
            opciones = ["Mayor", "Menor", "Igual", "No se puede determinar"]
            pregunta = (
                "Los aprobados tienen una permanencia escolar "
                "promedio ___ que los rechazados."
            )

        elif num == 5:
            opcion_correcta = (
                "Por cada $1 invertido se generan "
                f"${sroi_bruto:.2f} en valor social"
            )
            opciones = [
                opcion_correcta,
                "Por cada ${:.2f} invertidos se genera $1 "
                "en valor social".format(sroi_bruto),
                "El SROI representa el costo total dividido "
                "por los beneficiarios",
                "El SROI mide cuántos estudiantes se retuvieron "
                "en el sistema escolar",
            ]
            random.Random(42).shuffle(opciones)
            correcta = opcion_correcta
            pregunta = "¿Cómo se interpreta el SROI bruto?"

        elif num == 6:
            opciones = ["2", "3", "4", "5"]
            correcta = "3"
            pregunta = (
                "¿Cuántos clústeres utilizó K-Means para segmentar?"
            )

        respuesta = st.radio(pregunta, opciones, key=f"q_{num}")
        if st.button("Responder", key=f"b_{num}"):
            if respuesta == correcta:
                st.success(
                    "Correcto. Siguiente sección desbloqueada."
                )
                st.session_state.seccion_maxima = max(
                    st.session_state.seccion_maxima, num + 1
                )
                st.rerun()
            else:
                st.error(
                    "Incorrecto. Revisa los resultados e intenta de nuevo."
                )

    elif num < 7 and completada:
        st.success("Sección completada")

    st.divider()
