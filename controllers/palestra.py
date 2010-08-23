#!/usr/bin/env python
# -*- coding: utf-8 -*-

def index():
    palestras = db().select(Palestra.ALL,orderby=~Palestra.id)
    return dict(palestras=palestras)

@auth.requires_login()
def cadastrar():
    form = SQLFORM(Palestra)
    if form.accepts(request.post_vars,session):
        response.flash='Adicionado com sucesso'
        redirect(URL(r=request,f="index"))
    return dict(form=form)

def detalhe():
    palestra = db.palestra[request.args(0)]
    
    if not palestra:
        response.flash = "Palestra inválida"
        
    return dict(palestra=palestra)
    
    
    