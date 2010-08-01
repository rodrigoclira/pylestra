#!/usr/bin/env python
# -*- coding: utf-8 -*-

def index():
    palestras = db().select(Palestra.ALL,orderby=~Palestra.id)
    return dict(palestras=palestras)

def adicionar():
    form = SQLFORM(Palestra)
    if form.accepts(request.post_vars,session):
        response.flash='Adicionado com sucesso'
    return dict(form=form)

def detalhe():
    palestra = db.palestra[request.args(0)]
    
    if not palestra:
        response.flash = "Palestra inválida"
        
    return dict(palestra=palestra)
    
    
    