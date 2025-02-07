from fasthtml.common import *

import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
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


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
#### YOUR CODE HERE
class ReportDropdown(Dropdown):

    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    #### YOUR CODE HERE
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        #### YOUR CODE HERE
        
        # Return the output from the
        # parent class's build_component method
        #### YOUR CODE HERE
    def build_component(self, entity_id ,model):
     
        self.label = model.name
        return super().build_component(entity_id, model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
    def component_data(self, entity_id: Any,model: Any):
       
        return model.names()


# Create a subclass of base_components/BaseComponent
# called `Header`
#### YOUR CODE HERE
class Header(BaseComponent):
  

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
    def build_component(self, entity_id ,model):
        return H1(model.name)
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):
  
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    def visualization(self, asset_id, model):
        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        data = model.event_counts(asset_id)
        
        # Use the pandas .fillna method to fill nulls with 0
        data = data.fillna(0)
        
        # User the pandas .set_index method to set
        # the date column as the index
        data.set_index('event_date', inplace=True)
        
        # Sort the index
        data.sort_index(inplace=True)
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        data = data.cumsum()
        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        data.columns = ['Positive', 'Negative']
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        fig, ax = plt.subplots()
        
        # call the .plot method for the
        # cumulative counts dataframe
        data.plot(ax=ax)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax=ax)

        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')

        
        # Set title and labels for x and y axis
        ax.set_title('Cumulative Event Counts')
        ax.set_xlabel('Date')
        ax.set_ylabel('Event Count')


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
#### YOUR CODE HERE
class BarChart(MatplotlibViz):

    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE
    predictor = load_model()  # Class-level attribute for the ML model


    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, asset_id, model):

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE
        data = model.model_data(asset_id)
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE
        prediction = self.predictor.predict_proba(data)

        
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE
        prediction = prediction[:, 1].reshape(-1, 1)

        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE
        pred = prediction.mean() if model.name == 'team' else prediction[0]

        # Initialize a matplotlib subplot
        #### YOUR CODE HERE
        fig, ax = plt.subplots()
        
        
        # Run the following code unchanged
        ax.barh([''], pred)
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')

 
# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    children = [
        LineChart(),
        BarChart()
    ]
    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
#### YOUR CODE HERE
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    #### YOUR CODE HERE
    def component_data(self, entity_id,model):
        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        #### YOUR CODE HERE
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
    
# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):
   
    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    #### YOUR CODE HERE
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# Initialize a fasthtml app 
app = FastHTML()

# Initialize the `Report` class
report = Report()


# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE
@app.get('/')
def home():
    
    # Call the initialized report
    # pass None and an instance
    # of the QueryBase class as arguments
    # Return the result
    #### YOUR CODE HERE
    return report(1, Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
#### YOUR CODE HERE
@app.get('/employee/{id}')
def employee_profile(id: str):
    
    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    return report(int(id), Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
@app.get('/team/{id}')
def team_profile(id: str):
 
    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    return report(int(id), Team())



# Keep the below code unchanged!
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