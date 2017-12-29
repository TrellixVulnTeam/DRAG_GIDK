from django.shortcuts import render
from django.http import HttpResponseRedirect

from DRAGProj.forms.custominputform import CustomInputForm
from DRAGProj.forms.presetform import PresetForm
from DRAGProj.forms.fitnessform import FitnessForm

import DRAG.datacontext as dc
import DRAGProj.geneticrunner as gr

import DRAGProj.dragcommon.formhelper as fh
import DRAGProj.dragcommon.pageerror as pe
import DRAGProj.dragcommon.viewshelper as vh

def index(request):
    dc.context["currentgeneration"] = 1
    gr.clearwavfiles()
    return render(request, "DRAG/index.html", {"is_home": True})

def fitness(request):
    context = dc.context
    if request.method == 'POST':
        form = FitnessForm(request.POST, size=context["populationsize"])
        if form.is_valid():
            candidatefitnesses = vh.gatherfitnessinput(form.collectfitnesses())
            population = gr.performgenetics(context["population"], candidatefitnesses)
            context["population"] = population
            gr.clearwavfiles()
            gr.processinput(population, context["bpm"])
            return HttpResponseRedirect('/RateFitness')
    else:
        try:
            bpm, population = context["bpm"], context["population"]
            vh.generationcheck(context["currentgeneration"], context["manualgenerations"])
            context["currentgeneration"] = context["currentgeneration"] + 1
            form = FitnessForm(size=context["populationsize"])
        except KeyError as k:
            return pe.catchkeyerror(request)

    context["fitnessform"] = form
    return render(request, "DRAG/fitness.html", context)

def firstfitness(request):
    context = dc.context
    try:
        bpm = context["bpm"]
        population = gr.initiliasepopulation(context["input"], context["genre"], bpm)
        gr.processinput(population, bpm)
        context["fitnessform"] = FitnessForm(size=context["populationsize"])
        context["population"] = population
        return render(request, "DRAG/fitness.html", dc.context)
    except KeyError as k:
        return pe.catchkeyerror(request)



def diversify(request):
    context = dc.context
    if request.method == 'POST':
        form = CustomInputForm(request.POST)
        if form.is_valid():
            context["genre"] = form.cleaned_data["genre"]
            context["bpm"] = form.cleaned_data["bpm"]
            context["input"] = fh.constructinput(form.cleaned_data)
            return HttpResponseRedirect('/FirstFitness')

    else:
        form = CustomInputForm()
        preset = PresetForm()
        context["presetform"] = preset

    context["form"] = form
    return render(request, 'DRAG/startdiversify.html', context)

def preset(request):
    context = dc.context
    if request.method == 'POST':
        form = PresetForm(request.POST)
        if form.is_valid():
            context["bpm"] = form.cleaned_data["bpm"]
            context["input"] = fh.getpreset(form.cleaned_data["preset"])
            context["genre"] = "Rock"
            return HttpResponseRedirect('/FirstFitness')

    else:
        return pe.catchpreseterror(request)

    return render(request, 'DRAG/startdiversify.html')

def neuralnetwork(request):
    context = dc.context
    try:
        bpm, population = context["bpm"], context["population"]
    except KeyError as k:
        return pe.catchkeyerror(request)
    return render(request, 'DRAG/neuralnetwork.html', context)

def error(request):
    return render(request, 'DRAG/error.html', dc.context)



