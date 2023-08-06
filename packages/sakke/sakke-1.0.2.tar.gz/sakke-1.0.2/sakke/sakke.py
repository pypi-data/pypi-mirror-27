# coding: utf8
"""SaKKe: utilitaire de statistiques de devoirs

usage: sakke [--name=<name>] [--transform=<transform>] [--option=<name:value> ...] <exercice_bareme> ...

Options:
  -h --help       Montre l'aide
  --name=<name>   Nom du devoir. [default: -]
  --transform=<transform>   Transformation à appliquer sur la note finale.
                            C'est une expression où x représente la note.
                            [default: x]
  --option=<name:value>     Option pour le rendu. Peut-être répétée.
                            Valeurs par défaut des options suportées
                                * latex_documentclass_options:a4paper,10pt,landscape
                                * latex_geometry_options:top=1cm,right=1cm,bottom=1cm,left=1cm
                                * latex_font_size:tiny
  exercice_bareme   Chemin vers les exercices (le format doit correspondre à l'exemple)

"""
import csv
import sys
# import statistics (requires >= 3.4)
import numpy
import os
import json
from docopt import docopt
from jinja2 import Environment, FileSystemLoader
from . import __version__
import operator

NOTE=20
TOTAL=4
SAKKE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(SAKKE_PATH, 'templates')

OPTIONS = {
    "latex_documentclass_options" : "a4paper,10pt,landscape",
    "latex_font_size": "tiny",
    "latex_geometry_options": "top=1cm,right=1cm,bottom=1cm,left=1cm"
}


def clean_line(l):
    def el_clean(e):
        # replace hypothetic ',' by ','
        # e.g export from calc with french number formatting
        ec = e.replace(',', '.')
        try:
            result = float(ec)
            return float(ec)
        except Exception as e:
            print("La valeur ->%s<- n'est pas valide" % ec)
            raise e
    try:
        result = list(map(el_clean, l[2:]))
        return result
    except Exception as e:
        print("Une erreur s'est glissée pour %s" % " ".join(l[0:2]))
        raise e

def main():
    arguments = docopt(__doc__, version=__version__)
    print(arguments)
    exercices_baremes = arguments['<exercice_bareme>']
    name = arguments['--name']
    transform = lambda x: eval(arguments['--transform'])
    # construction des options
    options = {}
    options.update(OPTIONS)
    options.update(dict(map(lambda x: x.split(':'), arguments['--option'])))
    print(options)
    if len(exercices_baremes) < 1:
        sys.exit(0)

    files = []
    for exercice_bareme in exercices_baremes:
        with open(exercice_bareme) as f:
            lines =  f.readlines()
            bareme = lines[0:5]
            result = lines[5:]
            files.append({
                'bareme': bareme,
                'result': result,
                'name': exercice_bareme
                })
# grouping by student
    students = {}
# students = {
#   s1 : {
#      note: # note
#      sum: # sum
#      exercice1 : {
#         raw : [] # raw results
#         sum :    # the sum according the
#      }
#      exercice2 : [],
#   }
# }
    bar = {}
# bareme = {
#     'title': [] # titles of the questions
#     'points': [] # corresponding points
# }
#
#
    general = {
        'name': name,
        'total': 0}

    for f in files:
        exo = f['name']
        baremefile = f['bareme']
        exofile = f['result']
        exoname = os.path.basename(exo).split('.')[0].replace('_', '-')
        # bareme should only contains two lines
        reader = list(csv.reader(baremefile, delimiter=','))
        bar.setdefault(exoname, {})
        bar[exoname]['title'] = reader[0][2:]
        bar[exoname]['points'] = clean_line(reader[1][0:])
        bar[exoname]['total'] = sum(bar[exoname]['points'])
        bar[exoname]['sum'] = [0]*len(bar[exoname]['title'])

        # filling the general
        general['total'] = general['total'] + bar[exoname]['total']
        # max_questions
        general.setdefault('max_questions', len(reader[0]))
        if general['max_questions'] < len(reader[0]):
            general['max_questions'] = len(reader[0])

        reader = csv.reader(exofile, delimiter=',')
        for row in reader:
            name = ' '.join(row[0:2]).decode('UTF-8')
            students.setdefault(name, {})
            students[name].setdefault('exercices', {})
            students[name]['name'] = name
            raw = clean_line(row[0:])
            corrected = raw[0:]
            # set raw results
            students[name]['exercices'].setdefault(exoname, {})
            students[name]['exercices'][exoname].setdefault('raw', raw)
            # update success
            try:
                bar[exoname]["sum"] = map(operator.add, bar[exoname]["sum"], raw)
            except:
                import pdb; pdb.set_trace()
            # compute corrected result
            for i in range(len(bar[exoname]['title'])):
                corrected[i] = raw[i] * bar[exoname]['points'][i] / TOTAL
            students[name]['exercices'][exoname].setdefault('corrected', corrected)
            # compute the sum
            s = sum(corrected)
            students[name]['exercices'][exoname].setdefault('sum', s)
            # compute the note
            note = s/bar[exoname]['total'] * NOTE
            students[name]['exercices'][exoname].setdefault('note', note)
            # repeating the bareme
            students[name]['exercices'][exoname].setdefault('bar', bar[exoname])
            # number of extra columns
            students[name]['exercices'][exoname]['bar']['extra'] = general['max_questions'] - len(bar[exoname]['title'])
            # filling student general
            students[name].setdefault('sum', 0)
            students[name]['sum'] = s + students[name]['sum']
            students[name].setdefault('note', 0)
            students[name]['note'] = transform(round(students[name]['sum']/general['total']*NOTE, 1))
            students[name]['total'] = general['total']


    # update success
    for exoname, data in bar.items():
        data["success"] = map( lambda x: round(100*x/(TOTAL*len(students.values()))), data["sum"])

    # update rank
    ranked = sorted(students.values(), key=operator.itemgetter('note'), reverse=True)
    for i in range(len(ranked)):
        ranked[i]["rank"] = i+1

    general['notes'] = numpy.array(list(map(lambda e: e['note'], students.values())))
    general['avg'] = round(numpy.mean(general['notes']), 1)
    general['std'] = round(numpy.std(general['notes']), 1)
    # gets back a list to be json-serializable
    general['notes'] = list(general['notes'])
    results = {
        "bar": bar,
        "general": general,
        "students": ranked
    }

    # Rendering tex
    env = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_DIR))
    template = env.get_template('stats.tex.j2')
    rendered_text = template.render(results=results, options=options)
    with open('out.tex', 'w') as f:
        f.write(rendered_text.encode('UTF-8'))

    template = env.get_template('stats.html.j2')
    rendered_text = template.render(results=json.dumps(results), options=options)
    with open('out.html', 'w') as f:
        f.write(rendered_text.encode('UTF-8'))


if __name__ == '__main__':
    #arguments = docopt(__doc__, version=0.1)
    #(arguments['<exercice:bareme>'])
    try:
        main()
    except Exception as e:
        print("Le programme s'est terminé avec une erreur : ")
        print(e)
