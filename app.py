import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from fuzzy_controller import calculate_productivity, RULE_TEXTS


st.set_page_config(
    page_title="FuzzyDev",
    page_icon="🧠",
    layout="wide"
)

st.title("FuzzyDev")
st.subheader("Akıllı Yazılım Geliştirici Verimlilik ve Yorgunluk Analiz Sistemi")

st.write(
    """
    Bu uygulama; çalışma süresi, uyku süresi, aktivite seviyesi ve stres seviyesini kullanarak
    bulanık mantık yöntemiyle 0-100 arası verimlilik skoru üretir.
    """
)

st.sidebar.header("Giriş Değerleri")

work_hours = st.sidebar.slider("Çalışma Süresi (saat)", 0, 12, 6)
sleep_hours = st.sidebar.slider("Uyku Süresi (saat)", 0, 10, 7)
activity = st.sidebar.slider("Aktivite Seviyesi", 0, 100, 70)
stress = st.sidebar.slider("Stres Seviyesi", 0, 100, 30)

calculate_button = st.sidebar.button("Hesapla")

if "result_data" not in st.session_state:
    st.session_state.result_data = None

if calculate_button:
    result, variables, active_rules, degrees = calculate_productivity(
        work_hours,
        sleep_hours,
        activity,
        stress
    )

    st.session_state.result_data = {
        "result": result,
        "variables": variables,
        "active_rules": active_rules,
        "degrees": degrees
    }

if st.session_state.result_data:
    result = st.session_state.result_data["result"]
    variables = st.session_state.result_data["variables"]
    active_rules = st.session_state.result_data["active_rules"]
    degrees = st.session_state.result_data["degrees"]

    if result < 25:
        level = "Çok Düşük"
        comment = "Verimlilik oldukça düşük. Dinlenme, stres azaltma ve çalışma süresini dengeleme önerilir."
    elif result < 45:
        level = "Düşük"
        comment = "Verimlilik düşük. Uyku, stres ve aktivite dengesi iyileştirilmelidir."
    elif result < 65:
        level = "Orta"
        comment = "Verimlilik orta seviyede. Sistem dengeli veya kararsız bir çalışma durumu göstermektedir."
    elif result < 85:
        level = "Yüksek"
        comment = "Verimlilik yüksek. Çalışma koşulları genel olarak olumlu görünmektedir."
    else:
        level = "Çok Yüksek"
        comment = "Verimlilik çok yüksek. Uyku, aktivite ve stres dengesi oldukça iyi durumdadır."

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.metric("Verimlilik Skoru", f"{result} / 100")

    with col2:
        st.metric("Verimlilik Seviyesi", level)

    with col3:
        st.metric("Aktif Kural Sayısı", len(active_rules))

    st.info(comment)

    st.divider()

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.header("Durulaştırılmış Çıkış")

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.bar(["Skor"], [result], width=0.4)
        ax.set_ylim(0, 100)
        ax.set_title("Verimlilik Sonucu", fontsize=10)
        ax.tick_params(labelsize=8)
        plt.tight_layout()

        st.pyplot(fig, use_container_width=False)

    with right_col:
        st.header("Üyelik Fonksiyonları")

        selected_variable = st.selectbox(
            "Grafiğini görmek istediğiniz değişken:",
            ["work_hours", "sleep_hours", "activity", "stress", "productivity"]
        )

        variable = variables[selected_variable]

        fig, ax = plt.subplots(figsize=(5, 2.5))

        for term_name, membership in variable.terms.items():
            ax.plot(
                variable.universe,
                membership.mf,
                linewidth=2,
                label=term_name
            )

        ax.set_title(selected_variable, fontsize=10)
        ax.set_xlabel("Değer", fontsize=8)
        ax.set_ylabel("Üyelik", fontsize=8)
        ax.tick_params(labelsize=8)
        ax.legend(fontsize=7, loc="upper right")
        plt.tight_layout()

        st.pyplot(fig, use_container_width=False)

    st.divider()

    st.header("Giriş Değerlerinin Üyelik Dereceleri")

    degree_df = pd.DataFrame([
        {"Değişken": "Çalışma Süresi", "Dilsel Değer": "Az", "Üyelik Derecesi": round(degrees["work_low"], 3)},
        {"Değişken": "Çalışma Süresi", "Dilsel Değer": "Normal", "Üyelik Derecesi": round(degrees["work_normal"], 3)},
        {"Değişken": "Çalışma Süresi", "Dilsel Değer": "Fazla", "Üyelik Derecesi": round(degrees["work_high"], 3)},

        {"Değişken": "Uyku Süresi", "Dilsel Değer": "Kötü", "Üyelik Derecesi": round(degrees["sleep_bad"], 3)},
        {"Değişken": "Uyku Süresi", "Dilsel Değer": "Orta", "Üyelik Derecesi": round(degrees["sleep_medium"], 3)},
        {"Değişken": "Uyku Süresi", "Dilsel Değer": "İyi", "Üyelik Derecesi": round(degrees["sleep_good"], 3)},

        {"Değişken": "Aktivite", "Dilsel Değer": "Düşük", "Üyelik Derecesi": round(degrees["activity_low"], 3)},
        {"Değişken": "Aktivite", "Dilsel Değer": "Orta", "Üyelik Derecesi": round(degrees["activity_medium"], 3)},
        {"Değişken": "Aktivite", "Dilsel Değer": "Yüksek", "Üyelik Derecesi": round(degrees["activity_high"], 3)},

        {"Değişken": "Stres", "Dilsel Değer": "Düşük", "Üyelik Derecesi": round(degrees["stress_low"], 3)},
        {"Değişken": "Stres", "Dilsel Değer": "Orta", "Üyelik Derecesi": round(degrees["stress_medium"], 3)},
        {"Değişken": "Stres", "Dilsel Değer": "Yüksek", "Üyelik Derecesi": round(degrees["stress_high"], 3)},
    ])

    st.dataframe(degree_df, use_container_width=True)

    st.divider()

    st.header("Aktif Kurallar")

    if active_rules:
        active_rule_df = pd.DataFrame(active_rules)
        st.dataframe(active_rule_df, use_container_width=True)
    else:
        st.warning("Bu giriş değerleri için aktif kural bulunamadı.")

    st.divider()

    st.header("Tüm Kural Tabanı")

    for i, rule in enumerate(RULE_TEXTS, start=1):
        st.write(f"{i}. {rule}")

else:
    st.warning("Sol menüden giriş değerlerini seçip Hesapla butonuna basın.")

st.divider()

st.header("Test Senaryoları")

try:
    test_df = pd.read_csv("test_results/test_senaryolari.csv")
    st.dataframe(test_df, use_container_width=True)
except FileNotFoundError:
    st.warning("test_results/test_senaryolari.csv dosyası bulunamadı.")