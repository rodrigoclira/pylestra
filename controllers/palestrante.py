#!/usr/bin/env python
# -*- coding: utf-8 -*-

def index():
    return {'message':T("Hello")}
    
def adicionar():
    form = SQLFORM(Palestrante)
    if form.accepts(request.post_vars,session):
        response.flash='Adicionado com sucesso'
    return dict(form=form)

def show():
    return response.download(request,db)
    