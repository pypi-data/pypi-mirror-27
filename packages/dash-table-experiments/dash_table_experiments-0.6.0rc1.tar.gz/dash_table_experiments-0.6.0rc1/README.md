# dash-table-experiments

What does a Dash Table component look like? `dash-table-experiments` is a package of alpha-level explorations in a Dash `Table` component. Everything is subject to change. See the [CHANGELOG.md](https://github.com/plotly/dash-table-experiments/blob/master/CHANGELOG.md) for recent changes.

The Dash Table component will likely be merged into the [`dash-core-components`](https://github.com/plotly/dash-core-componets) once it stabilizes.

For updates and more, please see the [dash community discussion on tables](https://community.plot.ly/t/display-tables-in-dash/4707/36).

Example from `usage.py`
![Dash DataTable](https://github.com/plotly/dash-table-experiments/raw/master/images/DataTable.gif)

Example from `usage-editable.py`
![Editable Dash DataTable](https://github.com/plotly/dash-table-experiments/raw/master/images/Editable-DataTable.gif)

## Installation ##

```
# Install
$ pip install dash-table-experiments
```

### Usage with Callbacks ###
Per [this Dash community answer](https://community.plot.ly/t/dash-datatable-using-callbacks/6756/2), to use callbacks with `dash-table-experiments` there are two key steps (for a full working example see [usage-callback.py](./usage-callback.py)):

```
# 1. Declare the table in app.layout
dt.DataTable(
    rows=[{}], # initialise the rows
    row_selectable=True,
    filterable=True,
    sortable=True,
    selected_row_indices=[],
    id='datatable'
)

# 2. Update rows in a callback
@app.callback(Output('datatable', 'rows'), [Input('field-dropdown', 'value')])
def update_datatable(user_selection):
    '''
    For user selections, return the relevant table
    '''
    if user_selection == 'Summary':
        return DATA.to_dict('records')
    else:
        return SOMEOTHERDATA.to_dict('records')
```

### Usage with Graphs ###
This example demonstrates the user's ability to select data points either in the table which updates the plot, or in the reverse, select points on the graph which updates the selection on the table. For a full working example see [usage.py](./usage.py).

### Usage Enabling Edits to a Table ###
Enable edits to a table which updates other objects e.g. a graph. For a full working example see [usage-editable.py](https://github.com/plotly/dash-table-experiments/tree/master/usage-editable.py)

### Using in Multi Page Apps ###

If you use `dash-table-experiments` inside a [multi-page app](https://plot.ly/dash/urls),
you will need to initialize an empty table inside your layout like this:
```
app.layout = html.Div([
    html.Div(id='content'),
    dcc.Location(id='location', refresh=False),

    # initialize an empty table
    html.Div(dt.DataTable(rows=[{}]), style={‘display’: ‘none’})
])
```

Why? Here's a little context from the community forum: https://community.plot.ly/t/display-tables-in-dash/4707/40?u=chriddyp
> When Dash serves the page, it crawls the `app.layout` to see which component libraries are being used (e.g. `dash_core_components`). Then, with this list of unique component libraries, it serves the necessary JS and CSS bundles that are distributed with those component libraries.

> In multi-page apps, we’re serving `dash_table_experiments` on a separate page, as the response of a callback. Dash only sees `dash_html_components` and `dash_core_components` in the app.layout and so it doesn’t serve the necessary JS and CSS bundles that are required for the dash-table-components component that is rendered in the future.

> This is a design flaw of Dash. For now, you can get around this issue by rendering a hidden dash-table-experiments component in the layout like above.
