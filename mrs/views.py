from django.shortcuts import render, redirect
from .recommendation import input

def movie(request):
    return render(request, 'mrs/movie.html')


def result(request):
    movie=""
    if request.method=="GET":
      movie=request.GET.get('movie')

    data=input(movie)
    if data=='Please check the spelling or try with some other movies':
      return render(request, 'mrs/movie.html', {'data':data})

    poster=data[0][-1]
    link=data[0][6]
    title=data[0][0]
    overview=data[0][1]
    status=data[0][2]
    date=data[0][3]
    duration=data[0][4]
    revenue=data[0][5]

    r1=data[2][0][0]
    r2=data[2][0][1]
    r3=data[2][0][2]
    r4=data[2][0][3]
    r5=data[2][0][4]
    r6=data[2][0][5]
    r7=data[2][0][6]
    r8=data[2][0][7]
    r9=data[2][0][8]
    r10=data[2][0][9]

    p1=data[2][1][0]
    p2=data[2][1][1]
    p3=data[2][1][2]
    p4=data[2][1][3]
    p5=data[2][1][4]
    p6=data[2][1][5]
    p7=data[2][1][6]
    p8=data[2][1][7]
    p9=data[2][1][8]
    p10=data[2][1][9]


    c=data[1] 
    i1=data[3][0]
    i2=data[3][1]
    i3=data[3][2]
    i4=data[3][3]
    i5=data[3][4]
    

    return render(request, 'mrs/result.html', {'mt':title, 'mo':overview, 'ms':status, 'mdate':date, 'mduration':duration,
                            'mr':revenue, 'p':poster, 'l':link, 'r1':r1, 'r2':r2, 'r3':r3, 'r4':r4, 'r5':r5, 'r6':r6,
                             'r7':r7, 'r8':r8, 'r9':r9, 'r10':r10, 'p1':p1, 'p2':p2, 'p3':p3, 'p4':p4, 'p5':p5, 'p6':p6,
                            'p7':p7, 'p8':p8, 'p9':p9, 'p10':p10, 'cast':data[1], 'i1':i1, 'i2':i2, 'i3':i3, 'i4':i4, 'i5':i5})