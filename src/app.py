import io
import re
import os
from pathlib import Path

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dash_table.Format import Format, Scheme, Trim
import dash_bio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from collections import OrderedDict
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Define custom styles
COLORS = {
    'background': '#ffffff',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#2ecc71',
    'accent': '#e74c3c',
    'header': '#2c3e50',
    'sidebar': '#f8f9fa'
}

# Define the layout components
def create_layout():
    return html.Div(
        [
            # Header
            html.Div(
                [
                    html.H1(
                        "Gene Set Enrichment Analysis Browser",
                        className="text-center mb-4",
                        style={
                            'color': 'white',
                            'fontSize': '2.5rem',
                            'fontWeight': 'bold',
                            'marginBottom': '1rem'
                        }
                    ),
                    html.P(
                        "Interactive visualization and analysis of GSEA results",
                        className="text-center",
                        style={
                            'color': 'white',
                            'fontSize': '1.2rem',
                            'opacity': '0.9'
                        }
                    ),
                ],
                className="container-fluid",
                style={
                    'padding': '2rem 0',
                    'backgroundColor': COLORS['header'],
                    'marginBottom': '2rem'
                }
            ),
            
            # Main Content with Sidebar
            html.Div(
                [
                    # Sidebar - Controls
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H4(
                                        "Controls",
                                        style={
                                            'color': COLORS['text'],
                                            'fontWeight': 'bold',
                                            'marginBottom': '1.5rem',
                                            'paddingBottom': '0.5rem',
                                            'borderBottom': f'2px solid {COLORS["primary"]}'
                                        }
                                    ),
                                    
                                    # Project Selection
                                    html.Div(
                                        [
                                            html.Label(
                                                "Select Project",
                                                className="form-label",
                                                style={'fontWeight': 'bold', 'color': COLORS['text']}
                                            ),
                                            dcc.Dropdown(
                                                id="project-selection",
                                                options=[],
                                                value=None,
                                                style={'width': '100%'},
                                                className="mb-4"
                                            ),
                                        ],
                                        className="mb-4"
                                    ),
                                    
                                    # Database Selection
                                    html.Div(
                                        [
                                            html.Label(
                                                "Select Database",
                                                className="form-label",
                                                style={'fontWeight': 'bold', 'color': COLORS['text']}
                                            ),
                                            dcc.Dropdown(
                                                id="database",
                                                options=[],
                                                value=None,
                                                style={'width': '100%'},
                                                className="mb-4"
                                            ),
                                        ],
                                        className="mb-4"
                                    ),
                                    
                                    # Gene Filter
                                    html.Div(
                                        [
                                            html.Label(
                                                "Filter by Genes",
                                                className="form-label",
                                                style={'fontWeight': 'bold', 'color': COLORS['text']}
                                            ),
                                            dcc.Input(
                                                id="genes",
                                                type="text",
                                                placeholder="Enter genes (comma-separated)...",
                                                style={
                                                    'width': '100%',
                                                    'padding': '0.5rem',
                                                    'border': f'1px solid {COLORS["primary"]}',
                                                    'borderRadius': '4px'
                                                },
                                                className="mb-4"
                                            ),
                                        ],
                                        className="mb-4"
                                    ),
                                ],
                                style={'padding': '1.5rem'}
                            ),
                        ],
                        className="col-md-3",
                        style={
                            'backgroundColor': COLORS['sidebar'],
                            'borderRadius': '8px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                            'height': '100%'
                        }
                    ),
                    
                    # Main Content Area
                    html.Div(
                        [
                            # GSEA Results Table
                            html.Div(
                                [
                                    html.H4(
                                        "GSEA Results",
                                        style={
                                            'color': COLORS['text'],
                                            'fontWeight': 'bold',
                                            'marginBottom': '1.5rem',
                                            'paddingBottom': '0.5rem',
                                            'borderBottom': f'2px solid {COLORS["primary"]}'
                                        }
                                    ),
                                    dash_table.DataTable(
                                        id="datatable",
                                        columns=[],
                                        data=[],
                                        sort_action="native",
                                        sort_mode="single",
                                        page_action="native",
                                        page_size=10,
                                        style_table={
                                            'height': '400px',
                                            'overflowY': 'auto',
                                            'border': f'1px solid {COLORS["primary"]}',
                                            'borderRadius': '4px'
                                        },
                                        style_header={
                                            'backgroundColor': COLORS['primary'],
                                            'color': 'white',
                                            'fontWeight': 'bold'
                                        },
                                        style_cell={
                                            'textAlign': 'left',
                                            'padding': '10px',
                                            'fontFamily': 'sans-serif'
                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': '#f8f9fa'
                                            }
                                        ]
                                    ),
                                ],
                                className="mb-4"
                            ),
                            
                            # Visualizations
                            html.Div(
                                [
                                    html.H4(
                                        "Visualizations",
                                        style={
                                            'color': COLORS['text'],
                                            'fontWeight': 'bold',
                                            'marginBottom': '1.5rem',
                                            'paddingBottom': '0.5rem',
                                            'borderBottom': f'2px solid {COLORS["primary"]}'
                                        }
                                    ),
                                    dcc.Graph(
                                        id="scatter-plot",
                                        style={'height': '300px', 'marginBottom': '2rem'}
                                    ),
                                    dcc.Graph(
                                        id="strip-plot",
                                        style={'height': '300px', 'marginBottom': '2rem'}
                                    ),
                                    dcc.Graph(
                                        id="dot-plot",
                                        style={'height': '300px'}
                                    ),
                                ],
                                style={'padding': '1.5rem'}
                            ),
                        ],
                        className="col-md-9"
                    ),
                ],
                className="row"
            ),
            
            dcc.Store(id="gsea-data"),
        ],
        style={
            'backgroundColor': COLORS['background'],
            'minHeight': '100vh'
        }
    )

