import dash_bootstrap_components as dbc
from dash import html,dcc

file_transfer_card = dbc.Card([
    dbc.CardHeader("File Transfer", className="card-title"),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([dcc.Upload(dbc.Button(html.Span([html.I(className="bi bi-upload", style={"margin-right": "5px"}),
                                                      "Upload .tls"]),
                                           className="d-grid gap-2",
                                           style={"width": "100%"}),
                                id="upload",
                                style={"width": "100%",
                                       "padding-bottom": "15px"}),
                     dbc.Button(html.Span([html.I(className="bi bi-download", style={"margin-right": "5px"}),
                                           "Download .tls"]),
                                className="d-grid gap-2",
                                id="download_button",
                                style={"width": "100%"})]),
            dcc.Download(id="download")
        ], align="center")
    ])
])
