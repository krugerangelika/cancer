import dash  # pip install dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP]
)

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
        menu_variant="dark",
        size="lg",
        align_end=True
    ),
    brand="Cancer Analytics App",
    brand_href="#",
    color="black",
    dark=True,
    className="mb-2",
    fluid=True,
    expand="xl",
    #fixed="top"
)

app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)