app.layout = create_layout()

# Callbacks
@app.callback(
    Output("project-selection", "options"),
    Output("project-selection", "value"),
    Input("project-selection", "id"),
)
def update_project_selection(_):
    data_dir = Path("data")
    options = [
        {"label": d.name, "value": d.name}
        for d in data_dir.iterdir()
        if d.is_dir()
    ]
    if not options:
        raise PreventUpdate
    return options, options[0]["value"]

@app.callback(
    Output("database", "options"),
    Output("database", "value"),
    Input("project-selection", "value"),
)
def get_database(project):
    if not project:
        raise PreventUpdate
    data_dir = Path("data") / project
    options = [
        {"label": f.name.split(".csv")[0], "value": f.name}
        for f in data_dir.glob("*.csv")
    ]
    return options, options[0]["value"] if options else None

@app.callback(
    Output("gsea-data", "data"),
    Input("project-selection", "value"),
    Input("database", "value"),
)
def get_gsea_data(project, database):
    if not project or not database:
        raise PreventUpdate
    
    data_path = Path("data") / project / database
    data = pd.read_csv(data_path)
    data["length"] = data["lead_genes"].str.split(";").apply(len)
    return data.to_json(date_format="iso", orient="split")

@app.callback(
    Output("datatable", "data"),
    Output("datatable", "columns"),
    Input("gsea-data", "data"),
    Input("genes", "value"),
)
def get_gsea_terms(data, genes):
    if not data:
        raise PreventUpdate
    
    gsea_data = pd.read_json(io.StringIO(data), orient="split")
    
    columns = [
        {"name": "Term", "id": "Term"},
        {"name": "ES", "id": "ES", "format": Format(precision=3)},
        {"name": "NES", "id": "NES", "format": Format(precision=3)},
        {"name": "P-Value", "id": "P-Value", "format": Format(precision=3)},
        {"name": "FDR", "id": "FDR", "format": Format(precision=3)},
        {"name": "Genes %", "id": "Genes %", "format": Format(precision=1)},
        {"name": "Lead Genes", "id": "Lead Genes"},
    ]
    
    df = pd.DataFrame({
        "Term": gsea_data["term"],
        "ES": gsea_data["es"],
        "NES": gsea_data["nes"],
        "P-Value": gsea_data["nom p-val"],
        "FDR": gsea_data["fdr q-val"],
        "Genes %": gsea_data["gene %"],
        "Lead Genes": gsea_data["length"],
        "list Lead Genes": gsea_data["lead_genes"],
    })
    
    df = df[df["P-Value"] <= 0.05]
    
    if genes:
        genes = re.split(r", ?", genes.strip(", "))
        df = df[df["list Lead Genes"].apply(lambda x: any(gene in x.split(";") for gene in genes))]
    
    return df.to_dict("records"), columns

@app.callback(
    Output("scatter-plot", "figure"),
    Output("strip-plot", "figure"),
    Output("dot-plot", "figure"),
    Input("datatable", "active_cell"),
    Input("datatable", "data"),
)
def update_plots(active_cell, table_data):
    if not active_cell or not table_data:
        raise PreventUpdate
    
    # Get the row data using the row index
    row_idx = active_cell["row"]
    row_data = table_data[row_idx]
    
    # Get the lead genes from the list Lead Genes column
    lead_genes = row_data["list Lead Genes"].split(";")
    
    # Common layout settings
    layout_settings = {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': COLORS['text']},
        'title': {'font': {'color': COLORS['text']}},
        'xaxis': {'gridcolor': '#e1e1e1'},
        'yaxis': {'gridcolor': '#e1e1e1'}
    }
    
    # Create scatter plot
    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(
        x=range(len(lead_genes)),
        y=[1] * len(lead_genes),
        mode="markers+text",
        name="Lead Genes",
        text=lead_genes,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            color=COLORS['primary'],
            size=10
        )
    ))
    scatter_fig.update_layout(
        title=f"Lead Genes Distribution - {row_data['Term']}",
        showlegend=False,
        **layout_settings
    )
    
    # Create strip plot
    strip_fig = go.Figure()
    strip_fig.add_trace(go.Box(
        y=[1] * len(lead_genes),
        boxpoints="all",
        jitter=0.3,
        pointpos=-1.8,
        name="Lead Genes",
        text=lead_genes,
        hoverinfo="text",
        marker=dict(
            color=COLORS['primary'],
            size=8
        )
    ))
    strip_fig.update_layout(
        title=f"Lead Genes Distribution (Strip Plot) - {row_data['Term']}",
        showlegend=False,
        **layout_settings
    )
    
    # Create dot plot
    dot_fig = go.Figure()
    dot_fig.add_trace(go.Scatter(
        x=range(len(lead_genes)),
        y=[1] * len(lead_genes),
        mode="markers+text",
        name="Lead Genes",
        text=lead_genes,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            color=COLORS['primary'],
            size=10
        )
    ))
    dot_fig.update_layout(
        title=f"Lead Genes Distribution (Dot Plot) - {row_data['Term']}",
        showlegend=False,
        **layout_settings
    )
    
    return scatter_fig, strip_fig, dot_fig

if __name__ == "__main__":
    app.run_server(debug=True) 