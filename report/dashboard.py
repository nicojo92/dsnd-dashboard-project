from fasthtml.common import *
import matplotlib.pyplot as plt

from employee_events import QueryBase, Employee, Team

from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent



class ReportDropdown(Dropdown):

    def build_component(self, entity_id, model):

        self.label = model.name

        return super().build_component(entity_id, model)


    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):

    def build_component(self, entity_id, model):
        return H1(model.name)


class LineChart(MatplotlibViz):

    def visualization(self, entity_id, model):

        df = model.event_counts(entity_id)
        df.fillna(0, inplace=True)
        df.set_index('event_date', inplace=True)
        df.sort_index(inplace=True)
        df = df.cumsum()
        df.columns = ['Positive', 'Negative']
        fig, ax = plt.subplots()
        ax = df.plot(kind='line', ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title('Cumulative Positive/Negative Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Events')



class BarChart(MatplotlibViz):

    predictor = load_model()


    def visualization(self, entity_id, model):

        df = model.model_data(entity_id)
        pred_probs = self.predictor.predict_proba(df)
        pred_probs = pred_probs[:, 1]

        if model.name == 'team':
            pred = pred_probs.mean()
        else:
            pred = pred_probs[0]

        fix, ax = plt.subplots()

        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)

        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')


class Visualizations(CombinedComponent):

    children = [LineChart(), BarChart()]

    outer_div_type = Div(cls='grid')


class NotesTable(DataTable):


    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]


class Report(CombinedComponent):

    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app, route = fast_app()
report = Report()

@route('/')
def get():
    return report(1, Employee())

@route('/employee/{entity_id}')
def get(entity_id:str=None):
    return report(entity_id, Employee())

@route('/team/{entity_id}')
def get(entity_id:str=None):
    return report(entity_id, Team())


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)



serve()
