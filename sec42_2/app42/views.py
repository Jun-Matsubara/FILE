from django.shortcuts import render, redirect
from django.http import HttpResponse
import os,json,time
from . import fs_data

BASE_DIR = os.path.dirname(__file__)
FILES_DIR = BASE_DIR + '/files'

def index(request):
    return render(request,'app42/index.html')

def upload(request):
    upfile= request.FILES.get('upfile',None)
    if upfile is None:
        return render(request,'app42/error.html',{'msg':'アップロード失敗'})
    if upfile.name == '':
        return render(request,'app42/error.html',{'msg':'アップロード失敗'})
    print('OK')
    meta = {
        'name':request.POST.get('name','名無し'),
        'memo':request.POST.get('memo','なし'),
        'pw':request.POST.get('pw',''),
        'limit':int(request.POST.get('limit','1')),
        'count':int(request.POST.get('count','0')),
        'filename':upfile.name,
    }
    print('OK2')
    if (meta['limit']== 0) or (meta['pw']== ''):
        return render(request,'app42/error.html',{'msg':'パラメータが不正です'})
    print('OK3')
    fs_data.save_file(upfile,meta)
    print('OK5')
    url=request._current_scheme_host + '/app42/download/' + meta['id']
    meta['url']=url
    meta['mode']= 'upload'
    print('OK6')
    return render(request,'app42/info.html',meta)

def download(request,id):
    meta= fs_data.get_data(id)
    if meta is None: 
        return render(request,'app42/error.html',{'msg':'パラメータが不正です'})
    print('OK13') 
    download='download'
    url=request._current_scheme_host + '/app42/download_go/' + id
    meta['mode']=download
    meta['url']=url     
    print('OK14')
    return render(request, 'app42/info.html',meta)

def download_go(request,id):
    meta = fs_data.get_data(id)
    if meta is None: 
        return render(request,'app42/error.html',{'msg':'パラメータが不正です'})
    print('OK8')
    pw= request.POST.get('pw','')
    if pw != meta['pw']:
        return render(request,'app42/error.html',{'msg':'パスワードが違います'})
    print('OK9')
    meta['count']=meta['count'] - 1
    if meta['count']<0:
        return render(request,'app42/error.html',{'msg':'ダウンロード回数を超えました'})
    print('OK10')
    fs_data.set_data(id,meta)
    if meta['time_limit']< time.time():
        return render(request,'app42/error.html',{'msg':'ダウンロード期限が過ぎています'})
    print('OK12')
    response = HttpResponse(
        open(FILES_DIR + '/' +meta['filename'],'rb').read(),
        content_type="imege/jpeg"
    )
    #meta['path']でやると保存先fileの中に同じ写真が何枚も入るからやめた
    print('OK15')
    #file_info = 'attachment; filename=' +meta['filename']
    #response['Content-Disposition'] = file_info
    print('finish')
    return response
    
        
