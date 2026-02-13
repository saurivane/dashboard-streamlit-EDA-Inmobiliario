"""
Configuración del dashboard - Colores y layouts
"""

COLORS = {
    'primary': '#4CAF50',
    'secondary': '#81C784',
    'accent': '#A5D6A7',
    'light': '#C8E6C9',
    'dark': '#1E1E1E',
    'text': '#FFFFFF'
}

LAYOUT_OPTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFFFFF', size=12),
    title_font=dict(size=16, color='#FFFFFF'),
    legend=dict(
        font=dict(color='#FFFFFF', size=11),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1
    ),
    xaxis=dict(
        title_font=dict(color='#FFFFFF'),
        tickfont=dict(color='#CCCCCC'),
        gridcolor='rgba(255,255,255,0.1)'
    ),
    yaxis=dict(
        title_font=dict(color='#FFFFFF'),
        tickfont=dict(color='#CCCCCC'),
        gridcolor='rgba(255,255,255,0.1)'
    )
)

PIE_LAYOUT_OPTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFFFFF', size=12),
    title_font=dict(size=16, color='#FFFFFF'),
    legend=dict(
        font=dict(color='#FFFFFF', size=11),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1
    )
)

CORR_LAYOUT_OPTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFFFFF', size=12),
    title_font=dict(size=16, color='#FFFFFF'),
    legend=dict(font=dict(color='#FFFFFF'))
)
