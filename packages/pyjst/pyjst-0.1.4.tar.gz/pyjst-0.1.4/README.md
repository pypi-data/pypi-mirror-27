# pyjst

Bake a template from corresponding JSON object

## How to use

Install (Python 3) : `pip install pyjst`

Create a project directory with given structure :
- project_name/
    - datas/
    - templates/

In **templates/** you can put templates with extension **.html**. In **datas/** you can put
corresponding data with extension **.json**. What this module does is simply render asked template
_name.html_ with corresponding data _name.json_. The output is generated in folder **output/**.

For instance let this file tree :
- example/
    - datas/
        - example.json
        - another.json
    - templates/
        - example.html
        - another.html

So go into your project folder : `cd example`

Then generate your static page _example_ : `pyjst example`

Or generate static page _another_ : `pyjst another`

Done !  
