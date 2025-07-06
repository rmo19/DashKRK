import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Ke Riko Dashboard",
    page_icon="",
    layout="wide")

alt.themes.enable("dark")

st.title('Ke Riko Dashboard')

df_original = pd.read_csv('datos_estructurados_keriko.csv')

df_original['ano'] = pd.to_datetime(df_original['ano'], format='%Y')

# --- FILTRO GLOBAL DE AÑO ---
years = sorted(df_original['ano'].dt.year.unique())
years.insert(0, "Todos")  # Agrega opción para ver todos los años

# Selector en la barra lateral
year = st.sidebar.selectbox("Selecciona el año", years)

# Filtrado del DataFrame
if year == "Todos":
    df = df_original
else:
    df = df_original[df_original['ano'].dt.year == year]

col1, col2, col3, col4 = st.columns(4)
total_revenue1 = df['sales'].sum()
total_revenue = df['precio'].sum()
col1.metric("Ventas totales", f"${total_revenue:,.2f}")

total_orders = df['folio'].nunique()
col2.metric("Numero de ordenes", f"{total_orders:,}")

aov = total_revenue/total_orders
col3.metric("ticket promedio", f"${aov:.2f}")

#ventas por mes

revenue = df.groupby('mes')['precio'].sum().reset_index()
if year == 2025:
    month_order = ['January', 'February', 'March', 'April', 'May', 'June']
else:
    month_order = ['June', 'July', 'August', 'September', 'October', 'November','December']

    

revenue['mes'] = pd.Categorical(revenue['mes'], categories=month_order, ordered=True)

revenue = revenue.sort_values('mes')

fig1 = px.bar(
    revenue,
    x='mes',
    y='precio',
    title='Ventas por mes',
    labels={'precio': 'Precio', 'mes': 'Mes'},
    color='mes',
    text='precio'  # Esto habilita las etiquetas
)

# Modificar trazas para mostrar texto encima y quitar hover
fig1.update_traces(
    textposition='outside',
    hoverinfo='skip',
    hovertemplate=None
)
# Remove the legend
fig1.update_layout(showlegend=False)



df['ano'] = df['ano'].astype(int)

# Convertir mes a número
df['mes_num'] = pd.to_datetime(df['mes'], format='%B').dt.month

# Calcular trimestre a partir del número de mes
df['quarter_num'] = ((df['mes_num'] - 1) // 3) + 1  # 1 a 4

df['quarter'] = df['ano'].astype(str) + 'Q' + df['quarter_num'].astype(str)

# Agrupar por trimestre y sumar precios
revenue_quarter = df.groupby('quarter')['precio'].sum().reset_index()

# Ordenar categorías para eje X
revenue_quarter['quarter'] = pd.Categorical(
    revenue_quarter['quarter'],
    categories=sorted(revenue_quarter['quarter'].unique()),
    ordered=True
)

revenue_quarter = revenue_quarter.sort_values('quarter')

# Crear gráfico de barras con Plotly Express
fig2 = px.bar(
    revenue_quarter,
    x='quarter',
    y='precio',
    title='Ventas por Trimestre',
    labels={'quarter': 'Trimestre', 'precio': 'Precio'},
    color='quarter'
)

# Ocultar leyenda y forzar eje X categórico para que muestre etiquetas correctas
fig2.update_layout(showlegend=False)
fig2.update_xaxes(type='category')

product_revenue = df.groupby('descripcion')['precio'].sum().reset_index()



top_10_products = product_revenue.sort_values('precio', ascending = False)[0:10]

# Top 10 Products by Revenue
fig3 = px.bar(
    top_10_products,
    x='precio',
    y='descripcion',
    title='Top 10 Productos por venta',
    labels={'descripcion': 'Producto', 'precio': 'Venta'},
    color='descripcion',
)
# Remove the legend
fig3.update_layout(showlegend=False)

category_aov = df.groupby('categoria')['precio'].mean().reset_index()
category_aov = category_aov.sort_values(by='precio', ascending=False)

# Average Order Value by Category
fig4 = px.bar(
    category_aov,
    x='precio',
    y='categoria',
    title='Ticker promedio por categoria',
    labels={'precio': 'Ventas', 'categoria': 'Categoria'},
    color='categoria',
)

# Remove the legend
fig4.update_layout(showlegend=False)

category_count = df['categoria'].value_counts().reset_index()


df['hora'] = pd.to_datetime(df['hora']).dt.hour

# Agrupar
order_per_hour = df.groupby('hora')['folio'].count().reset_index()
order_per_hour.rename(columns={'folio': 'count_of_orders'}, inplace=True)
order_per_hour = order_per_hour.sort_values('hora')

# Gráfica
fig6 = px.line(
    order_per_hour,
    x='hora',
    y='count_of_orders',
    title='Hora pico',
    labels={'hora': 'Hora', 'count_of_orders': 'No. de Órdenes'},
    markers=True,
)
fig6.update_layout(
    xaxis=dict(range=[8, 17]),
    showlegend=False
)

# Remove the legend
fig6.update_layout(showlegend=False)

weekdays_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Group by weekday and count the number of orders
weekday_order_counts = df['weekday'].value_counts().reindex(weekdays_order).reset_index()
weekday_order_counts.columns = ['weekday', 'count_of_orders']

# Peak Day
fig7 = px.bar(
    weekday_order_counts,
    x='weekday',
    y='count_of_orders',
    title='Ordenes por dia',
    labels={'weekday': 'Dia', 'count_of_orders': 'No. de Ordenes'},
    color='weekday',
)

# Remove the legend
fig7.update_layout(showlegend=False)

# Create columns for displaying the charts
col1, col2 = st.columns([3, 3])

with col1:
    st.plotly_chart(fig1)
with col2:
    st.plotly_chart(fig2)

# Create columns for displaying the charts
col3, col4 = st.columns([3, 3])

with col3:
    st.plotly_chart(fig3)
with col4:
    st.plotly_chart(fig4)


# Create columns for displaying the charts
col6, col7 = st.columns([3, 3])

with col6:
    st.plotly_chart(fig6)
with col7:
    st.plotly_chart(fig7)

