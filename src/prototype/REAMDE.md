# Setup Dev environment for Data Science

Run:
- `python3 -m pip install requirements.txt`
- !!! this will install some pip modules to your local machine's pip 

Setup/Create the virtual environment:
- `python3 -m virtualenv env`

Activate the virtual environment:
- `source env/bin/activate` on Unix
- `.\env\Scripts\activate` on Windows

Then inside the environment:
- `python3 -m pip install -r requirements.env.txt`

## Prototype Data Set

Can be found at [Kaggle](https://www.kaggle.com/kmldas/insect-identification-from-habitus-images)

Another good place for data :
[gblif.org](https://www.gbif.org/)
Which has developper APIs, reference at:
[API reference](https://www.gbif.org/developer/summary)
