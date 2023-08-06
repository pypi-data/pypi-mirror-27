'''
The MIT License (MIT)

Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


from singularity.views.trees import (
    container_tree, 
    container_similarity,
    container_difference
)

from singularity.analysis.classify import estimate_os

from flask import (
    Flask, 
    render_template, 
    request
)

from flask_restful import Resource, Api
from werkzeug import secure_filename
import webbrowser
import tempfile
import shutil
import random
import os

# SERVER CONFIGURATION ##############################################
class SingularityServer(Flask):

    def __init__(self, *args, **kwargs):
        super(SingularityServer, self).__init__(*args, **kwargs)

        # Set up temporary directory on start of application
        self.tmpdir = tempfile.mkdtemp()
        self.tree = None # Holds tree visualization data
        self.sims = None  # Holds similarity score visualization data
        self.image = None
        self.images = None
        self.sudopw = None


# API VIEWS #########################################################
# eventually we can have views or functions served in this way...

app = SingularityServer(__name__)
#api = Api(app)    
#api.add_resource(apiExperiments,'/experiments')
#api.add_resource(apiExperimentSingle,'/experiments/<string:exp_id>')


# BAR PLOTS TO COMPARE TO PACKAGES #################################
@app.route('/container/os')
def app_plot_os_sims():
    if app.sims == None:
         sims = estimate_os(container=app.image,
                            sudopw=app.sudopw,
                            return_top=False)
         sims = sims.sort_values(by=['SCORE'])
         app.sims = sims['SCORE'].to_dict()
    container_name = os.path.basename(app.image).split(".")[0]
    return render_template('similarity_scatter.html',sim_scores=app.sims,
                                                     container_name=container_name)

# INTERACTIVE CONTAINER EXPLORATION ################################

@app.route('/container/tree')
def app_container_tree():
    # The server will store the package name and result object for query
    if app.tree == None:
        app.tree = container_tree(app.image)
    container_name = os.path.basename(app.image).split(".")[0]
    return render_template('container_tree.html',graph=app.tree['graph'],
                                                 files=app.tree['files'],
                                                 container_name=container_name)
    
@app.route('/containers/subtract')
def difference_tree():
    # The server will store the package name and result object for query
    if app.tree == None:
        app.tree = container_difference(app.images[0],app.images[1])
    container1_name,container2_name = get_container_names()
    title = "%s minus %s" %(container1_name,container2_name)
    return render_template('container_tree.html',graph=app.tree['graph'],
                                                 files=app.tree['files'],
                                                 container_name=title)

@app.route('/containers/similarity')
def app_similar_tree():
    # The server will store the package name and result object for query
    if app.tree == None:
        app.tree = container_similarity(app.images[0],app.images[1])
    container1_name,container2_name = get_container_names()
    title = "%s INTERSECT %s" %(container1_name,container2_name)
    return render_template('container_tree.html',graph=app.tree['graph'],
                                                 files=app.tree['files'],
                                                 container_name=title)

def get_container_names():
    '''return container names for one or more images, depending on what
    app initialized for.
    '''
    if app.images != None:
        container1_name = os.path.basename(app.images[0]).split(".")[0]
        container2_name = os.path.basename(app.images[1]).split(".")[0]
        return container1_name,container2_name
    return None

# START FUNCTIONS ##################################################
    
# Function to make single package/image tree
def make_tree(image,port=None,sudopw=None):
    app.image = image
    app.sudopw = sudopw
    if port==None:
        port=8088
    print("It goes without saying. I suspect now it's not going.")
    webbrowser.open("http://localhost:%s/container/tree" %(port))
    app.run(host="0.0.0.0",debug=False,port=port)


# Function to make bar chart to compare to os
def plot_os_sims(image,port=None,sudopw=None):
    app.image = image
    app.sudopw = sudopw
    if port==None:
        port=8088
    print("The not remembering is part of the disability, my dear fish.")
    webbrowser.open("http://localhost:%s/container/os" %(port))
    app.run(host="0.0.0.0",debug=False,port=port)


# Function to make similar tree to compare images
def make_sim_tree(image1,image2,port=None):
    app.images = [image1,image2]
    if port==None:
        port=8088
    print("The recipe for insight can be reduced to a box of cereal and a Sunday afternoon.")
    webbrowser.open("http://localhost:%s/containers/similarity" %(port))
    app.run(host="0.0.0.0",debug=False,port=port)


# Function to make difference tree for two images
def make_diff_tree(image1,image2,port=None):
    app.images = [image1,image2]
    if port==None:
        port=8088
    print("Pandas... just let them go.")
    webbrowser.open("http://localhost:%s/containers/subtract" %(port))
    app.run(host="0.0.0.0",debug=True,port=port)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
